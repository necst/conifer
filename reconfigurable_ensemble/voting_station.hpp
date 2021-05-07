#ifndef VOTING_STATION_H__
#define VOTING_STATION_H__

#include "hls_stream.h"
#include "parameters.h"
#include "SELECTORS.h"

void voting_station(
	hls::stream<tree_score_s_t>  &input_score_stream,
	hls::stream<class_score_s_t> &output_score_stream
);

#endif
