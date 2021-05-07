############################################################
## This file is generated automatically by Vitis HLS.
## Please DO NOT edit it.
## Copyright 1986-2020 Xilinx, Inc. All Rights Reserved.
############################################################
open_project reconfigurable_ensemble
add_files reconfigurable_ensemble/BDT.h
add_files reconfigurable_ensemble/ensamble.cpp
add_files reconfigurable_ensemble/ensamble.h
add_files reconfigurable_ensemble/parameters.h
add_files reconfigurable_ensemble/utils.h
add_files reconfigurable_ensemble/voting_station.cpp
add_files reconfigurable_ensemble/voting_station.hpp
add_files -tb reconfigurable_ensemble/testbench.cpp
add_files -tb reconfigurable_ensemble/tb_data
open_solution "voting_station" -flow_target vivado
set_part {xczu3eg-sbva484-1-e}
create_clock -period 10 -name default
#source "./reconfigurable_ensemble/voting_station/directives.tcl"
csim_design
csynth_design
cosim_design
export_design -format ip_catalog
