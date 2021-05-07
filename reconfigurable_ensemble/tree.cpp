#ifndef TREE_CPP__
#define TREE_CPP__

#include "tree.h"
#include "BDT.h"

void tree(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[CURRENT_TREE][CURRENT_CLASS].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = input.dest;

	output_stream << output;

	return;
}

#endif
