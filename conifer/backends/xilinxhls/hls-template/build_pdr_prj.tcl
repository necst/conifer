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
##hls-fpga-machine-learning insert individual-ips

if {$opt(fastsim)} {
    open_solution "tree_idle"
    csim_design
}

exit
