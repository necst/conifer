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


################################################################
# This is a generated script based on design: design_1
#
# Though there are limitations about the generated script,
# the main purpose of this utility is to make learning
# IP Integrator Tcl commands easier.
################################################################

namespace eval _tcl {
proc get_script_folder {} {
   set script_path [file normalize [info script]]
   set script_folder [file dirname $script_path]
   return $script_folder
}
}
variable script_folder
set script_folder [_tcl::get_script_folder]

################################################################
# Check if script is running in correct Vivado version.
################################################################
set scripts_vivado_version 2020.2
set current_vivado_version [version -short]

if { [string first $scripts_vivado_version $current_vivado_version] == -1 } {
   puts ""
   catch {common::send_gid_msg -ssname BD::TCL -id 2041 -severity "ERROR" "This script was generated using Vivado <$scripts_vivado_version> and is being run in <$current_vivado_version> of Vivado. Please run the script in Vivado <$scripts_vivado_version> then open the design in Vivado <$current_vivado_version>. Upgrade the design by running \"Tools => Report => Report IP Status...\", then run write_bd_tcl to create an updated script."}

   return 1
}

################################################################
# COMMAND-LINE ARGUMENTS
################################################################
set prj_root  [lindex $argv 0]
set prj_dir [lindex $argv 1]
set ip_dir [lindex $argv 2]
set prj_name ## hls-fpga-machine-learning insert project-name
set prj_part ## hls-fpga-machine-learning insert project-part
set prj_board ## hls-fpga-machine-learning insert project-board
set sample_length ## hls-fpga-machine-learning insert sample_length
set n_classes ## hls-fpga-machine-learning insert n-classes
set result_lenght ## hls-fpga-machine-learning insert result_lenght
set output_length ## hls-fpga-machine-learning insert output_length
set n_banks ## hls-fpga-machine-learning insert n-banks
set n_trees_per_bank ## hls-fpga-machine-learning insert n-trees-per-bank
set id_length ## hls-fpga-machine-learning insert id-length


################################################################
# START
################################################################

# To test this script, run the following commands from Vivado Tcl console:
# source design_1_script.tcl

# If there is no project opened, this script will create a
# project, but make sure you do not have an existing project
# <./myproj/project_1.xpr> in the current working folder.

#set list_projs [get_projects -quiet]
#if { $list_projs eq "" } {
   create_project -force ${prj_name} ${prj_dir} -part ${prj_part}
   set_property BOARD_PART ${prj_board} [current_project]
#}



# CHANGE DESIGN NAME HERE
variable design_name
set design_name top_system

common::send_gid_msg -ssname BD::TCL -id 2003 -severity "INFO" "Currently there is no design <$design_name> in project, so creating one..."

create_bd_design $design_name

common::send_gid_msg -ssname BD::TCL -id 2004 -severity "INFO" "Making design <$design_name> as current_bd_design."
current_bd_design $design_name

set_property ip_repo_paths $ip_dir [current_project]
update_ip_catalog

set bCheckIPsPassed 1

set parentCell ""

variable script_folder
variable design_name

if { $parentCell eq "" } {
   set parentCell [get_bd_cells /]
}

# Get object for parentCell
set parentObj [get_bd_cells $parentCell]
if { $parentObj == "" } {
   catch {common::send_gid_msg -ssname BD::TCL -id 2090 -severity "ERROR" "Unable to find parent cell <$parentCell>!"}
   return
}

# Make sure parentObj is hier blk
set parentObj [get_bd_cells $parentCell]
if { $parentObj == "" } {
   catch {common::send_gid_msg -ssname BD::TCL -id 2090 -severity "ERROR" "Unable to find parent cell <$parentCell>!"}
   return
}

# Save current instance; Restore later
set oldCurInst [current_bd_instance .]

# Set parent object as current
current_bd_instance $parentObj

# TODO: Add support for Zynq UltraScale+
## hls-fpga-machine-learning insert processing-system-block
# Zynq-7000 (Pynq-Z2)
create_bd_cell -type ip -vlnv xilinx.com:ip:processing_system7:5.5 processing_system7
apply_bd_automation -rule xilinx.com:bd_rule:processing_system7 -config {make_external "FIXED_IO, DDR" apply_board_preset "1" Master "Disable" Slave "Disable" }  [get_bd_cells processing_system7]
set_property -dict [list CONFIG.PCW_USE_S_AXI_HP0 {1} CONFIG.PCW_USE_FABRIC_INTERRUPT {1} CONFIG.PCW_IRQ_F2P_INTR {1}] [get_bd_cells processing_system7]

