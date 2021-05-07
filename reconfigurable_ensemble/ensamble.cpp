#include "BDT.h"
#include "parameters.h"
#include "iris_GB.h"
void iris_GB(input_arr_t x, score_arr_t score, score_t tree_scores[BDT::fn_classes(n_classes) * n_trees]){
	#pragma HLS array_partition variable=x
	#pragma HLS array_partition variable=score
	#pragma HLS pipeline
	#pragma HLS unroll
	bdt.decision_function(x, score, tree_scores);
}