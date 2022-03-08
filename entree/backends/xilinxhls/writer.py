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

    fout = open(
        '{}/firmware/{}.cpp'.format(cfg['OutputDir'], cfg['ProjectName']), 'w')
    fout.write('#include "BDT.h"\n')
    fout.write('#include "parameters.h"\n')
    fout.write('#include "{}.h"\n'.format(cfg['ProjectName']))

    if cfg.get('PDR', False) == False:
        # Monolithic IP
        fout.write(
            'void {}(input_t *x, score_t *score/*, score_t tree_scores[BDT::fn_classes(n_classes) * n_trees]*/){{\n'.format(cfg['ProjectName']))
        fout.write('\t#pragma HLS INTERFACE s_axilite port=return\n')
        fout.write('\t#pragma HLS INTERFACE m_axi depth=n_features bundle=x port=x\n')
        fout.write('\t#pragma HLS INTERFACE s_axilite port=x\n')
        fout.write('\t#pragma HLS INTERFACE m_axi depth=n_classes bundle=score port=score\n')
        fout.write('\t#pragma HLS INTERFACE s_axilite port=score\n')
        fout.write('\t\n')
        fout.write('\tinput_arr_t x_local;\n')
        fout.write('\t#pragma HLS array_partition variable=x_local\n')
        fout.write('\t\n')
        fout.write('\tscore_arr_t score_local;\n')
        fout.write('\t#pragma HLS array_partition variable=score_local\n')
        fout.write('\t\n')
        fout.write('\tpre_load: for (unsigned int i = 0; i < n_features; i++) {\n')
        fout.write('\t    #pragma HLS unroll\n')
        fout.write('\t    x_local[i] = x[i];\n')
        fout.write('\t}\n')
        fout.write('\t\n')
        fout.write('\tscore_t tree_scores[BDT::fn_classes(n_classes) * n_trees];\n')
        fout.write('\t\n')
        fout.write('\tbdt.decision_function(x_local, score_local, tree_scores);\n')
        fout.write('\t\n')
        fout.write('\tpost_store: for (unsigned int i = 0; i < n_classes; i++) {\n')
        fout.write('\t    #pragma HLS unroll\n')
        fout.write('\t    score[i] = score_local[i];\n')
        fout.write('\t}\n')
        fout.write('}')
        fout.close()
    else:
        # Reconfigurable set of IPs
        
        # ENUMERATOR
        fout.write(('void {}__enumerator(hls::stream<idless_input_arr_s_t> &input_stream, hls::stream<input_arr_s_t> &output_stream){{\n').format(cfg['ProjectName']))
        fout.write('\t#pragma HLS INTERFACE axis register port=input_stream\n')
        fout.write('\t#pragma HLS INTERFACE axis register port=output_stream\n')
        fout.write('\t#pragma HLS INTERFACE ap_ctrl_none port=return\n')
        fout.write('\tstatic BDT::Enumerator<max_parallel_samples, sample_id_size, n_features, idless_input_arr_s_t, input_arr_s_t> en;\n')
        fout.write('\ten.top_function(input_stream, output_stream);}\n')
        fout.write('\n')

        # BANK BUFFER IP
        for ibank in range(1, bank_count + 1):
            fout.write(('void {}__bank_buffer_{}(hls::stream<input_arr_s_t> &input_stream, hls::stream<input_arr_s_t> &output_stream, '+
                        'hls::stream<bank_command_s_t> &command_stream){{\n').format(cfg['ProjectName'], ibank))
            fout.write('\t#pragma HLS INTERFACE axis register port=input_stream\n')
            fout.write('\t#pragma HLS INTERFACE axis register port=output_stream\n')
            fout.write('\t#pragma HLS INTERFACE axis register port=command_stream\n')
            fout.write('\t#pragma HLS INTERFACE ap_ctrl_none port=return\n')
            fout.write('\tstatic BDT::Bank_buffer<input_arr_s_t, bank_command_s_t, max_parallel_samples, bank_count> bb({});\n'.format(ibank))
            fout.write('\tbb.top_function(input_stream, output_stream, command_stream);}\n')
            fout.write('\n')

        # TREE IPs
        for itree, trees in enumerate(ensemble_dict['trees']):
             for iclass, tree in enumerate(trees):
                fout.write(('void {}__tree_cl{}_{}(hls::stream<input_arr_s_t> &input_stream, ' +
                            'hls::stream<tree_score_s_t> &output_stream){{\n').format(cfg['ProjectName'], iclass, itree))
                fout.write('\t#pragma HLS INTERFACE axis register port=input_stream\n')
                fout.write('\t#pragma HLS INTERFACE axis register port=output_stream\n')
                fout.write('\t#pragma HLS INTERFACE ap_ctrl_none port=return\n')
                fout.write('\tinput_arr_s_t input;\n')
                fout.write('\tinput_stream >> input;\n')
                fout.write('\tauto output_data = bdt.trees[{}][{}].decision_function(input.data);\n'.format(itree, iclass))
                fout.write('\ttree_score_s_t output;\n')
                fout.write('\toutput.data = output_data;\n')
                fout.write('\toutput.keep = -1;\n')
                fout.write('\toutput.strb = 0;\n')
                fout.write('\toutput.id = input.id;\n')
                fout.write('\toutput.dest = {};\n'.format(iclass))
                fout.write('\toutput_stream << output;}\n')
                fout.write('\n')
        
        # IDLE TREE IP
        fout.write(('void {}__tree_idle(hls::stream<input_arr_s_t> &input_stream, ' +
                    'hls::stream<tree_score_s_t> &output_stream){{\n').format(cfg['ProjectName']))
        fout.write('\t#pragma HLS INTERFACE axis register port=input_stream\n')
        fout.write('\t#pragma HLS INTERFACE axis register port=output_stream\n')
        fout.write('\t#pragma HLS INTERFACE ap_ctrl_none port=return\n')
        fout.write('\tinput_arr_s_t input;\n')
        fout.write('\tinput_stream >> input;\n')
        fout.write('\ttree_score_s_t output;\n')
        fout.write('\toutput.data = 0;\n')
        fout.write('\toutput.keep = 0;\n')
        fout.write('\toutput.strb = 0;\n')
        fout.write('\toutput.id = input.id;\n')
        fout.write('\toutput.dest = -1;\n')
        fout.write('\toutput_stream << output;}\n')
        fout.write('\n')

        # VOTE BUFFER IP
        fout.write(('void {}__vote_buffer(hls::stream<tree_score_s_t> &input_stream, ' +
                    'hls::stream<tree_score_s_t> &output_stream, bool &irq){{\n').format(cfg['ProjectName']))
        fout.write('\t#pragma HLS INTERFACE axis register port=input_stream\n')
        fout.write('\t#pragma HLS INTERFACE axis register port=output_stream\n')
        fout.write('\t	#pragma HLS INTERFACE ap_none register port=irq\n')
        fout.write('\t#pragma HLS INTERFACE ap_ctrl_none port=return\n')
        fout.write('\tstatic BDT::Vote_buffer<tree_score_s_t> vb;\n')
        fout.write('\tvb.top_function(input_stream, output_stream, irq);}\n')
        fout.write('\n')        

        # VOTING STATION IPs
        for iclass in range(class_count):
            fout.write(('void {}__voting_station_cl{}(hls::stream<tree_score_s_t>  &input_score_stream, ' +
                            'hls::stream<class_score_s_t> &output_score_stream){{\n').format(cfg['ProjectName'], iclass))
            fout.write('\t#pragma HLS INTERFACE axis register port=input_score_stream\n')
            fout.write('\t#pragma HLS INTERFACE axis register port=output_score_stream\n')
            fout.write('\t#pragma HLS INTERFACE ap_ctrl_none port=return\n')
            fout.write(('\tstatic BDT::Voting_station<n_classes, tree_score_s_t, class_score_s_t, score_t, max_parallel_samples> '+
                        'vs({iclass}, bdt.init_predict[{iclass}], bdt.normalisation);\n').format(iclass=iclass))
            fout.write('\tvs.top_function(input_score_stream, output_score_stream);}\n')
            fout.write('\n')
    
    ###################
    # parameters.h
    ###################

    fout = open('{}/firmware/parameters.h'.format(cfg['OutputDir']), 'w')
    fout.write('#ifndef BDT_PARAMS_H__\n#define BDT_PARAMS_H__\n\n')
    fout.write('#include "BDT.h"\n')
    fout.write('#include "ap_fixed.h"\n\n')
    if cfg.get('PDR', False) == True:
            fout.write('#include "utils.h"\n')
            fout.write('#include "ap_axi_sdata.h"\n\n')

    fout.write('static const int n_trees = {};\n'.format(
        ensemble_dict['n_trees']))
    fout.write('static const int max_depth = {};\n'.format(
        ensemble_dict['max_depth']))
    fout.write('static const int n_features = {};\n'.format(
        ensemble_dict['n_features']))
    fout.write('static const int n_classes = {};\n'.format(
        ensemble_dict['n_classes']))
    fout.write('typedef {} input_t;\n'.format(cfg['Precision']))
    fout.write('typedef input_t input_arr_t[n_features];\n')
    fout.write('typedef {} score_t;\n'.format(cfg['Precision']))
    fout.write('typedef score_t score_arr_t[n_classes];\n')
    # TODO score_arr_t
    fout.write('typedef input_t threshold_t;\n\n')

    if cfg.get('PDR', False) == True:
        # TODO: Allow max_parallel_sample configuration
        max_parallel_samples = 6
        fout.write('static const int max_parallel_samples = {};\n'.format(max_parallel_samples))
        fout.write('static const int bank_count = {};\n'.format(bank_count))
        fout.write('static const int sample_id_size = bitsizeof(max_parallel_samples);\n')
        fout.write('static const int bank_address_size = bitsizeof(bank_count + 1);\n')
        fout.write('typedef hls::axis<ap_uint<8>, 0, 0, bank_address_size> bank_command_s_t;\n')
        fout.write('typedef hls::axis<input_arr_t, 0, 0, 0> idless_input_arr_s_t;\n')
        fout.write('typedef hls::axis<input_arr_t, 0, sample_id_size, 0> input_arr_s_t;\n')
        fout.write('typedef hls::axis<score_t, 0, sample_id_size, bitsizeof(n_classes)> tree_score_s_t;\n')
        fout.write('typedef hls::axis<score_t, 0, sample_id_size, 0> class_score_s_t;\n\n')
    
    tree_fields = ['feature', 'threshold', 'value',
                   'children_left', 'children_right', 'parent']

    fout.write(
        "static const BDT::BDT<n_trees, max_depth, n_classes, input_arr_t, score_t, threshold_t> bdt = \n")
    fout.write("{ // The struct\n")
    newline = "\t" + str(ensemble_dict['norm']) + ", // The normalisation\n"
    fout.write(newline)
    newline = "\t{"
    if ensemble_dict['n_classes'] > 2:
        for iip, ip in enumerate(ensemble_dict['init_predict']):
            if iip < len(ensemble_dict['init_predict']) - 1:
                newline += '{},'.format(ip)
            else:
                newline += '{}}}, // The init_predict\n'.format(ip)
    else:
        newline += str(ensemble_dict['init_predict'][0]) + '},\n'
    fout.write(newline)
    fout.write("\t{ // The array of trees\n")
    # loop over trees
    for itree, trees in enumerate(ensemble_dict['trees']):
        fout.write('\t\t{ // trees[' + str(itree) + ']\n')
        # loop over classes
        for iclass, tree in enumerate(trees):
            fout.write('\t\t\t{ // [' + str(iclass) + ']\n')
            # loop over fields
            for ifield, field in enumerate(tree_fields):
                newline = '\t\t\t\t{'
                newline += ','.join(map(str, tree[field]))
                newline += '}'
                if ifield < len(tree_fields) - 1:
                    newline += ','
                newline += '\n'
                fout.write(newline)
            newline = '\t\t\t}'
            if iclass < len(trees) - 1:
                newline += ','
            newline += '\n'
            fout.write(newline)
        newline = '\t\t}'
        if itree < ensemble_dict['n_trees'] - 1:
            newline += ','
        newline += '\n'
        fout.write(newline)
    fout.write('\t}\n};')

    fout.write('\n#endif')
    fout.close()

    #######################
    # myproject.h
    #######################

    fout = open(
        '{}/firmware/{}.h'.format(cfg['OutputDir'], cfg['ProjectName']), 'w')
    fout.write('#ifndef {}_H__\n#define {}_H__\n\n'.format(cfg['ProjectName'].upper(), cfg['ProjectName'].upper()))
    fout.write('#include "BDT.h"\n')
    fout.write('#include "parameters.h"\n')
    if cfg.get('PDR', False) == True:
        fout.write('#include "hls_stream.h"\n')

    if cfg.get('PDR', False) == False:
        # Monolithic IP
        fout.write(
            'void {}(input_t *x, score_t *score/*, score_t tree_scores[BDT::fn_classes(n_classes) * n_trees]*/);\n'.format(cfg['ProjectName']))
    else:
        # Reconfigurable set of IPs
        
        # ENUMERTOR
        fout.write(('void {}__enumerator(hls::stream<idless_input_arr_s_t> &input_stream, hls::stream<input_arr_s_t> &output_stream);\n'.format(cfg['ProjectName'])))    

        # BANK BUFFER IP
        for ibank in range(1, bank_count + 1):
            fout.write(('void {}__bank_buffer_{}(hls::stream<input_arr_s_t> &input_stream, hls::stream<input_arr_s_t> &output_stream, '+
                        'hls::stream<bank_command_s_t> &command_stream);\n').format(cfg['ProjectName'], ibank))

        # TREE IPs
        for itree, trees in enumerate(ensemble_dict['trees']):
             for iclass, tree in enumerate(trees):
                fout.write(('void {}__tree_cl{}_{}(hls::stream<input_arr_s_t> &input_stream, ' +
                            'hls::stream<tree_score_s_t> &output_stream);\n').format(cfg['ProjectName'], iclass, itree))

        # IDLE TREE IP
        fout.write(('void {}__tree_idle(hls::stream<input_arr_s_t> &input_stream, ' +
                    'hls::stream<tree_score_s_t> &output_stream);\n').format(cfg['ProjectName'])) 

        # VOTE BUFFER IP
        fout.write(('void {}__vote_buffer(hls::stream<tree_score_s_t> &input_stream, ' +
                    'hls::stream<tree_score_s_t> &output_stream, bool &irq);\n').format(cfg['ProjectName']))

        # VOTING STATION IPs
        class_count = 1
        for itree, trees in enumerate(ensemble_dict['trees']):
             if len(trees) > class_count:
                 class_count = len(trees)

        for iclass in range(class_count):
            fout.write(('void {}__voting_station_cl{}(hls::stream<tree_score_s_t>  &input_score_stream, ' +
                            'hls::stream<class_score_s_t> &output_score_stream);\n').format(cfg['ProjectName'], iclass))

    fout.write('\n#endif')
    fout.close()

    #######################
    # myproject_test.cpp
    #######################

    if cfg.get('PDR', False) == False:
        f = open(os.path.join(filedir, 'hls-template/myproject_test.cpp'))
    else:
        f = open(os.path.join(filedir, 'hls-template/myproject_pdr_test.cpp'))
    
    fout = open(
        '{}/{}_test.cpp'.format(cfg['OutputDir'], cfg['ProjectName']), 'w')

    for line in f.readlines():
        indent = ' ' * (len(line) - len(line.lstrip(' ')))

        # Insert numbers
        if 'myproject' in line:
            newline = line.replace('myproject', cfg['ProjectName'])
        elif '//hls-fpga-machine-learning insert data' in line:
            newline = line
            newline += '      std::vector<float>::const_iterator in_begin = in.cbegin();\n'
            newline += '      std::vector<float>::const_iterator in_end;\n'
            newline += '      input_arr_t x;\n'
            newline += '      in_end = in_begin + ({});\n'.format(
                ensemble_dict['n_features'])
            if cfg.get('PDR', False) == False: 
                newline += '      std::copy(in_begin, in_end, x);\n'
            else:
                newline += '      std::copy(in_begin, in_end, in_pkt.data);\n'
            newline += '      in_begin = in_end;\n'
            # brace-init zeros the array out because we use std=c++0x
            newline += '      score_arr_t score{};\n'
            newline += '      score_t tree_scores[BDT::fn_classes(n_classes) * n_trees]{};\n'
            # but we can still explicitly zero out if you want
            newline += '      std::fill_n(score, {}, 0.);\n'.format(
                ensemble_dict['n_classes'])
            if cfg.get('PDR', False) == True:
                newline += '      sample_stream[0] << in_pkt;\n'
        elif '//hls-fpga-machine-learning insert zero' in line:
            newline = line
            newline += '    input_arr_t x;\n'
            newline += '    std::fill_n(x, {}, 0.);\n'.format(
                ensemble_dict['n_features'])
            newline += '    score_arr_t score{};\n'
            newline += '    score_t tree_scores[BDT::fn_classes(n_classes) * n_trees]{};\n'
            newline += '    std::fill_n(score, {}, 0.);\n'.format(
                ensemble_dict['n_classes'])
        elif '//hls-fpga-machine-learning insert top-level-function' in line:
            newline = line
            if cfg.get('PDR', False) == False: 
                top_level = indent + \
                    '{}(x, score/*, tree_scores*/);\n'.format(cfg['ProjectName'])
            else:
                # TODO: Use all the bank buffers and test reconfiguration
                # TODO: Use vote buffers
                top_level =     indent + 'bank_command_s_t command_pkt;\n'
                top_level +=    indent + 'command_pkt.data = 0b00111111;\n'
                top_level +=    indent + 'command_pkt.dest = 0;\n'
                top_level +=    indent + 'bank_command_stream[0] << command_pkt;\n'
                top_level +=    indent + '{name}__bank_buffer_1(sample_stream[0], bank_stream[0], bank_command_stream[0]);\n'.format(name=cfg['ProjectName'])
                top_level +=    indent + 'axis_crossbar<input_arr_s_t, 1, n_trees * n_classes>(bank_stream, tree_stream);\n'
                for itree, trees in enumerate(ensemble_dict['trees']):
                    for iclass, tree in enumerate(trees):
                        top_level +=  (indent + '{name}__tree_cl{iclass}_{itree}(' + \
                                'tree_stream[{itree} * n_classes + {iclass}], ' + \
                                'aux_score_stream[{itree} * n_classes + {iclass}]);\n' + \
                            indent + 'tree_scores[{itree} * n_classes + {iclass}] = ' + \
                                'tee<tree_score_s_t, score_t>(' + \
                                    'aux_score_stream[{itree} * n_classes + {iclass}], ' + \
                                    'score_stream[{itree} * n_classes + {iclass}]);\n').format(name=cfg['ProjectName'],
                                    itree=itree,
                                    iclass=iclass)
                top_level +=    indent + 'axis_crossbar<tree_score_s_t, n_trees * n_classes, n_classes>(score_stream, in_class_stream);\n'
                for iclass in range(class_count):
                    top_level += (indent + 'while(!in_class_stream[{iclass}].empty()) {{\n' + \
                        indent + '  {name}__voting_station_cl{iclass}(in_class_stream[{iclass}], out_class_stream[{iclass}]);\n' + \
                        indent + '}}\n').format(iclass=iclass, name=cfg['ProjectName'])
            newline += top_level
        elif '//hls-fpga-machine-learning insert predictions' in line:
            newline = line
            newline += indent + \
                'for(int i = 0; i < {}; i++) {{\n'.format(
                    ensemble_dict['n_classes'])
            newline += indent + '  std::cout << pr[i] << " ";\n'
            newline += indent + '}\n'
            newline += indent + 'std::cout << std::endl;\n'
        elif '//hls-fpga-machine-learning insert tb-output' in line:
            newline = line
            newline += indent + \
                'for(int i = 0; i < {}; i++) {{\n'.format(
                    ensemble_dict['n_classes'])
            newline += indent + '  fout << score[i] << " ";\n'
            newline += indent + '}\n'
        elif '//hls-fpga-machine-learning insert output' in line or '//hls-fpga-machine-learning insert quantized' in line:
            newline = line
            newline += indent + \
                'for(int i = 0; i < {}; i++) {{\n'.format(
                    ensemble_dict['n_classes'])
            newline += indent + '  std::cout << score[i] << " ";\n'
            newline += indent + '}\n'
            newline += indent + 'std::cout << std::endl;\n'
        elif '//hls-fpga-machine-learning insert final-round' in line:
            newline = line
            if cfg.get('PDR', False) == True:
                for iclass in range(class_count):
                    newline += (indent + \
                        '{name}__voting_station_cl{iclass}(in_class_stream[{iclass}], out_class_stream[{iclass}]);\n').format(iclass=iclass, name=cfg['ProjectName'])
        elif '//hls-fpga-machine-learning insert stream-check' in line:
            newline = line
            if cfg.get('PDR', False) == True:
                newline += indent
                for iclass in range(class_count):
                    newline += '!out_class_stream[{}].empty()'.format(iclass)
                    if iclass < class_count - 1:
                        newline += ' && '
                    else:
                        newline += '\n'
        else:
            newline = line
        fout.write(newline)
    # fout.write('#include "BDT.h"\n')
    # fout.write('#include "firmware/parameters.h"\n')
    # fout.write('#include "firmware/{}.h"\n'.format(cfg['ProjectName']))

    #fout.write('int main(){\n')
    #fout.write('\tinput_arr_t x = {{{}}};\n'.format(str([0] * ensemble_dict['n_features'])[1:-1]));
    #fout.write('\tscore_arr_t score;\n')
    #fout.write('\t{}(x, score);\n'.format(cfg['ProjectName']))
    #fout.write('\tfor(int i = 0; i < n_classes; i++){\n')
    #fout.write('\t\tstd::cout << score[i] << ", ";\n\t}\n')
    #fout.write('\tstd::cout << std::endl;\n')
    #fout.write('\treturn 0;\n}')
    # fout.close()

    fout.close()

    #######################
    # build_prj.tcl
    #######################

    bdtdir = os.path.abspath(os.path.join(filedir, "../bdt_utils"))
    relpath = os.path.relpath(bdtdir, start=cfg['OutputDir'])

    if cfg.get('PDR', False) == False:
        f = open(os.path.join(filedir, 'hls-template/build_prj.tcl'), 'r')
    else:
        f = open(os.path.join(filedir, 'hls-template/build_pdr_prj.tcl'), 'r')
    fout = open('{}/build_prj.tcl'.format(cfg['OutputDir']), 'w')

    for line in f.readlines():

        line = line.replace('nnet_utils', relpath)
        line = line.replace('myproject', cfg['ProjectName'])

        # if 'set_top' in line:
        #    line = line.replace('myproject', '{}_decision_function'.format(cfg['ProjectName']))
        if 'set_part {xc7vx690tffg1927-2}' in line:
            line = 'set_part {{{}}}\n'.format(cfg['XilinxPart'])
        elif 'create_clock -period 5 -name default' in line:
            line = 'create_clock -period {} -name default\n'.format(
                cfg['ClockPeriod'])
        # Remove some lines
        elif ('weights' in line) or ('-tb firmware/weights' in line):
            line = ''
        elif '##hls-fpga-machine-learning insert individual-ips' in line:
            line = ''
            if cfg.get('PDR', False) == True:
                for ibank in range(1, bank_count + 1):
                    line += 'source build_pdr_ips/bank_buffer_{}.tcl\n'.format(ibank)
                for itree, trees in enumerate(ensemble_dict['trees']):
                    for iclass, tree in enumerate(trees): 
                        line += 'source build_pdr_ips/tree_cl{}_{}.tcl\n'.format(iclass, itree)
                for iclass in range(class_count):
                    line += 'source build_pdr_ips/voting_station_cl{}.tcl\n'.format(iclass)

        fout.write(line)
    f.close()
    fout.close()

    if cfg.get('PDR', False) == True:
        os.mkdir('{}/build_pdr_ips'.format(cfg['OutputDir']))
        for ibank in range(1, bank_count + 1):
            f = open(os.path.join(filedir, 'hls-template/build_pdr_ip.tcl'), 'r')
            fout = open('{}/build_pdr_ips/bank_buffer_{}.tcl'.format(cfg['OutputDir'], ibank), 'w')

            for line in f.readlines():
                line = line.replace('myproject', cfg['ProjectName'])
                line = line.replace('the_ip', 'bank_buffer_{}'.format(ibank))

                if 'set_part {xc7vx690tffg1927-2}' in line:
                    line = 'set_part {{{}}}\n'.format(cfg['XilinxPart'])
                elif 'create_clock -period 5 -name default' in line:
                    line = 'create_clock -period {} -name default\n'.format(
                        cfg['ClockPeriod'])

                fout.write(line)

            f.close()
            fout.close()
        
        for itree, trees in enumerate(ensemble_dict['trees']):
            for iclass, tree in enumerate(trees): 
                f = open(os.path.join(filedir, 'hls-template/build_pdr_ip.tcl'), 'r')
                fout = open('{}/build_pdr_ips/tree_cl{}_{}.tcl'.format(cfg['OutputDir'], iclass, itree), 'w')

                for line in f.readlines():
                    line = line.replace('myproject', cfg['ProjectName'])
                    line = line.replace('the_ip', 'tree_cl{}_{}'.format(iclass, itree))

                    if 'set_part {xc7vx690tffg1927-2}' in line:
                        line = 'set_part {{{}}}\n'.format(cfg['XilinxPart'])
                    elif 'create_clock -period 5 -name default' in line:
                        line = 'create_clock -period {} -name default\n'.format(
                            cfg['ClockPeriod'])

                    fout.write(line)

                f.close()
                fout.close()

        for iclass in range(class_count):
            f = open(os.path.join(filedir, 'hls-template/build_pdr_ip.tcl'), 'r')
            fout = open('{}/build_pdr_ips/voting_station_cl{}.tcl'.format(cfg['OutputDir'], iclass), 'w')

            for line in f.readlines():
                line = line.replace('myproject', cfg['ProjectName'])
                line = line.replace('the_ip', 'voting_station_cl{}'.format(iclass))

                if 'set_part {xc7vx690tffg1927-2}' in line:
                    line = 'set_part {{{}}}\n'.format(cfg['XilinxPart'])
                elif 'create_clock -period 5 -name default' in line:
                    line = 'create_clock -period {} -name default\n'.format(
                        cfg['ClockPeriod'])

                fout.write(line)

            f.close()
            fout.close()

        f = open(os.path.join(filedir, 'hls-template/build_pdr_ip.tcl'), 'r')
        fout = open('{}/build_pdr_ips/tree_idle.tcl'.format(cfg['OutputDir']), 'w')

        for line in f.readlines():
            line = line.replace('myproject', cfg['ProjectName'])
            line = line.replace('the_ip', 'tree_idle')

            if 'set_part {xc7vx690tffg1927-2}' in line:
                line = 'set_part {{{}}}\n'.format(cfg['XilinxPart'])
            elif 'create_clock -period 5 -name default' in line:
                line = 'create_clock -period {} -name default\n'.format(
                    cfg['ClockPeriod'])

            fout.write(line)

        f.close()
        fout.close()

        f = open(os.path.join(filedir, 'hls-template/build_pdr_ip.tcl'), 'r')
        fout = open('{}/build_pdr_ips/vote_buffer.tcl'.format(cfg['OutputDir']), 'w')

        for line in f.readlines():
            line = line.replace('myproject', cfg['ProjectName'])
            line = line.replace('the_ip', 'vote_buffer')

            if 'set_part {xc7vx690tffg1927-2}' in line:
                line = 'set_part {{{}}}\n'.format(cfg['XilinxPart'])
            elif 'create_clock -period 5 -name default' in line:
                line = 'create_clock -period {} -name default\n'.format(
                    cfg['ClockPeriod'])

            fout.write(line)

        f.close()
        fout.close()

        f = open(os.path.join(filedir, 'hls-template/build_pdr_ip.tcl'), 'r')
        fout = open('{}/build_pdr_ips/enumerator.tcl'.format(cfg['OutputDir']), 'w')

        for line in f.readlines():
            line = line.replace('myproject', cfg['ProjectName'])
            line = line.replace('the_ip', 'enumerator')

            if 'set_part {xc7vx690tffg1927-2}' in line:
                line = 'set_part {{{}}}\n'.format(cfg['XilinxPart'])
            elif 'create_clock -period 5 -name default' in line:
                line = 'create_clock -period {} -name default\n'.format(
                    cfg['ClockPeriod'])

            fout.write(line)

        f.close()
        fout.close()
    #######################
    # build_tree_wrapper.tcl
    #######################

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
    # build_system_bd.tcl
    #######################

    if cfg.get('PDR', False) == True:
        f = open(os.path.join(filedir, 'system-template/top_system.tcl'), 'r')
        fout = open('{}/build_system_bd.tcl'.format(cfg['OutputDir']), 'w')
        for line in f.readlines():

            precision = int(cfg['Precision'].split('<')[1].split(',')[0])
            
            if '## hls-fpga-machine-learning insert project-name' in line:
                line = line.replace('## hls-fpga-machine-learning insert project-name', '{}_system'.format(cfg['ProjectName']))
            elif '## hls-fpga-machine-learning insert project-part' in line:
                line = line.replace('## hls-fpga-machine-learning insert project-part', cfg['XilinxPart'])
            elif '## hls-fpga-machine-learning insert project-board' in line:
                line = line.replace('## hls-fpga-machine-learning insert project-board', cfg['XilinxBoard'])
            elif '## hls-fpga-machine-learning insert sample_length' in line:
                line = line.replace('## hls-fpga-machine-learning insert sample_length', str(int((2**math.ceil(math.log(precision, 2)))*ensemble_dict['n_features'])))
            elif '## hls-fpga-machine-learning insert n-classes' in line:
                line = line.replace('## hls-fpga-machine-learning insert n-classes', str(int(class_count)))
            elif '## hls-fpga-machine-learning insert result_lenght' in line:
                line = line.replace('## hls-fpga-machine-learning insert result_lenght', str(int(8*math.ceil(precision)/8)))
            elif '## hls-fpga-machine-learning insert output_length' in line:
                line = line.replace('## hls-fpga-machine-learning insert output_length', str(int(2**math.ceil(math.log(8*(math.ceil(precision)/8), 2)))))
            elif '## hls-fpga-machine-learning insert n-banks' in line:
                line = line.replace('## hls-fpga-machine-learning insert n-banks', str(int(bank_count)))
            elif '## hls-fpga-machine-learning insert n-trees-per-bank' in line:
                line = line.replace('## hls-fpga-machine-learning insert n-trees-per-bank', str(int(cfg['TreesPerBank'])))
            elif '## hls-fpga-machine-learning insert id-length' in line:
                line = line.replace('## hls-fpga-machine-learning insert id-length', str(int(math.ceil(math.log(int(max_parallel_samples), 2))+1)))
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
    # build_tree_wrapper.tcl
    #######################

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

    if cfg.get('PDR', False) == True:
        f = open(os.path.join(filedir, 'system-template/static_shell.tcl'), 'r')
        fout = open('{}/synth_static_shell.tcl'.format(cfg['OutputDir']), 'w')
        for line in f.readlines():

            if '## hls-fpga-machine-learning insert project-name' in line:
                line = line.replace('## hls-fpga-machine-learning insert project-name', '{}_system'.format(cfg['ProjectName']))

            fout.write(line)
        f.close()
        fout.close()

    #######################
    # design.tcl
    #######################

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
