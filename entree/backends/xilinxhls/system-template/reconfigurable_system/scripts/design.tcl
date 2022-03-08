# This source file comes from the Xilinx(r) Application Node 1231
# (https://xilinx-wiki.atlassian.net/wiki/spaces/A/pages/18841851/XAPP1231+-+Partial+Reconfiguration+of+a+Hardware+Accelerator+with+Vivado+Design+Suite)

###############################################################
###   Tcl Variables
###############################################################
####Define location for "Tcl" directory. Defaults to "./Tcl"
set tclHome "./scripts/tcl"
if {[file exists $tclHome]} {
   set tclDir $tclHome
} elseif {[file exists "./tcl"]} {
   set tclDir  "./tcl"
} else {
   error "ERROR: No valid location found for required Tcl scripts. Set \$tclDir in design.tcl to a valid location."
}
puts "Setting TCL dir to $tclDir"

####Source required Tcl Procs
source $tclDir/design_utils.tcl
source $tclDir/log_utils.tcl
source $tclDir/synth_utils.tcl
source $tclDir/impl_utils.tcl
source $tclDir/hd_floorplan_utils.tcl

###############################################################
### Define Part, Package, Speedgrade 
###############################################################
set part ## hls-fpga-machine-learning insert project-part
check_part $part

###############################################################
###  Setup Variables
###############################################################
#set tclParams [list <param1> <value> <param2> <value> ... <paramN> <value>]
set tclParams [list hd.visual 1 \
              ]

####flow control
set run.rmSynth        1
set run.prImpl         1
set run.prVerify       1
set run.writeBitstream 1
set run.flatImpl       0

####Report and DCP controls - values: 0-required min; 1-few extra; 2-all
set verbose      1
set dcpLevel     1

####Output Directories
set synthDir  "./Synth"
set implDir   "./Implement"
set dcpDir    "./Checkpoint"
set bitDir    "./Bitstreams"

####Input Directories
set srcDir     "./srcs"
set xdcDir     "./constrs"
set rtlDir     "$srcDir/hdl"
set ipDir      "$srcDir/ip"
set prjDir     "$srcDir/prj"

###############################################################
### Top Definition
###############################################################
set top "top_system_wrapper"
set static "static"
add_module $static
set_attribute module $static moduleName      $top
set_attribute module $static top_level       1
set_attribute module $static synthCheckpoint $srcDir/dcp/static_shell.dcp

####################################################################
### RP Module Definitions
####################################################################

## hls-fpga-machine-learning insert rp-module-definition

########################################################################
### Configurations (Implementation) Definition
########################################################################

## hls-fpga-machine-learning insert rp-configuration

####################################################################
### Create Flat implementation run 
####################################################################

## hls-fpga-machine-learning insert rp-flat-configuration

########################################################################
### Task / flow portion
########################################################################
source $tclDir/run.tcl

exit