# Create instance: axi_dma_samples, and set properties
set axi_dma_samples [ create_bd_cell -type ip -vlnv xilinx.com:ip:axi_dma:7.1 axi_dma_samples ]
set_property -dict [ list \
CONFIG.c_include_s2mm {0} \
CONFIG.c_include_sg {0} \
CONFIG.c_m_axi_mm2s_data_width $sample_length \
CONFIG.c_m_axis_mm2s_tdata_width $sample_length \
CONFIG.c_mm2s_burst_size {32} \
CONFIG.c_sg_include_stscntrl_strm {0} \
] $axi_dma_samples

# Create instance: axi_dma_ctrl, and set properties
set axi_dma_ctrl [ create_bd_cell -type ip -vlnv xilinx.com:ip:axi_dma:7.1 axi_dma_ctrl ]
set_property -dict [ list \
CONFIG.c_include_s2mm {0} \
CONFIG.c_include_sg {0} \
CONFIG.c_m_axis_mm2s_tdata_width {8} \
CONFIG.c_micro_dma {0} \
CONFIG.c_sg_include_stscntrl_strm {0} \
] $axi_dma_ctrl


# Create instance: enumerator, and set properties
set enumerator [ create_bd_cell -type ip -vlnv xilinx.com:##project_name##:enumerator:1.0 enumerator ]

# Create instance: axis_broadcaster_samples, and set properties
set axis_broadcaster_samples [ create_bd_cell -type ip -vlnv xilinx.com:ip:axis_broadcaster:1.1 axis_broadcaster_samples ]
set_property CONFIG.NUM_MI $n_banks $axis_broadcaster_samples

# Create instance: axis_broadcaster_samples, and set properties
set axis_broadcaster_ctrl [ create_bd_cell -type ip -vlnv xilinx.com:ip:axis_broadcaster:1.1 axis_broadcaster_ctrl ]
set_property CONFIG.NUM_MI $n_banks $axis_broadcaster_ctrl

# Create instance: bank_buffer, broadcasters, dfx_decoupler, tree, vote_buffer, and set properties
for {set i 0} {$i < $n_banks} {incr i} {
   set bank_buffer_$i [ create_bd_cell -type ip -vlnv xilinx.com:##project_name##:bank_buffer_[expr $i + 1]:1.0 bank_buffer_$i ]
   set axis_broadcaster_bank_$i [ create_bd_cell -type ip -vlnv xilinx.com:ip:axis_broadcaster:1.1 axis_broadcaster_bank_$i ]
   set_property CONFIG.NUM_MI $n_trees_per_bank [set axis_broadcaster_bank_$i]
   for {set j 0} {$j < $n_trees_per_bank} {incr j} {
   create_bd_cell -type ip -vlnv xilinx.com:ip:dfx_decoupler:1.0 dfx_decoupler_${i}_${j}
   set_property -dict [list CONFIG.ALL_PARAMS {HAS_SIGNAL_CONTROL 1 HAS_SIGNAL_STATUS 1 INTF {input_stream {ID 0 VLNV xilinx.com:interface:axis_rtl:1.0 MODE slave}}} CONFIG.GUI_SELECT_INTERFACE {0} CONFIG.GUI_INTERFACE_NAME {input_stream} CONFIG.GUI_SELECT_VLNV {xilinx.com:interface:axis_rtl:1.0} CONFIG.GUI_SELECT_MODE {slave} CONFIG.GUI_SIGNAL_SELECT_0 {TVALID} CONFIG.GUI_SIGNAL_SELECT_1 {TREADY} CONFIG.GUI_SIGNAL_SELECT_2 {TDATA} CONFIG.GUI_SIGNAL_SELECT_3 {TUSER} CONFIG.GUI_SIGNAL_SELECT_4 {TLAST} CONFIG.GUI_SIGNAL_SELECT_5 {TID} CONFIG.GUI_SIGNAL_SELECT_6 {TDEST} CONFIG.GUI_SIGNAL_SELECT_7 {TSTRB} CONFIG.GUI_SIGNAL_SELECT_8 {TKEEP} CONFIG.GUI_SIGNAL_DECOUPLED_0 {true} CONFIG.GUI_SIGNAL_DECOUPLED_1 {true} CONFIG.GUI_SIGNAL_PRESENT_0 {true} CONFIG.GUI_SIGNAL_PRESENT_1 {true} CONFIG.GUI_SIGNAL_PRESENT_2 {true} CONFIG.GUI_SIGNAL_PRESENT_4 {true} CONFIG.GUI_SIGNAL_WIDTH_2 {32} CONFIG.GUI_SIGNAL_WIDTH_7 {4} CONFIG.GUI_SIGNAL_WIDTH_8 {4}] [get_bd_cells dfx_decoupler_${i}_${j}]
   set_property -dict [list CONFIG.ALL_PARAMS {HAS_SIGNAL_CONTROL 1 HAS_SIGNAL_STATUS 1 INTF {input_stream {ID 0 VLNV xilinx.com:interface:axis_rtl:1.0 MODE slave} output_stream {ID 1 VLNV xilinx.com:interface:axis_rtl:1.0}}} CONFIG.GUI_SELECT_INTERFACE {1} CONFIG.GUI_INTERFACE_NAME {output_stream} CONFIG.GUI_SELECT_VLNV {xilinx.com:interface:axis_rtl:1.0} CONFIG.GUI_SELECT_MODE {master} CONFIG.GUI_SIGNAL_SELECT_0 {TVALID} CONFIG.GUI_SIGNAL_SELECT_1 {TREADY} CONFIG.GUI_SIGNAL_SELECT_2 {TDATA} CONFIG.GUI_SIGNAL_SELECT_3 {TUSER} CONFIG.GUI_SIGNAL_SELECT_4 {TLAST} CONFIG.GUI_SIGNAL_SELECT_5 {TID} CONFIG.GUI_SIGNAL_SELECT_6 {TDEST} CONFIG.GUI_SIGNAL_SELECT_7 {TSTRB} CONFIG.GUI_SIGNAL_SELECT_8 {TKEEP} CONFIG.GUI_SIGNAL_DECOUPLED_0 {true} CONFIG.GUI_SIGNAL_DECOUPLED_1 {true} CONFIG.GUI_SIGNAL_PRESENT_0 {true} CONFIG.GUI_SIGNAL_PRESENT_1 {true} CONFIG.GUI_SIGNAL_PRESENT_2 {true} CONFIG.GUI_SIGNAL_PRESENT_4 {true} CONFIG.GUI_SIGNAL_WIDTH_2 {32} CONFIG.GUI_SIGNAL_WIDTH_7 {4} CONFIG.GUI_SIGNAL_WIDTH_8 {4}] [get_bd_cells dfx_decoupler_${i}_${j}]
   set tree_${i}_${j} [ create_bd_cell -type ip -vlnv xilinx.com:##project_name##:tree_wrapper:1.0 tree_${i}_${j} ]
   set vote_buffer_${i}_${j} [ create_bd_cell -type ip -vlnv xilinx.com:##project_name##:vote_buffer:1.0 vote_buffer_${i}_${j} ]
   }

   # Create instance: axis_interconnect_0, and set properties
   set axis_interconnect_${i} [ create_bd_cell -type ip -vlnv xilinx.com:ip:axis_interconnect:2.1 axis_interconnect_${i} ]
   set_property -dict [ list \
      CONFIG.M00_AXIS_HIGHTDEST {0xFFFFFFFF} \
      CONFIG.NUM_MI {1} \
      CONFIG.NUM_SI $n_trees_per_bank \
   ] [set axis_interconnect_${i}]

   set axi_gpio_${i}_decouplers [create_bd_cell -type ip -vlnv xilinx.com:ip:axi_gpio:2.0 axi_gpio_${i}_decouplers]
   set_property -dict [list CONFIG.C_GPIO_WIDTH {1} CONFIG.C_GPIO2_WIDTH $n_trees_per_bank CONFIG.C_IS_DUAL {1} CONFIG.C_ALL_INPUTS_2 {1} CONFIG.C_ALL_OUTPUTS {1}] [get_bd_cells axi_gpio_${i}_decouplers]

   set concat_decoupler_status_${i} [create_bd_cell -type ip -vlnv xilinx.com:ip:xlconcat:2.1 concat_decoupler_status_${i}]
   set_property -dict [list CONFIG.NUM_PORTS $n_trees_per_bank ] [get_bd_cells concat_decoupler_status_${i}]

   set axi_gpio_${i}_reset [create_bd_cell -type ip -vlnv xilinx.com:ip:axi_gpio:2.0 axi_gpio_${i}_reset]
   set_property -dict [list CONFIG.C_GPIO_WIDTH {1} CONFIG.C_ALL_OUTPUTS {1}] [get_bd_cells axi_gpio_${i}_reset]
   set_property -dict [list CONFIG.C_DOUT_DEFAULT {0xFFFFFFFF}] [get_bd_cells axi_gpio_${i}_reset]

}

# Create instance: axis_interconnect_x, and set properties
set axis_interconnect_x [ create_bd_cell -type ip -vlnv xilinx.com:ip:axis_interconnect:2.1 axis_interconnect_x ]
set_property -dict [ list \
CONFIG.NUM_MI $n_classes \
CONFIG.NUM_SI $n_banks \
] $axis_interconnect_x


# Create instance: voting_station, and set properties
for {set i 0} {$i < $n_classes} {incr i} {

set voting_station_cl${i} [ create_bd_cell -type ip -vlnv xilinx.com:##project_name##:voting_station_cl${i}:1.0 voting_station_cl${i} ]
set axis_dwidth_converter_${i} [ create_bd_cell -type ip -vlnv xilinx.com:ip:axis_dwidth_converter:1.1 axis_dwidth_converter_${i} ]
set_property -dict [ list \
   CONFIG.M_TDATA_NUM_BYTES $output_length \
] [set axis_dwidth_converter_${i}]
set axi_dma_cl$i [ create_bd_cell -type ip -vlnv xilinx.com:ip:axi_dma:7.1 axi_dma_cl$i ]
set_property -dict [ list \
   CONFIG.c_include_mm2s {0} \
   CONFIG.c_include_sg {0} \
   CONFIG.c_m_axi_mm2s_data_width $output_length \
   CONFIG.c_m_axis_mm2s_tdata_width $output_length \
   CONFIG.c_s2mm_burst_size {32} \
   CONFIG.c_sg_include_stscntrl_strm {0} \
] [set axi_dma_cl${i}]
}

# Create instance: xlconcat_0, and set properties
set xlconcat [ create_bd_cell -type ip -vlnv xilinx.com:ip:xlconcat:2.1 xlconcat ]
set_property -dict [ list \
CONFIG.NUM_PORTS [expr $n_banks*$n_trees_per_bank] \
] $xlconcat

# Create instance: axi_intc, and set properties
set interrupt_controller [ create_bd_cell -type ip -vlnv xilinx.com:ip:axi_intc:4.1 interrupt_controller ]
set_property -dict [list CONFIG.C_IRQ_CONNECTION {1}] $interrupt_controller


# Nets
connect_bd_intf_net -intf_net axi_dma_samples_M_AXIS_MM2S [get_bd_intf_pins axi_dma_samples/M_AXIS_MM2S] [get_bd_intf_pins enumerator/input_stream]
connect_bd_intf_net -intf_net enumerator_output_stream [get_bd_intf_pins enumerator/output_stream] [get_bd_intf_pins axis_broadcaster_samples/S_AXIS]
connect_bd_intf_net -intf_net axi_dma_ctrl_M_AXIS_MM2S [get_bd_intf_pins axi_dma_ctrl/M_AXIS_MM2S] [get_bd_intf_pins axis_broadcaster_ctrl/S_AXIS]
for {set i 0} {$i < $n_banks} {incr i} {
      connect_bd_intf_net -intf_net [format "axis_broadcaster_samples_M%02d_AXIS" $i] [get_bd_intf_pins [format "axis_broadcaster_samples/M%02d_AXIS" $i]] [get_bd_intf_pins bank_buffer_${i}/input_stream]
      connect_bd_intf_net -intf_net [format "axis_broadcaster_ctrl_M%02d_AXIS" $i] [get_bd_intf_pins [format "axis_broadcaster_ctrl/M%02d_AXIS" $i]] [get_bd_intf_pins bank_buffer_${i}/command_stream]
      connect_bd_intf_net -intf_net bank_buffer_${i}_output_stream [get_bd_intf_pins bank_buffer_${i}/output_stream] [get_bd_intf_pins axis_broadcaster_bank_${i}/S_AXIS]
      for {set j 0} {$j < $n_trees_per_bank} {incr j} {
            connect_bd_intf_net -intf_net s_input_stream_${i}_${j} [get_bd_intf_pins axis_broadcaster_bank_${i}/[format "M%02d_AXIS" $j]] [get_bd_intf_pins dfx_decoupler_${i}_${j}/s_input_stream]
            connect_bd_intf_net -intf_net rp_input_stream_${i}_${j} [get_bd_intf_pins dfx_decoupler_${i}_${j}/rp_input_stream] [get_bd_intf_pins tree_${i}_${j}/input_stream]
            connect_bd_intf_net -intf_net rp_output_stream_${i}_${j} [get_bd_intf_pins tree_${i}_${j}/output_stream] [get_bd_intf_pins dfx_decoupler_${i}_${j}/rp_output_stream]
            connect_bd_intf_net -intf_net s_output_stream_${i}_${j} [get_bd_intf_pins dfx_decoupler_${i}_${j}/s_output_stream] [get_bd_intf_pins vote_buffer_${i}_${j}/input_stream]
            connect_bd_intf_net -intf_net axis_interconnect_${i}_[format "S%02d_AXIS" $j] [get_bd_intf_pins vote_buffer_${i}_${j}/output_stream] [get_bd_intf_pins axis_interconnect_${i}/[format "S%02d_AXIS" $j]]
            connect_bd_net -net tree_${i}_${j}_irq [get_bd_pins vote_buffer_${i}_${j}/irq] [get_bd_pins xlconcat/In[expr $i*$n_trees_per_bank+$j]]
            connect_bd_net [get_bd_pins dfx_decoupler_${i}_${j}/decouple_status] [get_bd_pins concat_decoupler_status_${i}/In${j}]
            if {$j == 0} {
               connect_bd_net -net axi_gpio_${i}_decouplers_gpio_io_o [get_bd_pins dfx_decoupler_${i}_${j}/decouple] [get_bd_pins axi_gpio_${i}_decouplers/gpio_io_o]
               connect_bd_net -net axi_gpio_${i}_resets_gpio_io_o [get_bd_pins tree_${i}_${j}/resetn] [get_bd_pins axi_gpio_${i}_reset/gpio_io_o]
            } else {
               connect_bd_net -net axi_gpio_${i}_decouplers_gpio_io_o [get_bd_pins dfx_decoupler_${i}_${j}/decouple]
               connect_bd_net -net axi_gpio_${i}_resets_gpio_io_o [get_bd_pins tree_${i}_${j}/resetn]
            }
      }
      connect_bd_net [get_bd_pins concat_decoupler_status_${i}/dout] [get_bd_pins axi_gpio_${i}_decouplers/gpio2_io_i]
      connect_bd_intf_net -intf_net axis_interconnect_x_[format "S%02d_AXIS" $i] [get_bd_intf_pins axis_interconnect_${i}/M00_AXIS] [get_bd_intf_pins axis_interconnect_x/[format "S%02d_AXIS" $i]]
}

for {set i 0} {$i < $n_classes} {incr i} {
            connect_bd_intf_net -intf_net voting_station_${i}_input_stream [get_bd_intf_pins axis_interconnect_x/[format "M%02d_AXIS" $i]] [get_bd_intf_pins voting_station_cl${i}/input_score_stream]
            connect_bd_intf_net -intf_net axis_dwidth_converter_${i}_S_AXIS [get_bd_intf_pins voting_station_cl${i}/output_score_stream] [get_bd_intf_pins axis_dwidth_converter_${i}/S_AXIS]
            connect_bd_intf_net -intf_net axi_dma_cl${i}_S_AXIS_S2MM [get_bd_intf_pins axis_dwidth_converter_${i}/M_AXIS] [get_bd_intf_pins axi_dma_cl${i}/S_AXIS_S2MM]
}

connect_bd_net -net xlconcat_dout1 [get_bd_pins interrupt_controller/intr] [get_bd_pins xlconcat/dout]

#Zynq-7000
connect_bd_net -net interrupt_controller_irq [get_bd_pins interrupt_controller/irq] [get_bd_pins processing_system7/IRQ_F2P]
#AXI4-Lite
startgroup
for {set i 0} {$i < $n_classes} {incr i} {
   apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config { Clk_master {Auto} Clk_slave {Auto} Clk_xbar {Auto} Master {/processing_system7/M_AXI_GP0} Slave {/axi_dma_cl${i}/S_AXI_LITE} ddr_seg {Auto} intc_ip {New AXI Interconnect} master_apm {0}}  [get_bd_intf_pins axi_dma_cl${i}/S_AXI_LITE]
}
apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config { Clk_master {Auto} Clk_slave {Auto} Clk_xbar {Auto} Master {/processing_system7/M_AXI_GP0} Slave {/axi_dma_ctrl/S_AXI_LITE} ddr_seg {Auto} intc_ip {New AXI Interconnect} master_apm {0}}  [get_bd_intf_pins axi_dma_ctrl/S_AXI_LITE]
apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config { Clk_master {Auto} Clk_slave {Auto} Clk_xbar {Auto} Master {/processing_system7/M_AXI_GP0} Slave {/axi_dma_samples/S_AXI_LITE} ddr_seg {Auto} intc_ip {New AXI Interconnect} master_apm {0}}  [get_bd_intf_pins axi_dma_samples/S_AXI_LITE]
for {set i 0} {$i < $n_banks} {incr i} {
   apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config { Clk_master {Auto} Clk_slave {Auto} Clk_xbar {Auto} Master {/processing_system7/M_AXI_GP0} Slave {/axi_gpio_${i}_decouplers/S_AXI} ddr_seg {Auto} intc_ip {New AXI Interconnect} master_apm {0}}  [get_bd_intf_pins axi_gpio_${i}_decouplers/S_AXI]
   apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config { Clk_master {Auto} Clk_slave {Auto} Clk_xbar {Auto} Master {/processing_system7/M_AXI_GP0} Slave {/axi_gpio_${i}_reset/S_AXI} ddr_seg {Auto} intc_ip {New AXI Interconnect} master_apm {0}}  [get_bd_intf_pins axi_gpio_${i}_reset/S_AXI]
}
apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config { Clk_master {Auto} Clk_slave {Auto} Clk_xbar {Auto} Master {/processing_system7/M_AXI_GP0} Slave {/interrupt_controller/s_axi} ddr_seg {Auto} intc_ip {New AXI Interconnect} master_apm {0}}  [get_bd_intf_pins interrupt_controller/s_axi]
endgroup
#AXI4-Master
apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config { Clk_master {Auto} Clk_slave {Auto} Clk_xbar {Auto} Master {/axi_dma_samples/M_AXI_MM2S} Slave {/processing_system7/S_AXI_HP0} ddr_seg {Auto} intc_ip {New AXI Interconnect} master_apm {0}}  [get_bd_intf_pins processing_system7/S_AXI_HP0]
startgroup
apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config { Clk_master {Auto} Clk_slave {/processing_system7/FCLK_CLK0 (100 MHz)} Clk_xbar {/processing_system7/FCLK_CLK0 (100 MHz)} Master {/axi_dma_ctrl/M_AXI_MM2S} Slave {/processing_system7/S_AXI_HP0} ddr_seg {Auto} intc_ip {/axi_mem_intercon} master_apm {0}}  [get_bd_intf_pins axi_dma_ctrl/M_AXI_MM2S]
for {set i 0} {$i < $n_classes} {incr i} {
   apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config { Clk_master {Auto} Clk_slave {/processing_system7/FCLK_CLK0 (100 MHz)} Clk_xbar {/processing_system7/FCLK_CLK0 (100 MHz)} Master {/axi_dma_cl0/M_AXI_S2MM} Slave {/processing_system7/S_AXI_HP0} ddr_seg {Auto} intc_ip {/axi_mem_intercon} master_apm {0}}  [get_bd_intf_pins axi_dma_cl${i}/M_AXI_S2MM]
}
endgroup
#Clocks
startgroup
apply_bd_automation -rule xilinx.com:bd_rule:clkrst -config { Clk {/processing_system7/FCLK_CLK0 (100 MHz)} Freq {100} Ref_Clk0 {} Ref_Clk1 {} Ref_Clk2 {}}  [get_bd_pins axis_broadcaster_ctrl/aclk]
apply_bd_automation -rule xilinx.com:bd_rule:clkrst -config { Clk {/processing_system7/FCLK_CLK0 (100 MHz)} Freq {100} Ref_Clk0 {} Ref_Clk1 {} Ref_Clk2 {}}  [get_bd_pins axis_broadcaster_samples/aclk]
for {set i 0} {$i < $n_banks} {incr i} {
   apply_bd_automation -rule xilinx.com:bd_rule:clkrst -config { Clk {/processing_system7/FCLK_CLK0 (100 MHz)} Freq {100} Ref_Clk0 {} Ref_Clk1 {} Ref_Clk2 {}}  [get_bd_pins axis_broadcaster_bank_${i}/aclk]
}
for {set i 0} {$i < $n_classes} {incr i} {
   apply_bd_automation -rule xilinx.com:bd_rule:clkrst -config { Clk {/processing_system7/FCLK_CLK0 (100 MHz)} Freq {100} Ref_Clk0 {} Ref_Clk1 {} Ref_Clk2 {}}  [get_bd_pins axis_dwidth_converter_${i}/aclk]
}
for {set i 0} {$i < $n_banks} {incr i} {
   apply_bd_automation -rule xilinx.com:bd_rule:clkrst -config { Clk {/processing_system7/FCLK_CLK0 (100 MHz)} Freq {100} Ref_Clk0 {} Ref_Clk1 {} Ref_Clk2 {}}  [get_bd_pins axis_interconnect_${i}/ACLK]
   apply_bd_automation -rule xilinx.com:bd_rule:clkrst -config { Clk {/processing_system7/FCLK_CLK0 (100 MHz)} Freq {100} Ref_Clk0 {} Ref_Clk1 {} Ref_Clk2 {}}  [get_bd_pins axis_interconnect_${i}/M00_AXIS_ACLK]
   for {set j 0} {$j < $n_trees_per_bank} {incr j} {
      apply_bd_automation -rule xilinx.com:bd_rule:clkrst -config { Clk {/processing_system7/FCLK_CLK0 (100 MHz)} Freq {100} Ref_Clk0 {} Ref_Clk1 {} Ref_Clk2 {}}  [get_bd_pins axis_interconnect_${i}/[format "S%02d" $j]_AXIS_ACLK]
   }
}
apply_bd_automation -rule xilinx.com:bd_rule:clkrst -config { Clk {/processing_system7/FCLK_CLK0 (100 MHz)} Freq {100} Ref_Clk0 {} Ref_Clk1 {} Ref_Clk2 {}}  [get_bd_pins axis_interconnect_x/ACLK]
for {set i 0} {$i < $n_classes} {incr i} {
   apply_bd_automation -rule xilinx.com:bd_rule:clkrst -config { Clk {/processing_system7/FCLK_CLK0 (100 MHz)} Freq {100} Ref_Clk0 {} Ref_Clk1 {} Ref_Clk2 {}}  [get_bd_pins axis_interconnect_x/[format "M%02d" $i]_AXIS_ACLK]
}
for {set i 0} {$i < $n_banks} {incr i} {
   for {set j 0} {$j < $n_trees_per_bank} {incr j} {
      apply_bd_automation -rule xilinx.com:bd_rule:clkrst -config { Clk {/processing_system7/FCLK_CLK0 (100 MHz)} Freq {100} Ref_Clk0 {} Ref_Clk1 {} Ref_Clk2 {}}  [get_bd_pins tree_${i}_${j}/ap_clk]
   }
}
endgroup

#Restore current instance
current_bd_instance $oldCurInst

validate_bd_design
save_bd_design

set dir [get_property DIRECTORY [current_project]]
set name [get_property NAME [current_project]]
set bdFile [get_files ${dir}/${name}.srcs/sources_1/bd/*.bd]
set bdName [file rootname [file tail $bdFile]]

save_bd_design -quiet
update_compile_order -fileset [current_fileset]
make_wrapper -files $bdFile -top
set_property synth_checkpoint_mode Hierarchical $bdFile
add_files -norecurse ${dir}/${name}.gen/sources_1/bd/top_system/hdl/top_system_wrapper.v
export_ip_user_files -of_objects  $bdFile -sync -no_script -force -quiet
generate_target all $bdFile -quiet
regenerate_bd_layout
