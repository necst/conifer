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

set prj_dir [lindex $argv 0]
set prj_name ## hls-fpga-machine-learning insert project-name

open_project ${prj_dir}/${prj_name}.xpr

update_compile_order -fileset sources_1
#TODO: Parametrize parallelism
reset_run synth_1
launch_runs synth_1 -jobs 2
wait_on_run synth_1
open_run synth_1 -name synth_1
write_checkpoint ${prj_dir}/static_shell.dcp -force
write_hw_platform -fixed -force -file ${prj_dir}/static_shell.xsa