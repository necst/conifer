#ifndef PARAMETERS_HPP__
#define PARAMETERS_HPP__

#include "ap_axi_sdata.h"
#include "ap_fixed.h"
#include "Tree.hpp"

constexpr int max_parallelism = 2;
static const int n_trees = 30;
static const int n_classes = 3;
typedef ap_fixed<18,8> score_t;

typedef hls::axis<score_t, 0, bitsizeof(max_parallelism), bitsizeof(n_classes)> input_s_t;
typedef hls::axis<score_t, 0, bitsizeof(max_parallelism), 0> output_s_t;

static const ap_fixed<18,8> init_predict = -1.0986122886681098;
static const ap_fixed<18, 8> normalization = 1;

#endif
