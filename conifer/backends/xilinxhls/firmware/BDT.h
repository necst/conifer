// Copyright 2022 Novel, Emerging Computing System Technologies Laboratory 
//                (NECSTLab), Politecnico di Milano

// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at

//     http://www.apache.org/licenses/LICENSE-2.0

// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

// Part of this source file comes from the Conifer open-source project 
// (https://github.com/thesps/conifer)

#ifndef BDT_H__
#define BDT_H__

#include "ap_fixed.h"
#include "utils.h"
#include "hls_stream.h"

namespace BDT{

constexpr int pow2(int x){
  return x == 0 ? 1 : 2 * pow2(x - 1);
}

constexpr int fn_nodes(int max_depth){
  return pow2(max_depth + 1) - 1;
}

constexpr int fn_leaves(int max_depth){
  return pow2(max_depth);
}

constexpr int fn_classes(int n_classes){
  // Number of trees given number of classes
  return n_classes == 2 ? 1 : n_classes;
}

template<int max_depth, class input_t, class score_t, class threshold_t>
struct Tree {
private:
  static constexpr int n_nodes = fn_nodes(max_depth);
  static constexpr int n_leaves = fn_leaves(max_depth);
public:
	int feature[n_nodes];
	threshold_t threshold[n_nodes];
	score_t value[n_nodes];
	int children_left[n_nodes];
	int children_right[n_nodes];
	int parent[n_nodes];

	score_t decision_function(input_t x) const{
		#pragma HLS pipeline II = 1
		#pragma HLS ARRAY_PARTITION variable=feature
		#pragma HLS ARRAY_PARTITION variable=threshold
		#pragma HLS ARRAY_PARTITION variable=value
		#pragma HLS ARRAY_PARTITION variable=children_left
		#pragma HLS ARRAY_PARTITION variable=children_right
		#pragma HLS ARRAY_PARTITION variable=parent
    // These resource pragmas prevent the array of trees from being partitioned
    // They should be unnecessary anyway due to their own partitioning above
		/*#pragma HLS RESOURCE variable=feature core=ROM_nP_LUTRAM
		#pragma HLS RESOURCE variable=threshold core=ROM_nP_LUTRAM
		#pragma HLS RESOURCE variable=value core=ROM_nP_LUTRAM
		#pragma HLS RESOURCE variable=children_left core=ROM_nP_LUTRAM
		#pragma HLS RESOURCE variable=children_right core=ROM_nP_LUTRAM
		#pragma HLS RESOURCE variable=parent core=ROM_nP_LUTRAM*/

		bool comparison[n_nodes];
		bool activation[n_nodes];
		bool activation_leaf[n_leaves];
		score_t value_leaf[n_leaves];

		#pragma HLS ARRAY_PARTITION variable=comparison
		#pragma HLS ARRAY_PARTITION variable=activation
		#pragma HLS ARRAY_PARTITION variable=activation_leaf
		#pragma HLS ARRAY_PARTITION variable=value_leaf

		// Execute all comparisons
		Compare: for(int i = 0; i < n_nodes; i++){
			#pragma HLS unroll
			// Only non-leaf nodes do comparisons
			// negative values mean is a leaf (sklearn: -2)
			if(feature[i] >= 0){
				comparison[i] = x[feature[i]] <= threshold[i];
			}else{
				comparison[i] = true;
			}
		}

		// Determine node activity for all nodes
		int iLeaf = 0;
		Activate: for(int i = 0; i < n_nodes; i++){
			#pragma HLS unroll
			// Root node is always active
			if(i == 0){
				activation[i] = true;
			}else{
				// If this node is the left child of its parent
				if(i == children_left[parent[i]]){
					activation[i] = comparison[parent[i]] && activation[parent[i]];
				}else{ // Else it is the right child
					activation[i] = !comparison[parent[i]] && activation[parent[i]];
				}
			}
			// Skim off the leaves
			if(children_left[i] == -1){ // is a leaf
				activation_leaf[iLeaf] = activation[i];
				value_leaf[iLeaf] = value[i];
				iLeaf++;
			}
		}

		score_t y = 0;
		for(int i = 0; i < n_leaves; i++){
			if(activation_leaf[i]){
				return value_leaf[i];
			}
		}
		return y;
	}
};

template<int n_trees, int max_depth, int n_classes, class input_t, class score_t, class threshold_t>
struct BDT{

public:
    score_t normalisation;
	score_t init_predict[fn_classes(n_classes)];
	Tree<max_depth, input_t, score_t, threshold_t> trees[n_trees][fn_classes(n_classes)];

