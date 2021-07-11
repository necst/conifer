## hls-fpga-machine-learning begin bank 0
## hls-fpga-machine-learning begin tree 0
create_pblock pblock_tree_0_0
add_cells_to_pblock [get_pblocks pblock_tree_0_0] [get_cells -quiet [list top_system_i/tree_0_0/inst/tree_bb]]
resize_pblock [get_pblocks pblock_tree_0_0] -add {SLICE_X56Y0:SLICE_X59Y49}
set_property RESET_AFTER_RECONFIG true [get_pblocks pblock_tree_0_0]
set_property SNAPPING_MODE ON [get_pblocks pblock_tree_0_0]
set_property HD.RECONFIGURABLE true [get_cells top_system_i/tree_0_0/inst/tree_bb]
## hls-fpga-machine-learning begin tree 1
create_pblock pblock_tree_0_1
add_cells_to_pblock [get_pblocks pblock_tree_0_1] [get_cells -quiet [list top_system_i/tree_0_1/inst/tree_bb]]
resize_pblock [get_pblocks pblock_tree_0_1] -add {SLICE_X60Y0:SLICE_X63Y49}
set_property RESET_AFTER_RECONFIG true [get_pblocks pblock_tree_0_1]
set_property SNAPPING_MODE ON [get_pblocks pblock_tree_0_1]
set_property HD.RECONFIGURABLE true [get_cells top_system_i/tree_0_1/inst/tree_bb]
## hls-fpga-machine-learning begin tree 2
create_pblock pblock_tree_0_2
add_cells_to_pblock [get_pblocks pblock_tree_0_2] [get_cells -quiet [list top_system_i/tree_0_2/inst/tree_bb]]
resize_pblock [get_pblocks pblock_tree_0_2] -add {SLICE_X64Y0:SLICE_X67Y49}
set_property RESET_AFTER_RECONFIG true [get_pblocks pblock_tree_0_2]
set_property SNAPPING_MODE ON [get_pblocks pblock_tree_0_2]
set_property HD.RECONFIGURABLE true [get_cells top_system_i/tree_0_2/inst/tree_bb]
## hls-fpga-machine-learning begin bank 1
## hls-fpga-machine-learning begin tree 0
create_pblock pblock_tree_1_0
add_cells_to_pblock [get_pblocks pblock_tree_1_0] [get_cells -quiet [list top_system_i/tree_1_0/inst/tree_bb]]
resize_pblock [get_pblocks pblock_tree_1_0] -add {SLICE_X72Y0:SLICE_X75Y49}
set_property RESET_AFTER_RECONFIG true [get_pblocks pblock_tree_1_0]
set_property SNAPPING_MODE ON [get_pblocks pblock_tree_1_0]
set_property HD.RECONFIGURABLE true [get_cells top_system_i/tree_1_0/inst/tree_bb]
## hls-fpga-machine-learning begin tree 1
create_pblock pblock_tree_1_1
add_cells_to_pblock [get_pblocks pblock_tree_1_1] [get_cells -quiet [list top_system_i/tree_1_2/inst/tree_bb]]
resize_pblock [get_pblocks pblock_tree_1_1] -add {SLICE_X76Y0:SLICE_X79Y49}
set_property RESET_AFTER_RECONFIG true [get_pblocks pblock_tree_1_1]
set_property SNAPPING_MODE ON [get_pblocks pblock_tree_1_1]
set_property HD.RECONFIGURABLE true [get_cells top_system_i/tree_1_1/inst/tree_bb]
## hls-fpga-machine-learning begin tree 2
create_pblock pblock_tree_1_2
add_cells_to_pblock [get_pblocks pblock_tree_1_2] [get_cells -quiet [list top_system_i/tree_1_1/inst/tree_bb]]
resize_pblock [get_pblocks pblock_tree_1_2] -add {SLICE_X82Y0:SLICE_X85Y49}
set_property RESET_AFTER_RECONFIG true [get_pblocks pblock_tree_1_2]
set_property SNAPPING_MODE ON [get_pblocks pblock_tree_1_2]
set_property HD.RECONFIGURABLE true [get_cells top_system_i/tree_1_2/inst/tree_bb]
