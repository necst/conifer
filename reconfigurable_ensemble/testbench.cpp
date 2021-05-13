//
//    rfnoc-hls-neuralnet: Vivado HLS code for neural-net building blocks
//
//    Copyright (C) 2017 EJ Kreinar
//
//    This program is free software: you can redistribute it and/or modify
//    it under the terms of the GNU General Public License as published by
//    the Free Software Foundation, either version 3 of the License, or
//    (at your option) any later version.
//
//    This program is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//    GNU General Public License for more details.
//
//    You should have received a copy of the GNU General Public License
//    along with this program.  If not, see <http://www.gnu.org/licenses/>.
//
#include <fstream>
#include <iostream>
#include <algorithm>
#include <vector>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include "ensamble.h"
#include "parameters.h"
#include "BDT.h"
#include "testbench_axis_interconnect.hpp"
#include "hls_stream.h"

#define CHECKPOINT 5000

template<typename pkt_t, typename data_t>
data_t tee(hls::stream<pkt_t> &in, hls::stream<pkt_t> &out) {
	pkt_t pkt;

	in >> pkt;
	out << pkt;

	return pkt.data;
}

int main(int argc, char **argv)
{
  //load input data from text file
  std::ifstream fin("tb_data/tb_input_features.dat");

#ifdef RTL_SIM
  std::string RESULTS_LOG = "tb_data/cosim_results.log";
  std::string VERBOSE_LOG = "tb_data/cosim_tree_results.log";
#else
  std::string RESULTS_LOG = "tb_data/csim_results.log";
  std::string VERBOSE_LOG = "tb_data/csim_tree_results.log";
#endif
  std::ofstream fout(RESULTS_LOG);
  std::ofstream ftrees(VERBOSE_LOG);

  std::string iline;
  std::string pline;
  int e = 0;
  int curr_id = max_parallel_samples - 1;

  if (fin.is_open()) {
	static hls::stream<input_arr_s_t> sample_stream[1];
	static hls::stream<input_arr_s_t> bank_stream[1];
	static hls::stream<input_arr_s_t> tree_stream[n_trees * n_classes];
	static hls::stream<tree_score_s_t> aux_score_stream[n_trees * n_classes];
	static hls::stream<tree_score_s_t> score_stream[n_trees * n_classes];
	static hls::stream<tree_score_s_t> in_class_stream[n_classes];
	static hls::stream<class_score_s_t> out_class_stream[n_classes];

    while ( std::getline(fin,iline) ) {
      if (e % CHECKPOINT == 0) std::cout << "Processing input " << e << std::endl;
      e++;
      char* cstr=const_cast<char*>(iline.c_str());
      char* current;
      std::vector<float> in;
      current=strtok(cstr," ");
      while(current!=NULL) {
        in.push_back(atof(current));
        current=strtok(NULL," ");
      }

      //hls-fpga-machine-learning insert data
      input_arr_s_t in_pkt;
      std::vector<float>::const_iterator in_begin = in.cbegin();
      std::vector<float>::const_iterator in_end;
      in_end = in_begin + (4);
      std::copy(in_begin, in_end, in_pkt.data);
      in_begin = in_end;
      score_arr_t score{};
      score_t tree_scores[BDT::fn_classes(n_classes) * n_trees]{};
      std::fill_n(score, 3, 0.);
      curr_id = (curr_id + 1) % max_parallel_samples;
      in_pkt.id = curr_id;

      int dbg_in_pkt_id = in_pkt.id.to_int();

      sample_stream[0] << in_pkt;

      //hls-fpga-machine-learning insert top-level-function
      bank_buffer(sample_stream[0], bank_stream[0], true, true, true);
      axis_crossbar<input_arr_s_t, 1, n_trees * n_classes>(bank_stream, tree_stream);
      tree_cl0_0(tree_stream[0 * n_classes + 0], aux_score_stream[0 * n_classes + 0]);
      tree_cl1_0(tree_stream[0 * n_classes + 1], aux_score_stream[0 * n_classes + 1]);
      tree_cl2_0(tree_stream[0 * n_classes + 2], aux_score_stream[0 * n_classes + 2]);
      tree_cl0_1(tree_stream[1 * n_classes + 0], aux_score_stream[1 * n_classes + 0]);
      tree_cl1_1(tree_stream[1 * n_classes + 1], aux_score_stream[1 * n_classes + 1]);
      tree_cl2_1(tree_stream[1 * n_classes + 2], aux_score_stream[1 * n_classes + 2]);
      tree_cl0_2(tree_stream[2 * n_classes + 0], aux_score_stream[2 * n_classes + 0]);
      tree_cl1_2(tree_stream[2 * n_classes + 1], aux_score_stream[2 * n_classes + 1]);
      tree_cl2_2(tree_stream[2 * n_classes + 2], aux_score_stream[2 * n_classes + 2]);
      tree_cl0_3(tree_stream[3 * n_classes + 0], aux_score_stream[3 * n_classes + 0]);
      tree_cl1_3(tree_stream[3 * n_classes + 1], aux_score_stream[3 * n_classes + 1]);
      tree_cl2_3(tree_stream[3 * n_classes + 2], aux_score_stream[3 * n_classes + 2]);
      tree_cl0_4(tree_stream[4 * n_classes + 0], aux_score_stream[4 * n_classes + 0]);
      tree_cl1_4(tree_stream[4 * n_classes + 1], aux_score_stream[4 * n_classes + 1]);
      tree_cl2_4(tree_stream[4 * n_classes + 2], aux_score_stream[4 * n_classes + 2]);
      tree_cl0_5(tree_stream[5 * n_classes + 0], aux_score_stream[5 * n_classes + 0]);
      tree_cl1_5(tree_stream[5 * n_classes + 1], aux_score_stream[5 * n_classes + 1]);
      tree_cl2_5(tree_stream[5 * n_classes + 2], aux_score_stream[5 * n_classes + 2]);
      tree_cl0_6(tree_stream[6 * n_classes + 0], aux_score_stream[6 * n_classes + 0]);
      tree_cl1_6(tree_stream[6 * n_classes + 1], aux_score_stream[6 * n_classes + 1]);
      tree_cl2_6(tree_stream[6 * n_classes + 2], aux_score_stream[6 * n_classes + 2]);
      tree_cl0_7(tree_stream[7 * n_classes + 0], aux_score_stream[7 * n_classes + 0]);
      tree_cl1_7(tree_stream[7 * n_classes + 1], aux_score_stream[7 * n_classes + 1]);
      tree_cl2_7(tree_stream[7 * n_classes + 2], aux_score_stream[7 * n_classes + 2]);
      tree_cl0_8(tree_stream[8 * n_classes + 0], aux_score_stream[8 * n_classes + 0]);
      tree_cl1_8(tree_stream[8 * n_classes + 1], aux_score_stream[8 * n_classes + 1]);
      tree_cl2_8(tree_stream[8 * n_classes + 2], aux_score_stream[8 * n_classes + 2]);
      tree_cl0_9(tree_stream[9 * n_classes + 0], aux_score_stream[9 * n_classes + 0]);
      tree_cl1_9(tree_stream[9 * n_classes + 1], aux_score_stream[9 * n_classes + 1]);
      tree_cl2_9(tree_stream[9 * n_classes + 2], aux_score_stream[9 * n_classes + 2]);
      tree_cl0_10(tree_stream[10 * n_classes + 0], aux_score_stream[10 * n_classes + 0]);
      tree_cl1_10(tree_stream[10 * n_classes + 1], aux_score_stream[10 * n_classes + 1]);
      tree_cl2_10(tree_stream[10 * n_classes + 2], aux_score_stream[10 * n_classes + 2]);
      tree_cl0_11(tree_stream[11 * n_classes + 0], aux_score_stream[11 * n_classes + 0]);
      tree_cl1_11(tree_stream[11 * n_classes + 1], aux_score_stream[11 * n_classes + 1]);
      tree_cl2_11(tree_stream[11 * n_classes + 2], aux_score_stream[11 * n_classes + 2]);
      tree_cl0_12(tree_stream[12 * n_classes + 0], aux_score_stream[12 * n_classes + 0]);
      tree_cl1_12(tree_stream[12 * n_classes + 1], aux_score_stream[12 * n_classes + 1]);
      tree_cl2_12(tree_stream[12 * n_classes + 2], aux_score_stream[12 * n_classes + 2]);
      tree_cl0_13(tree_stream[13 * n_classes + 0], aux_score_stream[13 * n_classes + 0]);
      tree_cl1_13(tree_stream[13 * n_classes + 1], aux_score_stream[13 * n_classes + 1]);
      tree_cl2_13(tree_stream[13 * n_classes + 2], aux_score_stream[13 * n_classes + 2]);
      tree_cl0_14(tree_stream[14 * n_classes + 0], aux_score_stream[14 * n_classes + 0]);
      tree_cl1_14(tree_stream[14 * n_classes + 1], aux_score_stream[14 * n_classes + 1]);
      tree_cl2_14(tree_stream[14 * n_classes + 2], aux_score_stream[14 * n_classes + 2]);
      tree_cl0_15(tree_stream[15 * n_classes + 0], aux_score_stream[15 * n_classes + 0]);
      tree_cl1_15(tree_stream[15 * n_classes + 1], aux_score_stream[15 * n_classes + 1]);
      tree_cl2_15(tree_stream[15 * n_classes + 2], aux_score_stream[15 * n_classes + 2]);
      tree_cl0_16(tree_stream[16 * n_classes + 0], aux_score_stream[16 * n_classes + 0]);
      tree_cl1_16(tree_stream[16 * n_classes + 1], aux_score_stream[16 * n_classes + 1]);
      tree_cl2_16(tree_stream[16 * n_classes + 2], aux_score_stream[16 * n_classes + 2]);
      tree_cl0_17(tree_stream[17 * n_classes + 0], aux_score_stream[17 * n_classes + 0]);
      tree_cl1_17(tree_stream[17 * n_classes + 1], aux_score_stream[17 * n_classes + 1]);
      tree_cl2_17(tree_stream[17 * n_classes + 2], aux_score_stream[17 * n_classes + 2]);
      tree_cl0_18(tree_stream[18 * n_classes + 0], aux_score_stream[18 * n_classes + 0]);
      tree_cl1_18(tree_stream[18 * n_classes + 1], aux_score_stream[18 * n_classes + 1]);
      tree_cl2_18(tree_stream[18 * n_classes + 2], aux_score_stream[18 * n_classes + 2]);
      tree_cl0_19(tree_stream[19 * n_classes + 0], aux_score_stream[19 * n_classes + 0]);
      tree_cl1_19(tree_stream[19 * n_classes + 1], aux_score_stream[19 * n_classes + 1]);
      tree_cl2_19(tree_stream[19 * n_classes + 2], aux_score_stream[19 * n_classes + 2]);
      tree_cl0_20(tree_stream[20 * n_classes + 0], aux_score_stream[20 * n_classes + 0]);
      tree_cl1_20(tree_stream[20 * n_classes + 1], aux_score_stream[20 * n_classes + 1]);
      tree_cl2_20(tree_stream[20 * n_classes + 2], aux_score_stream[20 * n_classes + 2]);
      tree_cl0_21(tree_stream[21 * n_classes + 0], aux_score_stream[21 * n_classes + 0]);
      tree_cl1_21(tree_stream[21 * n_classes + 1], aux_score_stream[21 * n_classes + 1]);
      tree_cl2_21(tree_stream[21 * n_classes + 2], aux_score_stream[21 * n_classes + 2]);
      tree_cl0_22(tree_stream[22 * n_classes + 0], aux_score_stream[22 * n_classes + 0]);
      tree_cl1_22(tree_stream[22 * n_classes + 1], aux_score_stream[22 * n_classes + 1]);
      tree_cl2_22(tree_stream[22 * n_classes + 2], aux_score_stream[22 * n_classes + 2]);
      tree_cl0_23(tree_stream[23 * n_classes + 0], aux_score_stream[23 * n_classes + 0]);
      tree_cl1_23(tree_stream[23 * n_classes + 1], aux_score_stream[23 * n_classes + 1]);
      tree_cl2_23(tree_stream[23 * n_classes + 2], aux_score_stream[23 * n_classes + 2]);
      tree_cl0_24(tree_stream[24 * n_classes + 0], aux_score_stream[24 * n_classes + 0]);
      tree_cl1_24(tree_stream[24 * n_classes + 1], aux_score_stream[24 * n_classes + 1]);
      tree_cl2_24(tree_stream[24 * n_classes + 2], aux_score_stream[24 * n_classes + 2]);
      tree_cl0_25(tree_stream[25 * n_classes + 0], aux_score_stream[25 * n_classes + 0]);
      tree_cl1_25(tree_stream[25 * n_classes + 1], aux_score_stream[25 * n_classes + 1]);
      tree_cl2_25(tree_stream[25 * n_classes + 2], aux_score_stream[25 * n_classes + 2]);
      tree_cl0_26(tree_stream[26 * n_classes + 0], aux_score_stream[26 * n_classes + 0]);
      tree_cl1_26(tree_stream[26 * n_classes + 1], aux_score_stream[26 * n_classes + 1]);
      tree_cl2_26(tree_stream[26 * n_classes + 2], aux_score_stream[26 * n_classes + 2]);
      tree_cl0_27(tree_stream[27 * n_classes + 0], aux_score_stream[27 * n_classes + 0]);
      tree_cl1_27(tree_stream[27 * n_classes + 1], aux_score_stream[27 * n_classes + 1]);
      tree_cl2_27(tree_stream[27 * n_classes + 2], aux_score_stream[27 * n_classes + 2]);
      tree_cl0_28(tree_stream[28 * n_classes + 0], aux_score_stream[28 * n_classes + 0]);
      tree_cl1_28(tree_stream[28 * n_classes + 1], aux_score_stream[28 * n_classes + 1]);
      tree_cl2_28(tree_stream[28 * n_classes + 2], aux_score_stream[28 * n_classes + 2]);
      tree_cl0_29(tree_stream[29 * n_classes + 0], aux_score_stream[29 * n_classes + 0]);
      tree_cl1_29(tree_stream[29 * n_classes + 1], aux_score_stream[29 * n_classes + 1]);
      tree_cl2_29(tree_stream[29 * n_classes + 2], aux_score_stream[29 * n_classes + 2]);
      tree_scores[0 * n_classes + 0] = tee<tree_score_s_t, score_t>(aux_score_stream[0 * n_classes + 0], score_stream[0 * n_classes + 0]);
      tree_scores[0 * n_classes + 1] = tee<tree_score_s_t, score_t>(aux_score_stream[0 * n_classes + 1], score_stream[0 * n_classes + 1]);
      tree_scores[0 * n_classes + 2] = tee<tree_score_s_t, score_t>(aux_score_stream[0 * n_classes + 2], score_stream[0 * n_classes + 2]);
      tree_scores[1 * n_classes + 0] = tee<tree_score_s_t, score_t>(aux_score_stream[1 * n_classes + 0], score_stream[1 * n_classes + 0]);
      tree_scores[1 * n_classes + 1] = tee<tree_score_s_t, score_t>(aux_score_stream[1 * n_classes + 1], score_stream[1 * n_classes + 1]);
      tree_scores[1 * n_classes + 2] = tee<tree_score_s_t, score_t>(aux_score_stream[1 * n_classes + 2], score_stream[1 * n_classes + 2]);
      tree_scores[2 * n_classes + 0] = tee<tree_score_s_t, score_t>(aux_score_stream[2 * n_classes + 0], score_stream[2 * n_classes + 0]);
      tree_scores[2 * n_classes + 1] = tee<tree_score_s_t, score_t>(aux_score_stream[2 * n_classes + 1], score_stream[2 * n_classes + 1]);
      tree_scores[2 * n_classes + 2] = tee<tree_score_s_t, score_t>(aux_score_stream[2 * n_classes + 2], score_stream[2 * n_classes + 2]);
      tree_scores[3 * n_classes + 0] = tee<tree_score_s_t, score_t>(aux_score_stream[3 * n_classes + 0], score_stream[3 * n_classes + 0]);
      tree_scores[3 * n_classes + 1] = tee<tree_score_s_t, score_t>(aux_score_stream[3 * n_classes + 1], score_stream[3 * n_classes + 1]);
      tree_scores[3 * n_classes + 2] = tee<tree_score_s_t, score_t>(aux_score_stream[3 * n_classes + 2], score_stream[3 * n_classes + 2]);
      tree_scores[4 * n_classes + 0] = tee<tree_score_s_t, score_t>(aux_score_stream[4 * n_classes + 0], score_stream[4 * n_classes + 0]);
      tree_scores[4 * n_classes + 1] = tee<tree_score_s_t, score_t>(aux_score_stream[4 * n_classes + 1], score_stream[4 * n_classes + 1]);
      tree_scores[4 * n_classes + 2] = tee<tree_score_s_t, score_t>(aux_score_stream[4 * n_classes + 2], score_stream[4 * n_classes + 2]);
      tree_scores[5 * n_classes + 0] = tee<tree_score_s_t, score_t>(aux_score_stream[5 * n_classes + 0], score_stream[5 * n_classes + 0]);
      tree_scores[5 * n_classes + 1] = tee<tree_score_s_t, score_t>(aux_score_stream[5 * n_classes + 1], score_stream[5 * n_classes + 1]);
      tree_scores[5 * n_classes + 2] = tee<tree_score_s_t, score_t>(aux_score_stream[5 * n_classes + 2], score_stream[5 * n_classes + 2]);
      tree_scores[6 * n_classes + 0] = tee<tree_score_s_t, score_t>(aux_score_stream[6 * n_classes + 0], score_stream[6 * n_classes + 0]);
      tree_scores[6 * n_classes + 1] = tee<tree_score_s_t, score_t>(aux_score_stream[6 * n_classes + 1], score_stream[6 * n_classes + 1]);
      tree_scores[6 * n_classes + 2] = tee<tree_score_s_t, score_t>(aux_score_stream[6 * n_classes + 2], score_stream[6 * n_classes + 2]);
      tree_scores[7 * n_classes + 0] = tee<tree_score_s_t, score_t>(aux_score_stream[7 * n_classes + 0], score_stream[7 * n_classes + 0]);
      tree_scores[7 * n_classes + 1] = tee<tree_score_s_t, score_t>(aux_score_stream[7 * n_classes + 1], score_stream[7 * n_classes + 1]);
      tree_scores[7 * n_classes + 2] = tee<tree_score_s_t, score_t>(aux_score_stream[7 * n_classes + 2], score_stream[7 * n_classes + 2]);
      tree_scores[8 * n_classes + 0] = tee<tree_score_s_t, score_t>(aux_score_stream[8 * n_classes + 0], score_stream[8 * n_classes + 0]);
      tree_scores[8 * n_classes + 1] = tee<tree_score_s_t, score_t>(aux_score_stream[8 * n_classes + 1], score_stream[8 * n_classes + 1]);
      tree_scores[8 * n_classes + 2] = tee<tree_score_s_t, score_t>(aux_score_stream[8 * n_classes + 2], score_stream[8 * n_classes + 2]);
      tree_scores[9 * n_classes + 0] = tee<tree_score_s_t, score_t>(aux_score_stream[9 * n_classes + 0], score_stream[9 * n_classes + 0]);
      tree_scores[9 * n_classes + 1] = tee<tree_score_s_t, score_t>(aux_score_stream[9 * n_classes + 1], score_stream[9 * n_classes + 1]);
      tree_scores[9 * n_classes + 2] = tee<tree_score_s_t, score_t>(aux_score_stream[9 * n_classes + 2], score_stream[9 * n_classes + 2]);
      tree_scores[10 * n_classes + 0] = tee<tree_score_s_t, score_t>(aux_score_stream[10 * n_classes + 0], score_stream[10 * n_classes + 0]);
      tree_scores[10 * n_classes + 1] = tee<tree_score_s_t, score_t>(aux_score_stream[10 * n_classes + 1], score_stream[10 * n_classes + 1]);
      tree_scores[10 * n_classes + 2] = tee<tree_score_s_t, score_t>(aux_score_stream[10 * n_classes + 2], score_stream[10 * n_classes + 2]);
      tree_scores[11 * n_classes + 0] = tee<tree_score_s_t, score_t>(aux_score_stream[11 * n_classes + 0], score_stream[11 * n_classes + 0]);
      tree_scores[11 * n_classes + 1] = tee<tree_score_s_t, score_t>(aux_score_stream[11 * n_classes + 1], score_stream[11 * n_classes + 1]);
      tree_scores[11 * n_classes + 2] = tee<tree_score_s_t, score_t>(aux_score_stream[11 * n_classes + 2], score_stream[11 * n_classes + 2]);
      tree_scores[12 * n_classes + 0] = tee<tree_score_s_t, score_t>(aux_score_stream[12 * n_classes + 0], score_stream[12 * n_classes + 0]);
      tree_scores[12 * n_classes + 1] = tee<tree_score_s_t, score_t>(aux_score_stream[12 * n_classes + 1], score_stream[12 * n_classes + 1]);
      tree_scores[12 * n_classes + 2] = tee<tree_score_s_t, score_t>(aux_score_stream[12 * n_classes + 2], score_stream[12 * n_classes + 2]);
      tree_scores[13 * n_classes + 0] = tee<tree_score_s_t, score_t>(aux_score_stream[13 * n_classes + 0], score_stream[13 * n_classes + 0]);
      tree_scores[13 * n_classes + 1] = tee<tree_score_s_t, score_t>(aux_score_stream[13 * n_classes + 1], score_stream[13 * n_classes + 1]);
      tree_scores[13 * n_classes + 2] = tee<tree_score_s_t, score_t>(aux_score_stream[13 * n_classes + 2], score_stream[13 * n_classes + 2]);
      tree_scores[14 * n_classes + 0] = tee<tree_score_s_t, score_t>(aux_score_stream[14 * n_classes + 0], score_stream[14 * n_classes + 0]);
      tree_scores[14 * n_classes + 1] = tee<tree_score_s_t, score_t>(aux_score_stream[14 * n_classes + 1], score_stream[14 * n_classes + 1]);
      tree_scores[14 * n_classes + 2] = tee<tree_score_s_t, score_t>(aux_score_stream[14 * n_classes + 2], score_stream[14 * n_classes + 2]);
      tree_scores[15 * n_classes + 0] = tee<tree_score_s_t, score_t>(aux_score_stream[15 * n_classes + 0], score_stream[15 * n_classes + 0]);
      tree_scores[15 * n_classes + 1] = tee<tree_score_s_t, score_t>(aux_score_stream[15 * n_classes + 1], score_stream[15 * n_classes + 1]);
      tree_scores[15 * n_classes + 2] = tee<tree_score_s_t, score_t>(aux_score_stream[15 * n_classes + 2], score_stream[15 * n_classes + 2]);
      tree_scores[16 * n_classes + 0] = tee<tree_score_s_t, score_t>(aux_score_stream[16 * n_classes + 0], score_stream[16 * n_classes + 0]);
      tree_scores[16 * n_classes + 1] = tee<tree_score_s_t, score_t>(aux_score_stream[16 * n_classes + 1], score_stream[16 * n_classes + 1]);
      tree_scores[16 * n_classes + 2] = tee<tree_score_s_t, score_t>(aux_score_stream[16 * n_classes + 2], score_stream[16 * n_classes + 2]);
      tree_scores[17 * n_classes + 0] = tee<tree_score_s_t, score_t>(aux_score_stream[17 * n_classes + 0], score_stream[17 * n_classes + 0]);
      tree_scores[17 * n_classes + 1] = tee<tree_score_s_t, score_t>(aux_score_stream[17 * n_classes + 1], score_stream[17 * n_classes + 1]);
      tree_scores[17 * n_classes + 2] = tee<tree_score_s_t, score_t>(aux_score_stream[17 * n_classes + 2], score_stream[17 * n_classes + 2]);
      tree_scores[18 * n_classes + 0] = tee<tree_score_s_t, score_t>(aux_score_stream[18 * n_classes + 0], score_stream[18 * n_classes + 0]);
      tree_scores[18 * n_classes + 1] = tee<tree_score_s_t, score_t>(aux_score_stream[18 * n_classes + 1], score_stream[18 * n_classes + 1]);
      tree_scores[18 * n_classes + 2] = tee<tree_score_s_t, score_t>(aux_score_stream[18 * n_classes + 2], score_stream[18 * n_classes + 2]);
      tree_scores[19 * n_classes + 0] = tee<tree_score_s_t, score_t>(aux_score_stream[19 * n_classes + 0], score_stream[19 * n_classes + 0]);
      tree_scores[19 * n_classes + 1] = tee<tree_score_s_t, score_t>(aux_score_stream[19 * n_classes + 1], score_stream[19 * n_classes + 1]);
      tree_scores[19 * n_classes + 2] = tee<tree_score_s_t, score_t>(aux_score_stream[19 * n_classes + 2], score_stream[19 * n_classes + 2]);
      tree_scores[20 * n_classes + 0] = tee<tree_score_s_t, score_t>(aux_score_stream[20 * n_classes + 0], score_stream[20 * n_classes + 0]);
      tree_scores[20 * n_classes + 1] = tee<tree_score_s_t, score_t>(aux_score_stream[20 * n_classes + 1], score_stream[20 * n_classes + 1]);
      tree_scores[20 * n_classes + 2] = tee<tree_score_s_t, score_t>(aux_score_stream[20 * n_classes + 2], score_stream[20 * n_classes + 2]);
      tree_scores[21 * n_classes + 0] = tee<tree_score_s_t, score_t>(aux_score_stream[21 * n_classes + 0], score_stream[21 * n_classes + 0]);
      tree_scores[21 * n_classes + 1] = tee<tree_score_s_t, score_t>(aux_score_stream[21 * n_classes + 1], score_stream[21 * n_classes + 1]);
      tree_scores[21 * n_classes + 2] = tee<tree_score_s_t, score_t>(aux_score_stream[21 * n_classes + 2], score_stream[21 * n_classes + 2]);
      tree_scores[22 * n_classes + 0] = tee<tree_score_s_t, score_t>(aux_score_stream[22 * n_classes + 0], score_stream[22 * n_classes + 0]);
      tree_scores[22 * n_classes + 1] = tee<tree_score_s_t, score_t>(aux_score_stream[22 * n_classes + 1], score_stream[22 * n_classes + 1]);
      tree_scores[22 * n_classes + 2] = tee<tree_score_s_t, score_t>(aux_score_stream[22 * n_classes + 2], score_stream[22 * n_classes + 2]);
      tree_scores[23 * n_classes + 0] = tee<tree_score_s_t, score_t>(aux_score_stream[23 * n_classes + 0], score_stream[23 * n_classes + 0]);
      tree_scores[23 * n_classes + 1] = tee<tree_score_s_t, score_t>(aux_score_stream[23 * n_classes + 1], score_stream[23 * n_classes + 1]);
      tree_scores[23 * n_classes + 2] = tee<tree_score_s_t, score_t>(aux_score_stream[23 * n_classes + 2], score_stream[23 * n_classes + 2]);
      tree_scores[24 * n_classes + 0] = tee<tree_score_s_t, score_t>(aux_score_stream[24 * n_classes + 0], score_stream[24 * n_classes + 0]);
      tree_scores[24 * n_classes + 1] = tee<tree_score_s_t, score_t>(aux_score_stream[24 * n_classes + 1], score_stream[24 * n_classes + 1]);
      tree_scores[24 * n_classes + 2] = tee<tree_score_s_t, score_t>(aux_score_stream[24 * n_classes + 2], score_stream[24 * n_classes + 2]);
      tree_scores[25 * n_classes + 0] = tee<tree_score_s_t, score_t>(aux_score_stream[25 * n_classes + 0], score_stream[25 * n_classes + 0]);
      tree_scores[25 * n_classes + 1] = tee<tree_score_s_t, score_t>(aux_score_stream[25 * n_classes + 1], score_stream[25 * n_classes + 1]);
      tree_scores[25 * n_classes + 2] = tee<tree_score_s_t, score_t>(aux_score_stream[25 * n_classes + 2], score_stream[25 * n_classes + 2]);
      tree_scores[26 * n_classes + 0] = tee<tree_score_s_t, score_t>(aux_score_stream[26 * n_classes + 0], score_stream[26 * n_classes + 0]);
      tree_scores[26 * n_classes + 1] = tee<tree_score_s_t, score_t>(aux_score_stream[26 * n_classes + 1], score_stream[26 * n_classes + 1]);
      tree_scores[26 * n_classes + 2] = tee<tree_score_s_t, score_t>(aux_score_stream[26 * n_classes + 2], score_stream[26 * n_classes + 2]);
      tree_scores[27 * n_classes + 0] = tee<tree_score_s_t, score_t>(aux_score_stream[27 * n_classes + 0], score_stream[27 * n_classes + 0]);
      tree_scores[27 * n_classes + 1] = tee<tree_score_s_t, score_t>(aux_score_stream[27 * n_classes + 1], score_stream[27 * n_classes + 1]);
      tree_scores[27 * n_classes + 2] = tee<tree_score_s_t, score_t>(aux_score_stream[27 * n_classes + 2], score_stream[27 * n_classes + 2]);
      tree_scores[28 * n_classes + 0] = tee<tree_score_s_t, score_t>(aux_score_stream[28 * n_classes + 0], score_stream[28 * n_classes + 0]);
      tree_scores[28 * n_classes + 1] = tee<tree_score_s_t, score_t>(aux_score_stream[28 * n_classes + 1], score_stream[28 * n_classes + 1]);
      tree_scores[28 * n_classes + 2] = tee<tree_score_s_t, score_t>(aux_score_stream[28 * n_classes + 2], score_stream[28 * n_classes + 2]);
      tree_scores[29 * n_classes + 0] = tee<tree_score_s_t, score_t>(aux_score_stream[29 * n_classes + 0], score_stream[29 * n_classes + 0]);
      tree_scores[29 * n_classes + 1] = tee<tree_score_s_t, score_t>(aux_score_stream[29 * n_classes + 1], score_stream[29 * n_classes + 1]);
      tree_scores[29 * n_classes + 2] = tee<tree_score_s_t, score_t>(aux_score_stream[29 * n_classes + 2], score_stream[29 * n_classes + 2]);
      axis_crossbar<tree_score_s_t, n_trees * n_classes, n_classes>(score_stream, in_class_stream);
      while(!in_class_stream[0].empty()) {
		  voting_station_cl0(in_class_stream[0], out_class_stream[0]);
      }
      while(!in_class_stream[1].empty()) {
		  voting_station_cl1(in_class_stream[1], out_class_stream[1]);
      }
      while(!in_class_stream[2].empty()) {
		  voting_station_cl2(in_class_stream[2], out_class_stream[2]);
	  }

      for(int  i = 0; i < n_trees; i++){
          for(int j = 0; j < BDT::fn_classes(n_classes); j++){
            ftrees << tree_scores[i * BDT::fn_classes(n_classes) + j] << " ";
          }
      }
      ftrees << std::endl;
    }

    // Flush the voting stations
    for (int i = 0; i < BDT::fn_classes(n_classes); i++) {
    	tree_score_s_t pkt;
		pkt.last = true;
    	in_class_stream[i] << pkt;
    }

    voting_station_cl0(in_class_stream[0], out_class_stream[0]);
    voting_station_cl1(in_class_stream[1], out_class_stream[1]);
    voting_station_cl2(in_class_stream[2], out_class_stream[2]);

    while(
		!out_class_stream[0].empty() &&
		!out_class_stream[1].empty() &&
		!out_class_stream[2].empty()
	) {

      for(int i = 0; i < BDT::fn_classes(n_classes); i++){
    	class_score_s_t score;
    	if (!out_class_stream[i].empty()) {
			out_class_stream[i] >> score;
			fout << score.data << " ";
    	} else {
    		fout << "NaN ";
    	}
      }
      fout << std::endl;
    }
    fin.close();
  } else {
	std::cout << "CRITICAL: Unable to open input file." << std::endl;
	return -1;
  }

  fout.close();
  ftrees.close();
  std::cout << "INFO: Saved inference results to file: " << RESULTS_LOG << std::endl;

  return 0;
}

