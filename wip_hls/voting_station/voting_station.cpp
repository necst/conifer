#ifndef VOTING_STATION_CPP__
#define VOTING_STATION_CPP__

#include "voting_station.hpp"

void voting_station(
	hls::stream<input_s_t>  &input_score_stream,
	hls::stream<output_s_t> &output_score_stream
) {
#pragma HLS INTERFACE ap_ctrl_none port=return
#pragma HLS INTERFACE axis register port=input_score_stream
#pragma HLS INTERFACE axis register port=output_score_stream

	static ap_uint<bitsizeof(max_parallelism)>  in_buff[2] = {0, 0};
	static ap_uint<1> curr_in_i = 0;

	static score_t out_buff[2] = {init_predict, init_predict};
	static ap_uint<1> curr_out_i = 0;

	input_s_t in;

	input_score_stream >> in;
	in_buff[curr_in_i] = in.id;
	curr_in_i = !curr_in_i;

	if (!in.last) {
		if (in_buff[curr_in_i] != in_buff[!curr_in_i]) {
			// Output previous accumulator
			output_s_t out;
			out.id = in_buff[!curr_in_i];
			out.data = out_buff[curr_out_i] * normalization;
			output_score_stream << out;
			// Switch accumulator
			curr_out_i = !curr_out_i;
			// (Re)Initialize accumulator
			out_buff[curr_out_i] = init_predict;
		}
		// Accumulate
		out_buff[curr_out_i] += in.data;
	} else {
		// Output last
		output_s_t out;
		out.id = in_buff[!curr_in_i];
		out.data = out_buff[curr_out_i] * normalization;
		output_score_stream << out;

		// Reset
		in_buff[0] = in_buff[1] = 0;
		out_buff[0] = out_buff[1] = init_predict;
	}

	return;

}

#endif
