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

################################################################
# START
################################################################

create_project -force ${prj_name} ${prj_dir} -part ${prj_part}
set_property BOARD_PART ${prj_board} [current_project]

variable design_name
set design_name tree_wrapper

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

create_bd_cell -type ip -vlnv xilinx.com:##project_name##:tree_cl0_0:1.0 tree_bb


create_bd_intf_port -mode Slave -vlnv xilinx.com:interface:axis_rtl:1.0 input_stream
set_property -dict [list CONFIG.TDATA_NUM_BYTES [get_property CONFIG.TDATA_NUM_BYTES [get_bd_intf_pins tree_bb/input_stream]] CONFIG.TID_WIDTH [get_property CONFIG.TID_WIDTH [get_bd_intf_pins tree_bb/input_stream]] CONFIG.HAS_TSTRB [get_property CONFIG.HAS_TSTRB [get_bd_intf_pins tree_bb/input_stream]] CONFIG.HAS_TKEEP [get_property CONFIG.HAS_TKEEP [get_bd_intf_pins tree_bb/input_stream]] CONFIG.HAS_TLAST [get_property CONFIG.HAS_TLAST [get_bd_intf_pins tree_bb/input_stream]]] [get_bd_intf_ports input_stream]
connect_bd_intf_net [get_bd_intf_pins tree_bb/input_stream] [get_bd_intf_ports input_stream]

create_bd_port -dir I -type clk -freq_hz 100000000 ap_clk
connect_bd_net [get_bd_pins /tree_bb/ap_clk] [get_bd_ports ap_clk]

create_bd_port -dir I -type rst resetn
connect_bd_net [get_bd_pins /tree_bb/ap_rst_n] [get_bd_ports resetn]

create_bd_intf_port -mode Master -vlnv xilinx.com:interface:axis_rtl:1.0 output_stream
connect_bd_intf_net [get_bd_intf_pins tree_bb/output_stream] [get_bd_intf_ports output_stream]

ipx::package_project -root_dir $ip_dir -vendor xilinx.com -library ##project_name## -taxonomy /UserIP -module tree_wrapper -import_files -force
ipx::remove_bus_parameter FREQ_HZ [ipx::get_bus_interfaces CLK.AP_CLK -of_objects [ipx::find_open_core xilinx.com:##project_name##:tree_wrapper:1.0]]
set_property core_revision 1 [ipx::find_open_core xilinx.com:##project_name##:tree_wrapper:1.0]
ipx::create_xgui_files [ipx::find_open_core xilinx.com:##project_name##:tree_wrapper:1.0]
ipx::update_checksums [ipx::find_open_core xilinx.com:##project_name##:tree_wrapper:1.0]
ipx::check_integrity [ipx::find_open_core xilinx.com:##project_name##:tree_wrapper:1.0]
ipx::save_core [ipx::find_open_core xilinx.com:##project_name##:tree_wrapper:1.0]

