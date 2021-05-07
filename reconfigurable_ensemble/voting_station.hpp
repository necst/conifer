#ifndef VOTING_STATION_H__
#define VOTING_STATION_H__

#include "hls_stream.h"
#include "parameters.h"

void voting_station(
	hls::stream<input_s_t>  &input_score_stream,
	hls::stream<output_s_t> &output_score_stream
);

#endif
