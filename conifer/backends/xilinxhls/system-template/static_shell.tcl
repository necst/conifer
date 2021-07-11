set prj_dir [lindex $argv 0]
set prj_name ## hls-fpga-machine-learning insert project-name

open_project ${prj_dir}/${prj_name}.xpr

update_compile_order -fileset sources_1
#TODO: Parametrize parallelism
reset_run synth_1
launch_runs synth_1 -jobs 20
wait_on_run synth_1
open_run synth_1 -name synth_1
write_checkpoint ${prj_dir}/static_shell.dcp -force
write_hw_platform -fixed -force -file ${prj_dir}/static_shell.xsa