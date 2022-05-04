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

# Part of this source file comes from the Conifer open-source project 
# (https://github.com/thesps/conifer)

import os
import sys
from shutil import copyfile
import numpy as np
import math
import glob
import zipfile
from jinja2 import Environment, FileSystemLoader

_TOOLS = {
    'vivadohls': 'vivado_hls',
    'vitishls': 'vitis_hls'
}

# Templates directory:
env = Environment(loader=FileSystemLoader('entree/backends/xilinxhls'))

def get_tool_exe_in_path(tool):
    if tool not in _TOOLS.keys():
        return None

    tool_exe = _TOOLS[tool]

    if os.system('which {} > /dev/null 2>/dev/null'.format(tool_exe)) != 0:
        return None

    return tool_exe


def get_hls():

    tool_exe = None

    if '_tool' in globals():
        tool_exe = get_tool_exe_in_path(_tool)
    else:
        for tool in _TOOLS.keys():
            tool_exe = get_tool_exe_in_path(tool)
            if tool_exe != None:
                break

    return tool_exe


def write(ensemble_dict, cfg):

    filedir = os.path.dirname(os.path.abspath(__file__))

    tree_count = 0
    class_count = 1
    for itree, trees in enumerate(ensemble_dict['trees']):
        tree_count += len(trees)
        if len(trees) > class_count:
            class_count = len(trees)

    # TODO: Flexible bank sizing
    if cfg.get('PDR', False) == True:
        bank_count = int(cfg['Banks'])
    

    os.makedirs('{}/firmware'.format(cfg['OutputDir']))
    os.makedirs('{}/tb_data'.format(cfg['OutputDir']))
    copyfile('{}/firmware/BDT.h'.format(filedir),
             '{}/firmware/BDT.h'.format(cfg['OutputDir']))
    copyfile('{}/firmware/utils.h'.format(filedir),
            '{}/firmware/utils.h'.format(cfg['OutputDir']))
    if cfg.get('PDR', False) == True:
        os.makedirs('{}/{}_reconfigurable_system'.format(cfg['OutputDir'], cfg['ProjectName']))
        os.makedirs('{}/{}_reconfigurable_system/srcs'.format(cfg['OutputDir'], cfg['ProjectName']))
        os.makedirs('{}/{}_reconfigurable_system/srcs/dcp'.format(cfg['OutputDir'], cfg['ProjectName']))
        os.makedirs('{}/{}_reconfigurable_system/srcs/hdl'.format(cfg['OutputDir'], cfg['ProjectName']))
        os.makedirs('{}/{}_reconfigurable_system/srcs/ip'.format(cfg['OutputDir'], cfg['ProjectName']))
        os.makedirs('{}/{}_reconfigurable_system/srcs/prj'.format(cfg['OutputDir'], cfg['ProjectName']))
        os.makedirs('{}/{}_reconfigurable_system/constrs'.format(cfg['OutputDir'], cfg['ProjectName']))
        os.makedirs('{}/{}_reconfigurable_system/scripts'.format(cfg['OutputDir'], cfg['ProjectName']))
        os.makedirs('{}/{}_reconfigurable_system/scripts/tcl'.format(cfg['OutputDir'], cfg['ProjectName']))
        for entry in os.scandir('{}/system-template/reconfigurable_system/scripts/tcl'.format(filedir)):
            if entry.is_file():
                copyfile(
                    entry.path, 
                    '{}/{}_reconfigurable_system/scripts/tcl/{}'.format(cfg['OutputDir'], cfg['ProjectName'], entry.name)
                )


    ###################
    # myproject.cpp
    ###################

    template = env.get_template('hls-template/firmware/myproject.cpp.jinja')
    
    tree_ips=[]
    # loop over trees
    for itree, trees in enumerate(ensemble_dict['trees']):
        # loop over classes
        for iclass, tree in enumerate(trees):
                tree_ips.append({"itree": itree, "trees": trees, "iclass": iclass, "tree": tree})
    
    template.stream(
        projectname=cfg['ProjectName'],
        cfg_get=cfg.get('PDR', False),
        bank_count=bank_count,
        tree_ips=tree_ips,
        range_bank_count=range(1, bank_count + 1),
        class_count=class_count
    ).dump('{}/firmware/{}.cpp'.format(cfg['OutputDir'], cfg['ProjectName']))
    
    ###################
    # parameters.h
    ###################

    template = env.get_template('hls-template/firmware/parameters.h.jinja')
    
    tree_fields = ['feature', 'threshold', 'value',
               'children_left', 'children_right', 'parent']

    tree_ips_fields=[]
    # loop over trees
    for itree, trees in enumerate(ensemble_dict['trees']):
        # loop over classes
        for iclass, tree in enumerate(trees):
            # loop over fields
            for ifield, field in enumerate(tree_fields):
                map_tree=','.join(map(str, tree[field]))
                tree_ips_fields.append({"itree": itree, "trees": trees, "iclass": iclass, "tree": tree,"ifield": ifield, "field": field,"map_tree": map_tree})
    
    max_parallel_samples=6
    
    template.stream(
        cfg_get_PDR=cfg.get('PDR', False),
        Precision=cfg['Precision'],
        n_trees=ensemble_dict['n_trees'],
        max_depth=ensemble_dict['max_depth'],
        n_features=ensemble_dict['n_features'],
        n_classes=ensemble_dict['n_classes'],
        norm=str(ensemble_dict['norm']),
        init_predict=str(ensemble_dict['init_predict'][0]),
        len_init_predict=len(ensemble_dict['init_predict']),
        enumerate_init_predict=enumerate(ensemble_dict['init_predict']),
        trees=ensemble_dict['trees'],
        len_tree_fields=len(tree_fields),
        tree_ips=tree_ips_fields,
        len_trees=len(trees),
        len_tree=len(tree),
        bank_count=bank_count,
        max_parallel_samples = max_parallel_samples
    ).dump('{}/firmware/parameters.h'.format(cfg['OutputDir']))


    #######################
    # myproject.h
    #######################
  

    template = env.get_template('hls-template/firmware/myproject.h.jinja')

    # VOTING STATION IPs
    class_count = 1
    for itree, trees in enumerate(ensemble_dict['trees']):
         if len(trees) > class_count:
             class_count = len(trees)

    template.stream(
        cfg_get=cfg.get('PDR', False),
        projectname=cfg['ProjectName'],
        range_bank_count=range(1, bank_count + 1),
        ensemble_trees=enumerate(ensemble_dict['trees']),
        bank_count=bank_count,
        enumerate_tree=enumerate(trees),
        tree_ips=tree_ips,
        range_class_count=range(class_count)
    ).dump('{}/firmware/{}.h'.format(cfg['OutputDir'], cfg['ProjectName']))

    #######################
    # myproject_test.cpp
    #######################

    if cfg.get('PDR', False) == False:
        template = env.get_template( 'hls-template/myproject_test.cpp.jinja')
    else:
        template = env.get_template( 'hls-template/myproject_pdr_test.cpp.jinja')

    template.stream(
        n_features=ensemble_dict['n_features'],
        n_classes=ensemble_dict['n_classes'],
        cfg_get=cfg.get('PDR', False),
        projectname=cfg['ProjectName'],
        class_count=class_count,
        tree_ips=tree_ips,
        enumerate_tree=enumerate(trees),
        ensemble_trees=enumerate(ensemble_dict['trees']),
        indent='    '
    ).dump('{}/{}_test.cpp'.format(cfg['OutputDir'], cfg['ProjectName']))


    #######################
    # build_prj.tcl
    #######################

    bdtdir = os.path.abspath(os.path.join(filedir, "../bdt_utils"))
    relpath = os.path.relpath(bdtdir, start=cfg['OutputDir'])

    # build_prj.tcl
    if cfg.get('PDR', False) == False:
        template = env.get_template('hls-template/build_prj.tcl.jinja')
    else:
        template = env.get_template('hls-template/build_pdr_prj.tcl.jinja')

    template.stream(
        ProjectName=cfg['ProjectName'],
        XilinxPart=cfg['XilinxPart'],
        ClockPeriod=cfg['ClockPeriod'],
        weights=False,
        tree_ips=tree_ips,
        range_class_count=range(class_count),
        cfg_get=cfg.get('PDR', False),
        range_bank_count=range(1, bank_count + 1)
    ).dump('{}/build_prj.tcl'.format(cfg['OutputDir']))

    # bank buffer
    if cfg.get('PDR', False) == True:
        os.mkdir('{}/build_pdr_ips'.format(cfg['OutputDir']))
        for ibank in range(1, bank_count + 1):
            template = env.get_template('hls-template/build_pdr_ip.tcl.jinja')
            
            template.stream(
                projectname=cfg['ProjectName'],
                XilinxPart=cfg['XilinxPart'],
                ClockPeriod=cfg['ClockPeriod'],
                the_ip='bank_buffer_{}'.format(ibank)
            ).dump('{}/build_pdr_ips/bank_buffer_{}.tcl'.format(cfg['OutputDir'], ibank))
        
        # class
        for itree, trees in enumerate(ensemble_dict['trees']):
            for iclass, tree in enumerate(trees): 
                template=env.get_template('hls-template/build_pdr_ip.tcl.jinja')

                template.stream(
                    projectname=cfg['ProjectName'],
                    XilinxPart=cfg['XilinxPart'],
                    ClockPeriod=cfg['ClockPeriod'],
                    the_ip='tree_cl{}_{}'.format(iclass, itree)
                ).dump('{}/build_pdr_ips/tree_cl{}_{}.tcl'.format(cfg['OutputDir'], iclass, itree))
        
        # voting station
        for iclass in range(class_count):
            template=env.get_template('hls-template/build_pdr_ip.tcl.jinja')

            template.stream(
                    projectname=cfg['ProjectName'],
                    XilinxPart=cfg['XilinxPart'],
                    ClockPeriod=cfg['ClockPeriod'],
                    the_ip='voting_station_cl{}'.format(iclass)
            ).dump('{}/build_pdr_ips/voting_station_cl{}.tcl'.format(cfg['OutputDir'], iclass))

        template=env.get_template('hls-template/build_pdr_ip.tcl.jinja')

        template.stream(
                projectname=cfg['ProjectName'],
                XilinxPart=cfg['XilinxPart'],
                ClockPeriod=cfg['ClockPeriod'],
                the_ip='tree_idle'
        ).dump('{}/build_pdr_ips/tree_idle.tcl'.format(cfg['OutputDir']))

        template=env.get_template('hls-template/build_pdr_ip.tcl.jinja')

        template.stream(
                projectname=cfg['ProjectName'],
                XilinxPart=cfg['XilinxPart'],
                ClockPeriod=cfg['ClockPeriod'],
                the_ip='vote_buffer'
        ).dump('{}/build_pdr_ips/vote_buffer.tcl'.format(cfg['OutputDir']))

        template=env.get_template('hls-template/build_pdr_ip.tcl.jinja')

        template.stream(
                projectname=cfg['ProjectName'],
                XilinxPart=cfg['XilinxPart'],
                ClockPeriod=cfg['ClockPeriod'],
                the_ip='enumerator'
        ).dump('{}/build_pdr_ips/enumerator.tcl'.format(cfg['OutputDir']))

    #######################
    # build_tree_wrapper.tcl
    #######################

    if cfg.get('PDR', False) == True:

        template = env.get_template('system-template/tree_wrapper.tcl.jinja')

        template.stream(
                projectname=cfg['ProjectName'],
                XilinxPart=cfg['XilinxPart'],
                XilinxBoard=cfg['XilinxBoard']
        ).dump('{}/build_tree_wrapper.tcl'.format(cfg['OutputDir']))
        


    #######################
    # build_system_bd.tcl
    #######################

    if cfg.get('PDR', False) == True:

        template = env.get_template('system-template/top_system.tcl.jinja')

        precision = int(cfg['Precision'].split('<')[1].split(',')[0])


        template.stream(
                projectname=cfg['ProjectName'],
                XilinxPart=cfg['XilinxPart'],
                XilinxBoard=cfg['XilinxBoard'],
                TreesPerBank=int(cfg['TreesPerBank']),
                bank_count=bank_count,
                class_count=class_count,
                max_parallel_samples=max_parallel_samples,
                num1=int((2**math.ceil(math.log(precision, 2)))*ensemble_dict['n_features']),
                num2=int(8*math.ceil(precision)/8),
                num3=int(2**math.ceil(math.log(8*(math.ceil(precision)/8), 2))),
                num4=int(math.ceil(math.log(int(max_parallel_samples), 2))+1)
        ).dump('{}/build_system_bd.tcl'.format(cfg['OutputDir']))
        


    #######################
    # build_tree_wrapper.tcl
    #######################
