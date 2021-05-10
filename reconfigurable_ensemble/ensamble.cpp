#ifndef ENSEMBLE_CPP__
#define ENSEMBLE_CPP__

#include "BDT.h"
#include "parameters.h"
#include "ensamble.h"

void bank_buffer(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<input_arr_s_t> &output_stream,
	bool do_capture,
	bool do_peek,
	bool do_discard
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
#pragma HLS INTERFACE s_axilite register port=do_capture
#pragma HLS INTERFACE s_axilite register port=do_peek
#pragma HLS INTERFACE s_axilite register port=do_discard

	static BDT::Bank_buffer<input_arr_s_t, max_parallel_samples> bb;

	bb.top_function(input_stream, output_stream, do_capture, do_peek, do_discard);
}

void tree_cl0_0(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[0][0].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 0;

	output_stream << output;

	return;
}

void tree_cl1_0(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[0][1].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 1;

	output_stream << output;

	return;
}

void tree_cl2_0(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[0][2].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 2;

	output_stream << output;

	return;
}

void tree_cl0_1(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[1][0].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 0;

	output_stream << output;

	return;
}

void tree_cl1_1(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[1][1].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 1;

	output_stream << output;

	return;
}

void tree_cl2_1(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[1][2].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 2;

	output_stream << output;

	return;
}

void tree_cl0_2(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[2][0].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 0;

	output_stream << output;

	return;
}

void tree_cl1_2(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[2][1].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 1;

	output_stream << output;

	return;
}

void tree_cl2_2(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[2][2].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 2;

	output_stream << output;

	return;
}

void tree_cl0_3(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[3][0].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 0;

	output_stream << output;

	return;
}

void tree_cl1_3(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[3][1].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 1;

	output_stream << output;

	return;
}

void tree_cl2_3(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[3][2].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 2;

	output_stream << output;

	return;
}

void tree_cl0_4(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[4][0].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 0;

	output_stream << output;

	return;
}

void tree_cl1_4(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[4][1].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 1;

	output_stream << output;

	return;
}

void tree_cl2_4(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[4][2].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 2;

	output_stream << output;

	return;
}

void tree_cl0_5(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[5][0].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 0;

	output_stream << output;

	return;
}

void tree_cl1_5(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[5][1].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 1;

	output_stream << output;

	return;
}

void tree_cl2_5(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[5][2].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 2;

	output_stream << output;

	return;
}

void tree_cl0_6(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[6][0].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 0;

	output_stream << output;

	return;
}

void tree_cl1_6(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[6][1].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 1;

	output_stream << output;

	return;
}

void tree_cl2_6(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[6][2].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 2;

	output_stream << output;

	return;
}

void tree_cl0_7(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[7][0].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 0;

	output_stream << output;

	return;
}

void tree_cl1_7(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[7][1].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 1;

	output_stream << output;

	return;
}

void tree_cl2_7(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[7][2].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 2;

	output_stream << output;

	return;
}

void tree_cl0_8(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[8][0].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 0;

	output_stream << output;

	return;
}

void tree_cl1_8(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[8][1].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 1;

	output_stream << output;

	return;
}

void tree_cl2_8(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[8][2].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 2;

	output_stream << output;

	return;
}

void tree_cl0_9(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[9][0].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 0;

	output_stream << output;

	return;
}

void tree_cl1_9(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[9][1].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 1;

	output_stream << output;

	return;
}

void tree_cl2_9(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[9][2].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 2;

	output_stream << output;

	return;
}

void tree_cl0_10(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[10][0].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 0;

	output_stream << output;

	return;
}

void tree_cl1_10(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[10][1].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 1;

	output_stream << output;

	return;
}

void tree_cl2_10(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[10][2].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 2;

	output_stream << output;

	return;
}

void tree_cl0_11(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[11][0].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 0;

	output_stream << output;

	return;
}

void tree_cl1_11(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[11][1].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 1;

	output_stream << output;

	return;
}

void tree_cl2_11(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[11][2].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 2;

	output_stream << output;

	return;
}

void tree_cl0_12(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[12][0].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 0;

	output_stream << output;

	return;
}

void tree_cl1_12(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[12][1].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 1;

	output_stream << output;

	return;
}

void tree_cl2_12(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[12][2].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 2;

	output_stream << output;

	return;
}

void tree_cl0_13(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[13][0].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 0;

	output_stream << output;

	return;
}

void tree_cl1_13(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[13][1].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 1;

	output_stream << output;

	return;
}

void tree_cl2_13(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[13][2].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 2;

	output_stream << output;

	return;
}

void tree_cl0_14(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[14][0].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 0;

	output_stream << output;

	return;
}

void tree_cl1_14(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[14][1].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 1;

	output_stream << output;

	return;
}

void tree_cl2_14(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[14][2].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 2;

	output_stream << output;

	return;
}

void tree_cl0_15(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[15][0].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 0;

	output_stream << output;

	return;
}

void tree_cl1_15(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[15][1].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 1;

	output_stream << output;

	return;
}

void tree_cl2_15(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[15][2].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 2;

	output_stream << output;

	return;
}

void tree_cl0_16(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[16][0].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 0;

	output_stream << output;

	return;
}

