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