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

## hls-fpga-machine-learning begin bank 0
## hls-fpga-machine-learning begin tree 0
create_pblock pblock_tree_rp_0_0
add_cells_to_pblock [get_pblocks pblock_tree_rp_0_0] [get_cells -quiet [list top_system_i/tree_rp_0_0]]
resize_pblock [get_pblocks pblock_tree_rp_0_0] -add {SLICE_X5Y120:SLICE_X8Y179}
set_property SNAPPING_MODE ON [get_pblocks pblock_tree_rp_0_0]
## hls-fpga-machine-learning begin tree 1
create_pblock pblock_tree_rp_0_1
add_cells_to_pblock [get_pblocks pblock_tree_rp_0_1] [get_cells -quiet [list top_system_i/tree_rp_0_1]]
resize_pblock [get_pblocks pblock_tree_rp_0_1] -add {SLICE_X5Y60:SLICE_X8Y119}
set_property SNAPPING_MODE ON [get_pblocks pblock_tree_rp_0_1]
## hls-fpga-machine-learning begin tree 2
create_pblock pblock_tree_rp_0_2
add_cells_to_pblock [get_pblocks pblock_tree_rp_0_2] [get_cells -quiet [list top_system_i/tree_rp_0_2]]
resize_pblock [get_pblocks pblock_tree_rp_0_2] -add {SLICE_X5Y0:SLICE_X8Y59}
set_property SNAPPING_MODE ON [get_pblocks pblock_tree_rp_0_2]
## hls-fpga-machine-learning begin bank 1
## hls-fpga-machine-learning begin tree 0
create_pblock pblock_tree_rp_1_0
add_cells_to_pblock [get_pblocks pblock_tree_rp_1_0] [get_cells -quiet [list top_system_i/tree_rp_1_0]]
resize_pblock [get_pblocks pblock_tree_rp_1_0] -add {SLICE_X22Y120:SLICE_X26Y179}
set_property SNAPPING_MODE ON [get_pblocks pblock_tree_rp_1_0]
## hls-fpga-machine-learning begin tree 1
create_pblock pblock_tree_rp_1_1
add_cells_to_pblock [get_pblocks pblock_tree_rp_1_1] [get_cells -quiet [list top_system_i/tree_rp_1_1]]
resize_pblock [get_pblocks pblock_tree_rp_1_1] -add {SLICE_X22Y60:SLICE_X26Y119}
set_property SNAPPING_MODE ON [get_pblocks pblock_tree_rp_1_1]
## hls-fpga-machine-learning begin tree 2
create_pblock pblock_tree_rp_1_2
add_cells_to_pblock [get_pblocks pblock_tree_rp_1_2] [get_cells -quiet [list top_system_i/tree_rp_1_2]]
resize_pblock [get_pblocks pblock_tree_rp_1_2] -add {SLICE_X22Y0:SLICE_X26Y59}
set_property SNAPPING_MODE ON [get_pblocks pblock_tree_rp_1_2]
