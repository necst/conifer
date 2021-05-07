#ifndef TREE_H__
#define TREE_H__

#include "hls_stream.h"
#include "parameters.h"
#include "SELECTORS.h"

void tree(
	hls::stream<input_arr_s_t> &input_stream,
	hls::stream<tree_score_s_t> &output_stream
);

#endif
