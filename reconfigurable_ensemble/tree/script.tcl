############################################################
## This file is generated automatically by Vitis HLS.
## Please DO NOT edit it.
## Copyright 1986-2020 Xilinx, Inc. All Rights Reserved.
############################################################
open_project reconfigurable_ensemble
set_top TOP_FUNCTION
add_files reconfigurable_ensemble/BDT.h
add_files reconfigurable_ensemble/SELECTORS.h
add_files reconfigurable_ensemble/bank_buffer.cpp
add_files reconfigurable_ensemble/bank_buffer.h
add_files reconfigurable_ensemble/ensamble.cpp
add_files reconfigurable_ensemble/ensamble.h
add_files reconfigurable_ensemble/parameters.h
add_files reconfigurable_ensemble/tree.cpp
add_files reconfigurable_ensemble/tree.h
add_files reconfigurable_ensemble/utils.h
add_files reconfigurable_ensemble/voting_station.cpp
add_files reconfigurable_ensemble/voting_station.hpp
add_files -tb reconfigurable_ensemble/testbench.cpp -cflags "-Wno-unknown-pragmas" -csimflags "-Wno-unknown-pragmas"
add_files -tb reconfigurable_ensemble/tb_data -cflags "-Wno-unknown-pragmas" -csimflags "-Wno-unknown-pragmas"
open_solution "tree" -flow_target vivado
set_part {xczu3eg-sbva484-1-e}
create_clock -period 2 -name default
source "./reconfigurable_ensemble/tree/directives.tcl"
csim_design
csynth_design
cosim_design
export_design -format ip_catalog
