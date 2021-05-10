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

template<class input_t, unsigned int max_parallel_samples>
struct Bank_buffer {

private:
	input_t buffer[max_parallel_samples + 1];
	ap_uint<bitsizeof(max_parallel_samples + 1)> curr_in  = 0;
	ap_uint<bitsizeof(max_parallel_samples + 1)> curr_out = 0;
	bool empty = true;
	void capture(
		hls::stream<input_t> &input_stream
	) {
		if (empty || curr_in != curr_out) {
			input_stream >> buffer[curr_in];
			curr_in = (curr_in + 1) % (max_parallel_samples + 1);
			empty = false;
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
	void top_function(
		hls::stream<input_t> &input_stream,
		hls::stream<input_t> &output_stream,
		bool do_capture,
		bool do_peek,
		bool do_discard
	) {
		if (do_capture) {
			capture(input_stream);
		}

		if (do_peek) {
			peek(output_stream);
		}

		if (do_discard) {
			discard();
		}
	}

};

template<class input_t, class output_t, class score_t, unsigned int max_parallel_samples>
struct Voting_station {

private:
	score_t init_predict;
	score_t normalisation;
	ap_uint<bitsizeof(max_parallel_samples)>  in_buff[2] = {0, 0};
	ap_uint<1> curr_in_i = 0;
	score_t out_buff[2];
	ap_uint<1> curr_out_i = 0;

public:
	Voting_station(score_t the_init_predict, score_t the_normalisation) {
		init_predict = the_init_predict;
		out_buff[0] = out_buff[1] = init_predict;
		normalisation = the_normalisation;

	}
	void top_function(
		hls::stream<input_t> &input_stream,
		hls::stream<output_t> &output_stream
	) {
		input_t in;

		input_stream >> in;
		in_buff[curr_in_i] = in.id;
		curr_in_i = !curr_in_i;

		if (!in.last) {
			if (in_buff[curr_in_i] != in_buff[!curr_in_i]) {
				// Output previous accumulator
				output_t out;
				out.id = in_buff[!curr_in_i];
				out.data = out_buff[curr_out_i] * normalisation;
				output_stream << out;
				// Switch accumulator
				curr_out_i = !curr_out_i;
				// (Re)Initialize accumulator
				out_buff[curr_out_i] = init_predict;
			}
			// Accumulate
			out_buff[curr_out_i] += in.data;
		} else {
			// Output last
			output_t out;
			out.id = in_buff[!curr_in_i];
			out.data = out_buff[curr_out_i] * normalisation;
			output_stream << out;

			// Reset
			in_buff[0] = in_buff[1] = 0;
			out_buff[0] = out_buff[1] = init_predict;
		}
	}

};

template<int max_depth, class input_t, class score_t, class threshold_t>
constexpr int Tree<max_depth, input_t, score_t, threshold_t>::n_nodes;

template<int max_depth, class input_t, class score_t, class threshold_t>
constexpr int Tree<max_depth, input_t, score_t, threshold_t>::n_leaves;

}
#endif
