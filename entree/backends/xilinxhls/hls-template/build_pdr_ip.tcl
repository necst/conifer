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

if {$opt(reset)} {
    open_solution -reset "the_ip"
} else {
    open_solution "the_ip"
}

set_part {xc7vx690tffg1927-2}
create_clock -period 5 -name default
set_directive_top -name TOP_FUNCTION "myproject__the_ip"

if {$opt(csim)} {
    csim_design
}

if {$opt(synth)} {
    csynth_design
}

if {$opt(cosim)} {
    cosim_design -trace_level all
}

if {$opt(export)} {
    export_design -format ip_catalog -description "myproject__the_ip" -display_name "myproject__the_ip" -ipname "the_ip" -library "myproject"
}

if {$opt(vsynth)} {
    puts "NOT IMPLEMENTED YET"
}