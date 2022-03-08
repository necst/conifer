# Copyright 2022 Novel, Emerging Computing System Technologies Laboratory 
#                (NECSTLab), Politecnico di Milano

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#################
#    HLS4ML
#################
array set opt {
    reset      0
    csim       1
    synth      1
    cosim      0
    export     0
    vsynth     0
    fastsim    0
}

foreach arg $::argv {
  foreach o [lsort [array names opt]] {
    regexp "$o=+(\\w+)" $arg unused opt($o)
  }
}

file mkdir tb_data

if {$opt(reset)} {
    open_project -reset myproject_prj
} else {
    open_project myproject_prj
}

set_top TOP_FUNCTION
add_files firmware/BDT.h -cflags "-std=c++14"
add_files firmware/myproject.cpp -cflags "-std=c++14"
add_files firmware/utils.h -cflags "-std=c++14"
add_files -tb myproject_test.cpp -cflags "-I firmware/ -std=c++14"
add_files -tb firmware/weights
add_files -tb tb_data

source build_pdr_ips/tree_idle.tcl
source build_pdr_ips/vote_buffer.tcl
source build_pdr_ips/enumerator.tcl
##hls-fpga-machine-learning insert individual-ips

if {$opt(fastsim)} {
    open_solution "tree_idle"
    csim_design
}

exit
