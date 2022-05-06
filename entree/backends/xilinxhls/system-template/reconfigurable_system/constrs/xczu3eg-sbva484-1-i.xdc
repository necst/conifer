create_pblock pblock_tree_rp_0_0
add_cells_to_pblock [get_pblocks pblock_tree_rp_0_0] [get_cells -quiet [list top_system_i/tree_rp_0_0]]
resize_pblock [get_pblocks pblock_tree_rp_0_0] -add {SLICE_X5Y60:SLICE_X8Y119}
set_property SNAPPING_MODE ON [get_pblocks pblock_tree_rp_0_0]
create_pblock pblock_tree_rp_0_1
add_cells_to_pblock [get_pblocks pblock_tree_rp_0_1] [get_cells -quiet [list top_system_i/tree_rp_0_1]]
resize_pblock [get_pblocks pblock_tree_rp_0_1] -add {SLICE_X9Y60:SLICE_X12Y119}
set_property SNAPPING_MODE ON [get_pblocks pblock_tree_rp_0_1]
create_pblock pblock_tree_rp_0_2
add_cells_to_pblock [get_pblocks pblock_tree_rp_0_2] [get_cells -quiet [list top_system_i/tree_rp_0_2]]
resize_pblock [get_pblocks pblock_tree_rp_0_2] -add {SLICE_X22Y60:SLICE_X25Y119}
set_property SNAPPING_MODE ON [get_pblocks pblock_tree_rp_0_2]
create_pblock pblock_tree_rp_1_0
add_cells_to_pblock [get_pblocks pblock_tree_rp_1_0] [get_cells -quiet [list top_system_i/tree_rp_1_0]]
resize_pblock [get_pblocks pblock_tree_rp_1_0] -add {SLICE_X5Y0:SLICE_X8Y59}
set_property SNAPPING_MODE ON [get_pblocks pblock_tree_rp_1_0]
create_pblock pblock_tree_rp_1_1
add_cells_to_pblock [get_pblocks pblock_tree_rp_1_1] [get_cells -quiet [list top_system_i/tree_rp_1_1]]
resize_pblock [get_pblocks pblock_tree_rp_1_1] -add {SLICE_X9Y0:SLICE_X12Y59}
set_property SNAPPING_MODE ON [get_pblocks pblock_tree_rp_1_1]
create_pblock pblock_tree_rp_1_2
add_cells_to_pblock [get_pblocks pblock_tree_rp_1_2] [get_cells -quiet [list top_system_i/tree_rp_1_2]]
resize_pblock [get_pblocks pblock_tree_rp_1_2] -add {SLICE_X22Y0:SLICE_X25Y59}
set_property SNAPPING_MODE ON [get_pblocks pblock_tree_rp_1_2]
