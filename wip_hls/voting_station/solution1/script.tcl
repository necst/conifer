############################################################
## This file is generated automatically by Vitis HLS.
## Please DO NOT edit it.
## Copyright 1986-2020 Xilinx, Inc. All Rights Reserved.
############################################################
open_project voting_station
set_top voting_station
add_files voting_station/voting_station.hpp
add_files voting_station/voting_station.cpp
add_files voting_station/parameters.hpp
add_files voting_station/Tree.hpp
add_files -tb voting_station/testbench.cpp -cflags "-Wno-unknown-pragmas" -csimflags "-Wno-unknown-pragmas"
open_solution "solution1" -flow_target vivado
set_part {xczu3eg-sbva484-1-e}
create_clock -period 2 -name default
config_export -format ip_catalog -rtl verilog
source "./voting_station/solution1/directives.tcl"
csim_design
csynth_design
cosim_design -trace_level all
export_design -rtl verilog -format ip_catalog -description "TEST" -vendor "NECSTLab" -library "Tree Ensemble" -display_name "TEST Voting Station"