	void decision_function(input_t x, score_t score[fn_classes(n_classes)], score_t tree_scores[fn_classes(n_classes) * n_trees]) const{
		#pragma HLS ARRAY_PARTITION variable=trees dim=0
		for(int j = 0; j < fn_classes(n_classes); j++){
			score[j] = init_predict[j];
		}
		Trees:
		for(int i = 0; i < n_trees; i++){
			Classes:
			for(int j = 0; j < fn_classes(n_classes); j++){
                score_t s = trees[i][j].decision_function(x);
				score[j] += s;
                tree_scores[i * fn_classes(n_classes) + j] = s;
			}
		}
        for(int j = 0; j < fn_classes(n_classes); j++){
            score[j] *= normalisation;
        }
	}

};

enum Bank_buffer_flag {
	BANK_BUFFER_FLAG_CAPTURE_ENABLE		= 0,
	BANK_BUFFER_FLAG_CAPTURE			= 1,
	BANK_BUFFER_FLAG_PEEK_ENABLE		= 2,
	BANK_BUFFER_FLAG_PEEK				= 3,
	BANK_BUFFER_FLAG_DISCARD_ENABLE 	= 4,
	BANK_BUFFER_FLAG_DISCARD			= 5,
	BANK_BUFFER_FLAG_TRANSPARENT_ENABLE	= 6,
	BANK_BUFFER_FLAG_TRANSPARENT		= 7
};

template<class input_t, class command_t, unsigned int max_parallel_samples, unsigned int max_bank_count>
struct Bank_buffer {

private:
	ap_uint<bitsizeof(max_bank_count + 1)> bank_id;
	input_t buffer[max_parallel_samples + 1];
	ap_uint<bitsizeof(max_parallel_samples + 1)> curr_in  = 0;
	ap_uint<bitsizeof(max_parallel_samples + 1)> curr_out = 0;
	bool empty = true;
	bool waiting_for_out = false;
	bool capture_enabled = false;
	bool transparent_enabled = false;
	void capture(
		hls::stream<input_t> &input_stream
	) {
		if (empty || curr_in != curr_out) {
			if (input_stream.read_nb(buffer[curr_in])) {
				curr_in = (curr_in + 1) % (max_parallel_samples + 1);
				empty = false;
			}
		}
	}
	void peek(
		hls::stream<input_t> &output_stream
	) {
		if (!empty) {
			output_stream << buffer[curr_out];
		}
	}
	void discard() {
		if (!empty) {
			curr_out = (curr_out + 1) % (max_parallel_samples + 1);
			empty = (curr_out == curr_in);
		}
	}

public:
	Bank_buffer(ap_uint<bitsizeof(max_bank_count + 1)> the_bank_id) {
		bank_id = the_bank_id;
	}