"""
# 8
###################################################################################################################################
###################################################################################################################################
################################# B U I L D _ T R E E _ W R A P P E R . T C L #####################################################
###################################################################################################################################
###################################################################################################################################


    if cfg.get('PDR', False) == True:
        f = open(os.path.join(filedir, 'system-template/tree_wrapper.tcl'), 'r')
        fout = open('{}/build_tree_wrapper.tcl'.format(cfg['OutputDir']), 'w')
        for line in f.readlines():

            precision = int(cfg['Precision'].split('<')[1].split(',')[0])
            
            if '## hls-fpga-machine-learning insert project-name' in line:
                line = line.replace('## hls-fpga-machine-learning insert project-name', '{}_system'.format(cfg['ProjectName']))
            elif '## hls-fpga-machine-learning insert project-part' in line:
                line = line.replace('## hls-fpga-machine-learning insert project-part', cfg['XilinxPart'])
            elif '## hls-fpga-machine-learning insert project-board' in line:
                line = line.replace('## hls-fpga-machine-learning insert project-board', cfg['XilinxBoard'])
            if '##project_name##' in line:
                line = line.replace('##project_name##', cfg['ProjectName'])
            # TODO: Manage clock
            #elif 'create_clock -period 5 -name default' in line:
            #    line = 'create_clock -period {} -name default\n'.format(
            #        cfg['ClockPeriod'])

            fout.write(line)
        f.close()
        fout.close()

    #######################
    # synth_static_shell.tcl
    #######################
# 9
###################################################################################################################################
###################################################################################################################################
################################# S Y N T H _ S T A T I C _ S H E L L . T C L #####################################################
###################################################################################################################################
###################################################################################################################################


    if cfg.get('PDR', False) == True:
        
        template = env.get_template('synth_static_shell.tcl')
        
        output = template.render(
            projectname=cfg['ProjectName'],
            file = open(os.path.join(filedir, 'system-template/static_shell.tcl'), 'r')
        )
        with open('{}/synth_static_shell.tcl'.format(cfg['OutputDir']), 'w') as synth_static_shell:
            synth_static_shell.write(output)
        

    #######################
    # design.tcl
    #######################
# 10
###################################################################################################################################
###################################################################################################################################
###################################### D E S I G N . T C L ########################################################################
###################################################################################################################################
###################################################################################################################################


    if cfg.get('PDR', False) == True:
        f = open(os.path.join(filedir, 'system-template/reconfigurable_system/scripts/design.tcl'), 'r')
        fout = open('{}/{}_reconfigurable_system/scripts/design.tcl'.format(cfg['OutputDir'], cfg['ProjectName']) , 'w')

        trees_per_bank = int(cfg['TreesPerBank'])
        rp_variants = math.ceil(tree_count / (trees_per_bank * bank_count))

        for line in f.readlines():
            
            if '## hls-fpga-machine-learning insert project-part' in line:
                line = line.replace('## hls-fpga-machine-learning insert project-part', cfg['XilinxPart'])
            elif '## hls-fpga-machine-learning insert rp-module-definition' in line:
                line = ''

                curr_bank = 0
                curr_tree_in_bank = 0
                curr_variant = 0

                for itree, trees in enumerate(ensemble_dict['trees']):
                    for iclass, tree in enumerate(trees):
                        if (curr_variant == 0):
                            line += 'set module_{bank}_{tree} "top_system_tree_{bank}_{tree}_0_tree_wrapper_tree_bb_0"\n'.format(
                                bank = curr_bank,
                                tree = curr_tree_in_bank
                            )

                        line += 'set module_{bank}_{tree}_variant{variant} "tree_cl{the_class}_{tree_in_class}"\n'.format(
                            bank = curr_bank,
                            tree = curr_tree_in_bank,
                            variant = curr_variant,
                            the_class = iclass,
                            tree_in_class = itree
                        )
                        line += 'set variant $module_{bank}_{tree}_variant{variant}\n'.format(
                            bank = curr_bank,
                            tree = curr_tree_in_bank,
                            variant = curr_variant
                        )
                        line += 'add_module $variant\n'
                        line += 'set_attribute module $variant moduleName   $module_{bank}_{tree}\n'.format(
                            bank = curr_bank,
                            tree = curr_tree_in_bank
                        )
                        line += 'set_attribute module $variant prj          $prjDir/$variant.prj\n'
                        line += 'set_attribute module $variant xdc          $ipDir/$variant/constraints/TOP_FUNCTION_ooc.xdc\n'
                        line += 'set_attribute module $variant synth        ${run.rmSynth}\n'
                        line += '\n'

                        curr_variant += 1

                        if (curr_variant >= rp_variants):
                            curr_variant = 0
                            curr_tree_in_bank += 1
                            if (curr_tree_in_bank >= trees_per_bank):
                                curr_tree_in_bank = 0
                                curr_bank += 1
                
                line += '\n'
                line += '\n'

                for ibank in range(bank_count):
                    for itree in range(trees_per_bank):
                        line += 'set module_{bank}_{tree}_inst "top_system_i/tree_{bank}_{tree}/inst/tree_bb"\n'.format(
                            bank = ibank,
                            tree = itree
                        )
                
                line += '\n'
                line += '\n'

            elif '## hls-fpga-machine-learning insert rp-configuration' in line:
                line = ''

                for i_config in range(rp_variants):
                    line += 'set config "Config_{}" \n'.format(i_config);
                    line += '\n';
                    line += 'add_implementation $config\n';
                    line += 'set_attribute impl $config top             $top\n';
                    line += 'set_attribute impl $config pr.impl         1\n';
                    line += 'set_attribute impl $config implXDC         [list $xdcDir/top_system_pblock.xdc \\\n';
                    line += '                                        ]\n';
                    line += 'set_attribute impl $config impl            ${run.prImpl} \n';
                    line += 'set_attribute impl $config partitions      [list [list $static           $top           {}] \\\n'.format(
                        'implement' if i_config == 0 else 'import'
                    );
                    for i_bank in range(bank_count):
                        for i_tree in range(trees_per_bank):
                            line += '                                                [list [ if {{ [info exists module_{bank}_{tree}_variant{variant}] == 1 }} {{set module_{bank}_{tree}_variant{variant}}} {{set module_0_0_variant0}} ] $module_{bank}_{tree}_inst [ if {{ [info exists module_{bank}_{tree}_variant{variant}] == 1 }} {{expr {{{{implement}}}}}} {{expr {{{{greybox}}}}}} ]] \\\n'.format(
                                bank = i_bank,
                                tree = i_tree,
                                variant = i_config
                            );
                    line += '                                        ]\n';
                    line += 'set_attribute impl $config verify          ${run.prVerify} \n';
                    line += 'set_attribute impl $config bitstream       ${run.writeBitstream} \n';
                    line += 'set_attribute impl $config cfgmem.pcap     1\n';
                    line += '\n';
                line += '\n';
            elif '## hls-fpga-machine-learning insert rp-flat-configuration' in line:
                line = ''

                line += 'add_implementation Flat\n'
                line += 'set_attribute impl Flat top          $top\n'
                line += 'set_attribute impl Flat implXDC      [list $xdcDir/top_system_pblock.xdc \\\n'
                line += '                                    ]\n'
                line += 'set_attribute impl Flat partitions   [list [list $static           $top           implement] \\\n'
                for i_bank in range(bank_count):
                    for i_tree in range(trees_per_bank):
                        line += '                                                [list $module_0_0_variant0 $module_{bank}_{tree}_inst greybox] \\\n'.format(
                            bank = i_bank,
                            tree = i_tree,
                            variant = 0
                        );
                line += '                                    ]\n'
                line += 'set_attribute impl Flat impl         ${run.flatImpl}\n'

            fout.write(line)
        f.close()
        fout.close()

    #######################
    # top_system_pblock.tcl
    #######################
# 11
###################################################################################################################################
###################################################################################################################################
################################# T O P _ S Y S T E M _ P B L O C K . T C L #######################################################
###################################################################################################################################
###################################################################################################################################


    if cfg.get('PDR', False) == True:
        f = open(os.path.join(filedir, 'system-template/reconfigurable_system/constrs/{}.xdc'.format(cfg['XilinxPart'])), 'r')
        fout = open('{}/{}_reconfigurable_system/constrs/top_system_pblock.xdc'.format(cfg['OutputDir'], cfg['ProjectName']) , 'w')

        trees_per_bank = int(cfg['TreesPerBank'])

        outputting_bank = False
        outputting_tree = False

        for line in f.readlines():
            if '## hls-fpga-machine-learning begin bank ' in line:
                i_bank = int(line.replace('## hls-fpga-machine-learning begin bank ', ''))
                outputting_bank = i_bank < bank_count
                line = ''
            elif '## hls-fpga-machine-learning begin tree ' in line and outputting_bank:
                i_tree = int(line.replace('## hls-fpga-machine-learning begin tree ', ''))
                outputting_tree = i_tree < trees_per_bank
                line = ''
            
            if (outputting_bank and outputting_tree):
                fout.write(line)
        
        f.close()
        fout.close()
"""

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
