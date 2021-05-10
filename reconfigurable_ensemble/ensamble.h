#ifndef IRIS_GB_H_
#define IRIS_GB_H_

#include "BDT.h"
#include "parameters.h"
#include "hls_stream.h"

void bank_buffer(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<input_arr_s_t> &output_stream,
	bool capture,
	bool peek,
	bool discard);

void tree_cl0_0(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl1_0(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl2_0(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl0_1(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl1_1(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl2_1(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl0_2(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl1_2(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl2_2(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl0_3(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl1_3(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl2_3(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl0_4(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl1_4(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl2_4(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl0_5(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl1_5(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl2_5(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl0_6(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl1_6(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl2_6(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl0_7(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl1_7(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl2_7(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl0_8(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl1_8(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl2_8(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl0_9(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl1_9(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl2_9(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl0_10(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl1_10(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl2_10(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl0_11(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl1_11(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl2_11(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl0_12(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl1_12(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl2_12(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl0_13(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl1_13(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl2_13(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl0_14(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl1_14(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl2_14(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl0_15(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl1_15(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl2_15(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl0_16(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl1_16(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl2_16(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl0_17(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl1_17(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl2_17(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl0_18(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl1_18(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl2_18(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl0_19(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl1_19(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl2_19(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl0_20(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl1_20(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl2_20(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl0_21(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl1_21(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl2_21(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl0_22(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl1_22(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl2_22(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl0_23(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl1_23(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl2_23(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl0_24(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl1_24(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl2_24(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl0_25(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl1_25(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl2_25(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl0_26(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl1_26(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl2_26(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl0_27(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl1_27(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl2_27(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl0_28(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl1_28(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl2_28(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl0_29(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl1_29(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void tree_cl2_29(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream);

void voting_station_cl0(
	hls::stream<tree_score_s_t>  &input_score_stream,
	hls::stream<class_score_s_t> &output_score_stream);

void voting_station_cl1(
	hls::stream<tree_score_s_t>  &input_score_stream,
	hls::stream<class_score_s_t> &output_score_stream);

void voting_station_cl2(
	hls::stream<tree_score_s_t>  &input_score_stream,
	hls::stream<class_score_s_t> &output_score_stream);

#endif