void tree_cl1_16(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[16][1].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 1;

	output_stream << output;

	return;
}

void tree_cl2_16(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[16][2].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 2;

	output_stream << output;

	return;
}

void tree_cl0_17(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[17][0].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 0;

	output_stream << output;

	return;
}

void tree_cl1_17(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[17][1].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 1;

	output_stream << output;

	return;
}

void tree_cl2_17(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[17][2].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 2;

	output_stream << output;

	return;
}

void tree_cl0_18(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[18][0].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 0;

	output_stream << output;

	return;
}

void tree_cl1_18(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[18][1].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 1;

	output_stream << output;

	return;
}

void tree_cl2_18(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[18][2].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 2;

	output_stream << output;

	return;
}

void tree_cl0_19(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[19][0].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 0;

	output_stream << output;

	return;
}

void tree_cl1_19(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[19][1].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 1;

	output_stream << output;

	return;
}

void tree_cl2_19(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[19][2].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 2;

	output_stream << output;

	return;
}

void tree_cl0_20(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[20][0].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 0;

	output_stream << output;

	return;
}

void tree_cl1_20(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[20][1].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 1;

	output_stream << output;

	return;
}

void tree_cl2_20(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[20][2].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 2;

	output_stream << output;

	return;
}

void tree_cl0_21(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[21][0].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 0;

	output_stream << output;

	return;
}

void tree_cl1_21(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[21][1].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 1;

	output_stream << output;

	return;
}

void tree_cl2_21(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[21][2].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 2;

	output_stream << output;

	return;
}

void tree_cl0_22(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[22][0].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 0;

	output_stream << output;

	return;
}

void tree_cl1_22(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[22][1].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 1;

	output_stream << output;

	return;
}

void tree_cl2_22(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[22][2].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 2;

	output_stream << output;

	return;
}

void tree_cl0_23(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[23][0].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 0;

	output_stream << output;

	return;
}

void tree_cl1_23(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[23][1].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 1;

	output_stream << output;

	return;
}

void tree_cl2_23(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[23][2].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 2;

	output_stream << output;

	return;
}

void tree_cl0_24(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[24][0].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 0;

	output_stream << output;

	return;
}

void tree_cl1_24(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[24][1].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 1;

	output_stream << output;

	return;
}

void tree_cl2_24(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[24][2].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 2;

	output_stream << output;

	return;
}

void tree_cl0_25(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[25][0].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 0;

	output_stream << output;

	return;
}

void tree_cl1_25(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[25][1].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 1;

	output_stream << output;

	return;
}

void tree_cl2_25(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[25][2].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 2;

	output_stream << output;

	return;
}

void tree_cl0_26(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[26][0].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 0;

	output_stream << output;

	return;
}

void tree_cl1_26(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[26][1].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 1;

	output_stream << output;

	return;
}

void tree_cl2_26(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[26][2].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 2;

	output_stream << output;

	return;
}

void tree_cl0_27(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[27][0].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 0;

	output_stream << output;

	return;
}

void tree_cl1_27(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[27][1].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 1;

	output_stream << output;

	return;
}

void tree_cl2_27(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[27][2].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 2;

	output_stream << output;

	return;
}

void tree_cl0_28(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[28][0].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 0;

	output_stream << output;

	return;
}

void tree_cl1_28(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[28][1].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 1;

	output_stream << output;

	return;
}

void tree_cl2_28(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[28][2].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 2;

	output_stream << output;

	return;
}

void tree_cl0_29(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[29][0].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 0;

	output_stream << output;

	return;
}

void tree_cl1_29(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[29][1].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 1;

	output_stream << output;

	return;
}

void tree_cl2_29(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
) {
#pragma HLS INTERFACE axis register port=input_stream
#pragma HLS INTERFACE axis register port=output_stream
	input_arr_s_t input;
	input_stream >> input;

	auto output_data = bdt.trees[29][2].decision_function(input.data);

	tree_score_s_t output;
	output.data = output_data;
	output.id = input.id;
	output.dest = 2;

	output_stream << output;

	return;
}

void voting_station_cl0(
	hls::stream<tree_score_s_t>  &input_score_stream,
	hls::stream<class_score_s_t> &output_score_stream
) {

	static BDT::Voting_station<
		tree_score_s_t,
		class_score_s_t,
		score_t,
		max_parallel_samples> vs(bdt.init_predict[0], bdt.normalisation);

	vs.top_function(input_score_stream, output_score_stream);
}

void voting_station_cl1(
	hls::stream<tree_score_s_t>  &input_score_stream,
	hls::stream<class_score_s_t> &output_score_stream
) {

	static BDT::Voting_station<
		tree_score_s_t,
		class_score_s_t,
		score_t,
		max_parallel_samples> vs(bdt.init_predict[1], bdt.normalisation);

	vs.top_function(input_score_stream, output_score_stream);
}

void voting_station_cl2(
	hls::stream<tree_score_s_t>  &input_score_stream,
	hls::stream<class_score_s_t> &output_score_stream
) {

	static BDT::Voting_station<
		tree_score_s_t,
		class_score_s_t,
		score_t,
		max_parallel_samples> vs(bdt.init_predict[2], bdt.normalisation);

	vs.top_function(input_score_stream, output_score_stream);
}

#endif
