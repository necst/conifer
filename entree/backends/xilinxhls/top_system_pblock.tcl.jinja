
########################################################################################################################################
    if cfg.get('PDR', False) == True:
        file = open(os.path.join(filedir, 'system-template/reconfigurable_system/constrs/{}.xdc'.format(cfg['XilinxPart'])), 'r')
        fout = open('{}/{}_reconfigurable_system/constrs/top_system_pblock.xdc'.format(cfg['OutputDir'], cfg['ProjectName']) , 'w')

        trees_per_bank = int(cfg['TreesPerBank'])

        outputting_bank = False
        outputting_tree = False
#########################################################################################################################################
        {% for line in file %}
            {% if '## hls-fpga-machine-learning begin bank ' in line:
                {% set i_bank = line|replace('## hls-fpga-machine-learning begin bank ', '')|int %}
                outputting_bank = i_bank < bank_count
                {% set line = '' %}
            {% elif '## hls-fpga-machine-learning begin tree ' in line and outputting_bank %}
                {% set i_tree = line|replace('## hls-fpga-machine-learning begin tree ', '')|int %}
                outputting_tree = i_tree < trees_per_bank
                {% set line = '' %}
            {% endif %}
            {% if (outputting_bank and outputting_tree) %}
                {{line}}
            {% endif  %}
        {% endfor %}
        
########################################################################################################################################################
        file.close()
        fout.close()

def auto_config():
    config = {'ProjectName': 'my_prj',
              'OutputDir': 'my-entree-prj',
              'Precision': 'ap_fixed<18,8>',
              'XilinxPart': 'xcvu9p-flgb2104-2L-e',
              'ClockPeriod': '5',
              'PDR': False}
    return config

def decision_function(X, config, trees=False):
    np.savetxt('{}/tb_data/tb_input_features.dat'.format(config['OutputDir']),
               X, delimiter=",", fmt='%10f')
    cwd = os.getcwd()
    os.chdir(config['OutputDir'])

    hls_tool = get_hls()
    if hls_tool == None:
        print("No HLS in PATH. Did you source the appropriate Xilinx Toolchain?")
        sys.exit(-1)

    if config.get('PDR', False) == False:
        cmd = '{} -f build_prj.tcl "csim=1 synth=0" > predict.log'.format(hls_tool)
    else:
        if config.get('PDR', False) and hls_tool != 'vitis_hls':
            print("Partial Dinamic Reconfiguration requires Xilinx Vitis HLS (Vivado HLS is not supported)")
            sys.exit(-2)
        cmd = '{} -f build_prj.tcl "csim=0 fastsim=1 synth=0" > predict.log'.format(hls_tool)

    success = os.system(cmd)
    if(success > 0):
        print("'predict' failed, check predict.log")
        sys.exit(-3)
    y = np.loadtxt('tb_data/csim_results.log')
    if trees:
        tree_scores = np.loadtxt('tb_data/csim_tree_results.log')
    os.chdir(cwd)
    if trees:
        return y, tree_scores
    else:
        return y


def sim_compile(config):
    return


def build(config, reset=False, csim=False, synth=True, cosim=False, export=False):
    cwd = os.getcwd()
    os.chdir(config['OutputDir'])

    hls_tool = get_hls()
    if hls_tool == None:
        print("No HLS in PATH. Did you source the appropriate Xilinx Toolchain?")
        sys.exit(-4)

    if config.get('PDR', False) and hls_tool != 'vitis_hls':
        print("Partial Dinamic Reconfiguration requires Xilinx Vitis HLS (Vivado HLS is not supported)")
        sys.exit(-5)

    cmd = '{hls_tool} -f build_prj.tcl "reset={reset} csim={csim} synth={synth} cosim={cosim} export={export}"'\
        .format(hls_tool=hls_tool, reset=reset, csim=csim, synth=synth, cosim=cosim, export=export)
    success = os.system(cmd)
    if(success > 0):
        print("'build' failed")
        sys.exit(-6)

    if config.get('PDR', False) == True:
        # Create Tree Wrapper Project
        cmd = 'vivado -nojournal -nolog -mode batch -source build_tree_wrapper.tcl -tclargs {prj} $(pwd)/{prj} $(pwd)/{hls}'.format(prj=config['ProjectName']+'_tree_wrapper', hls=config['ProjectName']+'_prj')
        print(cmd)
        success = os.system(cmd)
        if(success > 0):
            print("'build' failed")
            sys.exit(-7)

        # Create System Project
        cmd = 'vivado -nojournal -nolog -mode batch -source build_system_bd.tcl -tclargs {prj} $(pwd)/{prj} $(pwd)/{hls}'.format(prj=config['ProjectName']+'_system', hls=config['ProjectName']+'_prj')
        print(cmd)
        success = os.system(cmd)
        if(success > 0):
            print("'build' failed")
            sys.exit(-8)

        # Enabling Black-Box Synthesis
        for file in glob.glob('./{}/**/synth/tree_wrapper_tree_*.v'.format(config['ProjectName']+'_system'), recursive=True):
            print(file)

            local_name = os.path.basename(os.path.dirname(os.path.dirname(file)))
            global_name = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(file))))) + '_' + local_name

            with open(file, 'r') as original_file:
                with open('./{}/srcs/hdl/{}.v'.format(config['ProjectName']+'_reconfigurable_system', global_name), 'w') as dest_file:
                    for line in original_file.readlines():
                        if not ('(* black_box="true" *)' in line):
                            line = line.replace(local_name, global_name)
                            dest_file.write(line)

            os.rename(file, file+'.bak')
            f = open(file+'.bak', 'r')
            fout = open(file, 'w')
            for line in f.readlines():
                    if line.startswith('module tree_'):
                            line = '(* black_box="true" *)\n' + line
                    
                    fout.write(line)
            f.close()
            fout.close()
            
        cmd = 'vivado -nojournal -nolog -mode batch -source synth_static_shell.tcl -tclargs $(pwd)/{prj}'.format(prj=config['ProjectName']+'_system')
        print(cmd)
        success = os.system(cmd)
        if(success > 0):
            print("'static shell's synth failed")
            sys.exit(-9)

        # Prepare source files for reconfiguration
        print("START PREPARING FOR RECONFIG...")

        # Gathering Static Shell dcp
        copyfile('./{}/static_shell.dcp'.format(config['ProjectName']+'_system'), 
        './{}/srcs/dcp/static_shell.dcp'.format(config['ProjectName']+'_reconfigurable_system'))
        
        # Extracting RM IPs
        ip_srcs = './{}/srcs/ip'.format(config['ProjectName']+'_reconfigurable_system')

        for ip_archive in glob.iglob('./{}/tree_*/impl/export.zip'.format(config['ProjectName']+'_prj')):
            ip_name = os.path.basename(os.path.dirname(os.path.dirname(ip_archive)))
            with zipfile.ZipFile(ip_archive, 'r') as zip_ref:
                zip_ref.extractall(path=ip_srcs + '/' + ip_name)

        # Generating IP PRJs
        prevOutDir = os.getcwd()
        os.chdir('./{}/'.format(config['ProjectName']+'_reconfigurable_system'))
        wrapper_sources = glob.glob('./srcs/hdl/*.v')
        for ip_folder in glob.iglob('./srcs/ip/tree_*'):
            ip_name = os.path.basename(ip_folder)
            ip_sources = glob.glob('{}/hdl/verilog/*.v'.format(ip_folder))
            with open('./srcs/prj/{}.prj'.format(ip_name), 'w') as dest_file:
                    for line in map(lambda x: 'verilog xil_defaultLib ' + x, ip_sources + wrapper_sources):
                        dest_file.write(line + '\n')

        cmd = 'vivado -nojournal -nolog -mode batch -source scripts/design.tcl'
        print(cmd)
        success = os.system(cmd)
        if(success > 0):
            print("'reconfig synth failed")
            sys.exit(-10)

        os.chdir(prevOutDir)
    os.chdir(cwd)
