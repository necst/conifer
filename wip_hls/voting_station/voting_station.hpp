#ifndef VOTING_STATION_HPP__
#define VOTING_STATION_HPP__

#include "hls_stream.h"
#include "parameters.hpp"
#include "utils.hpp"

void voting_station(
	hls::stream<input_s_t>  &input_score_stream,
	hls::stream<output_s_t> &output_score_stream
);

#endif
