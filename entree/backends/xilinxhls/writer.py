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
import shutil
import sys
import numpy as np
import math
import glob
import zipfile
from . import templating_environment as env

_TOOLS = {
    'vivadohls': 'vivado_hls',
    'vitishls': 'vitis_hls'
}



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
    else:
        bank_count = 0
    

    os.makedirs('{}/firmware'.format(cfg['OutputDir']))
    os.makedirs('{}/tb_data'.format(cfg['OutputDir']))
    shutil.copyfile('{}/firmware/BDT.h'.format(filedir),
             '{}/firmware/BDT.h'.format(cfg['OutputDir']))
    shutil.copyfile('{}/firmware/utils.h'.format(filedir),
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
                shutil.copyfile(
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
        cfg_PDR=cfg.get('PDR', False),
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
                tree_ips_fields.append({"itree": itree, "trees": trees, "iclass": iclass, "tree": tree,"ifield": ifield, "field": field,"map_tree": tree[field]})
    
    max_parallel_samples=6
    
    template.stream(
        cfg_PDR=cfg.get('PDR', False),
        Precision=cfg['Precision'],
        n_trees=ensemble_dict['n_trees'],
        max_depth=ensemble_dict['max_depth'],
        n_features=ensemble_dict['n_features'],
        n_classes=ensemble_dict['n_classes'],
        norm=str(ensemble_dict['norm']),
        init_predict=ensemble_dict['init_predict'],
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
        cfg_PDR=cfg.get('PDR', False),
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
        cfg_PDR=cfg.get('PDR', False),
        projectname=cfg['ProjectName'],
        class_count=class_count,
        tree_ips=tree_ips,
        enumerate_tree=enumerate(trees),
        ensemble_trees=enumerate(ensemble_dict['trees'])
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
        cfg_PDR=cfg.get('PDR', False),
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
    # build_system_bd.tcl
    #######################
    
    # create list that counts for each class the nuber of trees
    trees_in_class = []
    for itree, trees in enumerate(ensemble_dict['trees']):
        for iclass, tree in enumerate(trees): 
            if itree == 0 :
                trees_in_class.append(1)
            else:
                trees_in_class[iclass] += 1

    if cfg.get('PDR', False) == True:

        template = env.get_template('system-template/top_system.tcl.jinja')

        precision = int(cfg['Precision'].split('<')[1].split(',')[0])

        # Set tree_rp and tree_rm
        n_banks = int(cfg['Banks'])
        n_trees_per_bank = int(cfg['TreesPerBank'])
        n_classes = int(ensemble_dict['n_classes'])
        n_trees = int(ensemble_dict['n_trees'])
        n_total_trees = 0
        for i in range(n_classes):
            n_total_trees += trees_in_class[i]     

        rm_in_rp_list = [[] for i in range(n_banks*n_trees_per_bank)]
        counter = 0

        for i in range(n_banks):
            for j in range(n_trees_per_bank):
                rm_in_rp_list[i * n_trees_per_bank + j].append("tree_rm_idle")
       
        for i in range(n_classes):
            for j in range(trees_in_class[i]):
                rm_in_rp_list[counter].append("tree_rm_{}_{}".format(i,j))
                if counter == (n_trees_per_bank * n_banks) - 1:
                    counter = 0
                else:
                    counter += 1
        counter = 0
        rm_in_rp_dict = []

        for i in range(n_banks):
            for j in range(n_trees_per_bank):
                rm_in_rp_dict.append({ "rp": "tree_rp_{}_{}".format(i,j) , "rm": rm_in_rp_list[counter]  })
                counter += 1

        template.stream(
                projectname = cfg['ProjectName'],
                XilinxPart = cfg['XilinxPart'],
                XilinxBoard = cfg['XilinxBoard'],
                TreesPerBank = int(cfg['TreesPerBank']),
                nBanks = bank_count,
                nClasses = class_count,
                TreesInClass = trees_in_class,
                rm_in_rp_dict = rm_in_rp_dict,
                SampleLength = int((2**math.ceil(math.log(precision, 2)))*ensemble_dict['n_features']),
                ResultLength = int(8*math.ceil(precision)/8),
                OutputLength = int(2**math.ceil(math.log(8*(math.ceil(precision)/8), 2))),
                IDLength = int(math.ceil(math.log(int(max_parallel_samples), 2))+1)
        ).dump('{}/build_system_bd.tcl'.format(cfg['OutputDir']))
        
    #######################
    # synth_and_impl.tcl
    #######################
        template = env.get_template('system-template/synth_and_impl.tcl.jinja')
        # NOTE: for how the template is designed, runs are set correctly only when
        # number of total trees is a multiple of number of tree slots in the architecture.
        template.stream(
                projectname = cfg['ProjectName'],
                XilinxPart = cfg['XilinxPart'],
                XilinxBoard = cfg['XilinxBoard'],
                n_trees_per_bank = int(cfg['TreesPerBank']),
                rm_in_rp_dict = rm_in_rp_dict,
                iter_cfgs = range( tree_count ),
                iter_runs = range(int(n_total_trees / (n_trees_per_bank*n_banks))),
                n_trees = n_trees,
                n_banks = bank_count,
                nClasses = class_count,
                nJobs = int(cfg['nJobs']),
                n_cfgs = math.ceil((n_total_trees / (n_trees_per_bank*n_banks)))
        ).dump('{}/synth_and_impl.tcl'.format(cfg['OutputDir'], cfg['ProjectName']) )

    #######################
    # top_system_pblock.tcl
    #######################
    if cfg.get('PDR', False) == True and cfg.get('autoFloorplanning', False) == True:
        f = open(os.path.join(filedir, 'system-template/reconfigurable_system/constrs/{}.xdc'.format(cfg['XilinxPart'])), 'r')
        fout = open('{}/{}_reconfigurable_system/constrs/top_system_pblock.xdc'.format(cfg['OutputDir'], cfg['ProjectName']) , 'w')
        # TODO: add here what to do with the constraint used for floorplanning! 
        # TODO: add jinja substitution for future parameters      
        for line in f.readlines():
            fout.write(line)
        
        f.close()
        fout.close()

def auto_config():
    config = {'ProjectName': 'my_prj',
              'OutputDir': 'my-entree-prj',
              'Precision': 'ap_fixed<18,8>',
              'XilinxPart': 'xczu3eg-sbva484-1-i',
              'ClockPeriod': '5',
              'PDR': False,
              'nJobs': str(os.cpu_count() - 2),
              'autoFloorplanning': True }
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
        # Create System Project
        cmd = 'vivado -nojournal -nolog -mode batch -source build_system_bd.tcl -tclargs {prj} $(pwd)/{prj} $(pwd)/{hls}'.format(prj=config['ProjectName']+'_system', hls=config['ProjectName']+'_prj')
        print(cmd)
        success = os.system(cmd)
        if(success > 0):
            print("'build' failed")
            sys.exit(-8)
        
        # Create configurations and runs synthesis, implementation and write bitstreams
        cmd = 'vivado -nojournal -nolog -mode batch -source synth_and_impl.tcl -tclargs {prj} $(pwd)/{prj} $(pwd)/{prjname}_reconfigurable_system/constrs/top_system_pblock.xdc'.format(prj=config['ProjectName']+'_system', prjname=config['ProjectName'])
        print(cmd)
        success = os.system(cmd)
        if(success > 0):
            print("synthesis or implementation failed")
            sys.exit(-9)

        # Set destination folder and move there bitstreams and .hwh files
        current = os.getcwd()
        os.mkdir('{}/exports'.format(current))
        destination = '{}/exports'.format(current)
        # move .bit files to the destination folder 
        source = '{}/{}_system/{}_system.runs'.format(current, config['ProjectName'], config['ProjectName'], config['ProjectName'])
        for i in os.listdir(source):
            if ('impl_1' in i) or ('child_' in i):
                for j in os.listdir('{}/{}'.format(source,i)):
                    if '.bit' in j:
                        shutil.copyfile('{}/{}/{}'.format(source,i,j), '{}/{}'.format(destination,j))
        # move .hwh files to destination folder, renaming with same names of .bit
        source = '{}/{}_system/{}_system.gen/sources_1/bd'.format(current, config['ProjectName'], config['ProjectName'], config['ProjectName'])
        for i in os.listdir(source):
            if 'tree_rm' in i:
                for j in os.listdir(destination):
                    if i in j and '.bit' in j:
                        j = j.replace('.bit','.hwh')
                        shutil.copyfile('{}/{}/hw_handoff/{}.hwh'.format(source,i,i),'{}/{}'.format(destination,j))
        source = '{}/{}_system/{}_system.gen/sources_1/bd/top_system/hw_handoff/top_system.hwh'.format(current, config['ProjectName'], config['ProjectName'], config['ProjectName'])
        shutil.copyfile(source, '{}/top_system_wrapper.hwh'.format(destination))

    os.chdir(cwd)
