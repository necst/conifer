################################################################
# COMMAND-LINE ARGUMENTS
################################################################
# TODO: update to jinja 
set prj_root  [lindex $argv 0]
set prj_dir [lindex $argv 1]
set ip_dir [lindex $argv 2]
set prj_name ## hls-fpga-machine-learning insert project-name
set prj_part ## hls-fpga-machine-learning insert project-part
set prj_board ## hls-fpga-machine-learning insert project-board
set sample_length ## hls-fpga-machine-learning insert sample_length
set n_classes ## hls-fpga-machine-learning insert n-classes
set n_trees_per_class ## hls-fpga-machine-learning insert n-trees-per-class
set result_lenght ## hls-fpga-machine-learning insert result_lenght
set output_length ## hls-fpga-machine-learning insert output_length
set n_banks ## hls-fpga-machine-learning insert n-banks
set n_trees_per_bank ## hls-fpga-machine-learning insert n-trees-per-bank
set id_length ## hls-fpga-machine-learning insert id-length
set n_jobs ## hls-fpga-machine-learning insert n-jobs


# generate output products for every element in the design
generate_target all [get_files  ${prj_dir}/${prj_root}.srcs/sources_1/bd/top_system/top_system.bd]
export_ip_user_files -of_objects [get_files ${prj_dir}/${prj_root}.srcs/sources_1/bd/top_system/top_system.bd] -no_script -sync -force -quiet
create_ip_run [get_files -of_objects [get_fileset sources_1] ${prj_dir}/${prj_root}.srcs/sources_1/bd/top_system/top_system.bd]
launch_runs top_system_* -jobs ${n_jobs}


# DFX wizard: set configurations and configuration runs
# TODO: use jinja in order to generate configurations for every conmbination of n_bank n_trees_per_bank n_classes n_trees_per_class
create_pr_configuration -name config_1 -partitions [list top_system_i/tree_rp_0_0:tree_rm_0_0_inst_0 top_system_i/tree_rp_0_1:tree_rm_0_1_inst_0 top_system_i/tree_rp_0_2:tree_rm_0_2_inst_0 top_system_i/tree_rp_1_0:tree_rm_0_3_inst_0 top_system_i/tree_rp_1_1:tree_rm_0_4_inst_0 top_system_i/tree_rp_1_2:tree_rm_0_5_inst_0 ]
create_pr_configuration -name config_2 -partitions [list top_system_i/tree_rp_0_0:tree_rm_1_0_inst_0 top_system_i/tree_rp_0_1:tree_rm_1_1_inst_0 top_system_i/tree_rp_0_2:tree_rm_1_2_inst_0 top_system_i/tree_rp_1_0:tree_rm_1_3_inst_0 top_system_i/tree_rp_1_1:tree_rm_1_4_inst_0 top_system_i/tree_rp_1_2:tree_rm_1_5_inst_0 ]
create_pr_configuration -name config_3 -partitions [list top_system_i/tree_rp_0_0:tree_rm_2_0_inst_0 top_system_i/tree_rp_0_1:tree_rm_2_1_inst_0 top_system_i/tree_rp_0_2:tree_rm_2_2_inst_0 top_system_i/tree_rp_1_0:tree_rm_2_3_inst_0 top_system_i/tree_rp_1_1:tree_rm_2_4_inst_0 top_system_i/tree_rp_1_2:tree_rm_2_5_inst_0 ]
set_property PR_CONFIGURATION config_1 [get_runs impl_1]
create_run child_0_impl_1 -parent_run impl_1 -flow {Vivado Implementation 2021} -pr_config config_2
create_run child_1_impl_1 -parent_run impl_1 -flow {Vivado Implementation 2021} -pr_config config_3

# launch synthesis
launch_runs synth_1 -jobs 12
wait_on_run synth_1



# TODO: try to find out how to use cnstraint files instead of tcl commands to do floorplanning
open_run synth_1 -name synth_1 -pr_config [current_pr_configuration]

startgroup
create_pblock pblock_tree_rp_0_0
resize_pblock pblock_tree_rp_0_0 -add SLICE_X5Y60:SLICE_X8Y119
add_cells_to_pblock pblock_tree_rp_0_0 [get_cells [list top_system_i/tree_rp_0_0]] -clear_locs
endgroup
startgroup
create_pblock pblock_tree_rp_0_1
resize_pblock pblock_tree_rp_0_1 -add SLICE_X9Y60:SLICE_X12Y119
add_cells_to_pblock pblock_tree_rp_0_1 [get_cells [list top_system_i/tree_rp_0_1]] -clear_locs
endgroup
startgroup
create_pblock pblock_tree_rp_0_2
resize_pblock pblock_tree_rp_0_2 -add SLICE_X22Y60:SLICE_X25Y119
add_cells_to_pblock pblock_tree_rp_0_2 [get_cells [list top_system_i/tree_rp_0_2]] -clear_locs
endgroup

file mkdir /home/users/matteo.santelmo/Desktop/TEST/TEST_entree_2/iris_PDR_Vivado_GB_system/iris_PDR_Vivado_GB_system.srcs/constrs_1/new
close [ open /home/users/matteo.santelmo/Desktop/TEST/TEST_entree_2/iris_PDR_Vivado_GB_system/iris_PDR_Vivado_GB_system.srcs/constrs_1/new/pblocks.xdc w ]
add_files -fileset constrs_1 /home/users/matteo.santelmo/Desktop/TEST/TEST_entree_2/iris_PDR_Vivado_GB_system/iris_PDR_Vivado_GB_system.srcs/constrs_1/new/pblocks.xdc
set_property target_constrs_file /home/users/matteo.santelmo/Desktop/TEST/TEST_entree_2/iris_PDR_Vivado_GB_system/iris_PDR_Vivado_GB_system.srcs/constrs_1/new/pblocks.xdc [current_fileset -constrset]
save_constraints -force