	void top_function(
		hls::stream<input_t> &input_stream,
		hls::stream<input_t> &output_stream,
		hls::stream<command_t> &command_stream
	) {
#pragma HLS PIPELINE
		command_t cmd_pkt;
		bool peek_enabled = false;
		bool discard_enabled = false;

		if (command_stream.read_nb(cmd_pkt)) {
			if (cmd_pkt.dest == 0 || cmd_pkt.dest == bank_id) {
				ap_uint<8> cmd = cmd_pkt.data;
				capture_enabled		= cmd.get_bit(BANK_BUFFER_FLAG_CAPTURE_ENABLE) 	    ? cmd.get_bit(BANK_BUFFER_FLAG_CAPTURE) 	: capture_enabled;
				peek_enabled		= cmd.get_bit(BANK_BUFFER_FLAG_PEEK_ENABLE) 		? cmd.get_bit(BANK_BUFFER_FLAG_PEEK)		: peek_enabled;
				discard_enabled 	= cmd.get_bit(BANK_BUFFER_FLAG_DISCARD_ENABLE)		? cmd.get_bit(BANK_BUFFER_FLAG_DISCARD)		: discard_enabled;
				transparent_enabled = cmd.get_bit(BANK_BUFFER_FLAG_TRANSPARENT_ENABLE)	? cmd.get_bit(BANK_BUFFER_FLAG_TRANSPARENT)	: transparent_enabled;
			}
		}


		if (transparent_enabled || capture_enabled) {
			capture(input_stream);
		}

		if (transparent_enabled || peek_enabled) {
			peek(output_stream);
			peek_enabled = false;
		}

		if (transparent_enabled || discard_enabled) {
			discard();
			discard_enabled = false;
		}
	}

};

template<class data_t>
struct Vote_buffer {
private:
	data_t pkt;
	bool engaged = false;
public:
	void top_function(hls::stream<data_t> &input_stream,
			hls::stream<data_t> &output_stream,
			bool &sig_engaged) {
		sig_engaged = engaged;
		if(!engaged) {
			input_stream >> pkt;
			engaged = true;
		} else {
			output_stream << pkt;
			engaged = false;
		}
		sig_engaged = engaged;
	}
};

template<int TID_MAX, int tid_size, int n_features, class input_s_t, class output_s_t>
struct Enumerator {
private:
	ap_uint<tid_size> next_tid = 0;
public:
	void top_function(
		hls::stream<input_s_t> &input_stream,
		hls::stream<output_s_t> &output_stream
	) {
		input_s_t in_pkt;
		input_stream >> in_pkt;

		output_s_t out_pkt;
		for (int i = 0; i < n_features; i++) {
			out_pkt.data[i] = in_pkt.data[i];
		}
		out_pkt.keep = in_pkt.keep;
		out_pkt.strb = in_pkt.strb;
		out_pkt.last = in_pkt.last;
		out_pkt.user = in_pkt.user;
		out_pkt.id   = next_tid;
		out_pkt.dest = in_pkt.dest;

		output_stream << out_pkt;

		next_tid = (next_tid + 1) % (TID_MAX + 1);
	}
};

template<int n_classes, class input_t, class output_t, class score_t, unsigned int max_parallel_samples>
struct Voting_station {

private:
	ap_uint<bitsizeof(fn_classes(n_classes))> class_id;
	score_t init_predict;
	score_t normalisation;
	ap_uint<bitsizeof(max_parallel_samples)>  in_buff[2] = {0, 0};
	ap_uint<1> curr_in_i = 0;
	score_t out_buff[2];
	ap_uint<1> curr_out_i = 0;
	bool empty = true;

public:
	Voting_station(ap_uint<bitsizeof(fn_classes(n_classes))> the_class_id, score_t the_init_predict, score_t the_normalisation) {
		class_id = the_class_id;
		init_predict = the_init_predict;
		out_buff[0] = out_buff[1] = init_predict;
		normalisation = the_normalisation;

	}
	void top_function(
		hls::stream<input_t> &input_stream,
		hls::stream<output_t> &output_stream
	) {
#pragma HLS PIPELINE
		input_t in;

		input_stream >> in;
		in_buff[curr_in_i] = in.id;
		curr_in_i = !curr_in_i;

		if (!in.last) {
			if (!empty && in_buff[curr_in_i] != in_buff[!curr_in_i]) {
				// Output previous accumulator
				output_t out;
				out.id = in_buff[!curr_in_i];
				out.data = out_buff[curr_out_i] * normalisation;
				out.last = true;
				out.keep = -1;
				out.strb = 0;
				out.dest = class_id;
				output_stream << out;
				// Switch accumulator
				curr_out_i = !curr_out_i;
				// (Re)Initialize accumulator
				out_buff[curr_out_i] = init_predict;
			}
			// Accumulate
			out_buff[curr_out_i] += in.data;
			empty = false;
		} else {
			// Output last
			output_t out;
			out.id = in_buff[!curr_in_i];
			out.data = out_buff[curr_out_i] * normalisation;
			out.last = true;
			out.keep = -1;
			out.strb = 0;
			out.dest = class_id;
			output_stream << out;

			// Reset
			in_buff[0] = in_buff[1] = 0;
			out_buff[0] = out_buff[1] = init_predict;
			empty = true;
		}
	}

};

template<int max_depth, class input_t, class score_t, class threshold_t>
constexpr int Tree<max_depth, input_t, score_t, threshold_t>::n_nodes;

template<int max_depth, class input_t, class score_t, class threshold_t>
constexpr int Tree<max_depth, input_t, score_t, threshold_t>::n_leaves;

}
#endif
