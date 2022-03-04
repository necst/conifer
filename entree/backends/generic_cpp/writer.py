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
import re
from shutil import copyfile

def clean(varStr):
    return re.sub('\W|^(?=\d)','_', varStr)

def write(ensemble_dict, cfg):

    filedir = os.path.dirname(os.path.abspath(__file__))

    tree_fields = ['feature', 'threshold', 'value',
                'children_left', 'children_right', 'parent']
    
    n_total_nodes = sum(map(lambda t: len(t[tree_fields[0]]), [tree for class_group in ensemble_dict['trees'] for tree in class_group]))

    os.makedirs('{}'.format(cfg['OutputDir']))
    copyfile('{}/firmware/DTEnsemble.h'.format(filedir),
             '{}/DTEnsemble.h'.format(cfg['OutputDir']))
    dt_name = clean(cfg['ProjectName'])
    
    ###################
    # parameters.h
    ###################

    fout = open('{}/{}.h'.format(cfg['OutputDir'], 'parameters'), 'w')
    fout.write('#ifndef {}_HPP__\n'.format(dt_name.upper()))
    fout.write('#define {}_HPP__\n'.format(dt_name.upper()))
    fout.write('\n')
    fout.write('#include <string_view>\n')
    fout.write('namespace {\n')
    fout.write('namespace {}_description {{\n'.format(dt_name))

    fout.write('static constexpr const std::string_view node_label = "{}";\n'.format(dt_name));

    fout.write('static const int n_total_nodes = {};\n'.format(
        n_total_nodes))
    fout.write('static const int n_trees = {};\n'.format(
        ensemble_dict['n_trees']))
    fout.write('static const int n_features = {};\n'.format(
        ensemble_dict['n_features']))
    fout.write('enum Feature {\n')
    fout.write(',\n'.join(
            map(
                lambda i: '\t'+clean(str(i)), 
                cfg.get('FeatureList', [])
            )
        ) + '\n')
    fout.write('};\n')
    fout.write('#ifdef ENTREE_REFLECTION_ENABLE\n')
    fout.write('#ifndef ENTREE_REFLECTION_LEVEL\n')
    fout.write('#define ENTREE_REFLECTION_LEVEL 1\n')
    fout.write('#endif\n')
    fout.write('#if (ENTREE_REFLECTION_LEVEL > 0)\n')
    fout.write('static const std::string_view feature_labels[] = {\n')
    fout.write(',\n'.join(
        map(
            lambda i: '\t"'+str(i)+'"',
            cfg.get('FeatureList', [])
        )
    ) + '\n')
    fout.write('};\n')
    fout.write('#endif\n')
    fout.write('#endif\n')
    fout.write('static const int n_classes = {};\n'.format(
        ensemble_dict['n_classes']))
    fout.write('enum Class {\n')
    fout.write(',\n'.join(
            map(
                lambda i: '\t'+clean(str(i))+'', 
                ensemble_dict.get('classes', [])
            )
        ) + '\n')
    fout.write('};\n')
    fout.write('#ifdef ENTREE_REFLECTION_ENABLE\n')
    fout.write('#ifndef ENTREE_REFLECTION_LEVEL\n')
    fout.write('#define ENTREE_REFLECTION_LEVEL 1\n')
    fout.write('#endif\n')
    fout.write('#if (ENTREE_REFLECTION_LEVEL > 0)\n')
    fout.write('static const std::string_view class_labels[] = {\n')
    fout.write(',\n'.join(
        map(
            lambda i: '\t"'+str(i)+'"',
            ensemble_dict.get('classes', [])
        )
    ) + '\n')
    fout.write('};\n')
    fout.write('#endif\n')
    fout.write('#endif\n')
    fout.write('typedef {} input_t;\n'.format(cfg['Precision']))
    fout.write('typedef input_t input_arr_t[n_features];\n')
    fout.write('typedef {} score_t;\n'.format("int" if ensemble_dict.get('direct', False) else cfg['Precision']))
    fout.write('typedef score_t score_arr_t[n_classes];\n')
    fout.write('typedef input_t threshold_t;\n\n')
    
    if any('rules' in tree.keys() for trees in ensemble_dict['trees'] for tree in trees):
        fout.write('#ifdef ENTREE_REFLECTION_ENABLE\n')
        fout.write('#ifndef ENTREE_REFLECTION_LEVEL\n')
        fout.write('#define ENTREE_REFLECTION_LEVEL 1\n')
        fout.write('#endif\n')
        fout.write('#if (ENTREE_REFLECTION_LEVEL > 1)\n')
        fout.write('static const std::string_view rules = "\\n\\\n'.format(dt_name.upper()))
        fout.write('FEATURES: [{}]\\n\\\n'.format(','.join(map(
                lambda i: '\''+clean(str(i))+'\'', 
                cfg.get('FeatureList', [])
            )
        )))
        fout.write('CLASSES: [{}]\\n\\\n'.format(','.join(map(
                lambda i: '\''+clean(str(i))+'\'', 
                ensemble_dict.get('classes', [])
            )
        )))
        for itree, trees in enumerate(ensemble_dict['trees']):
            for iclass, tree in enumerate(trees):
                if 'rules' in tree.keys():
                    fout.write('TREE #{}-{}:\\n\\\n'.format(itree, iclass))
                    fout.write(tree['rules'].replace('\n', '\\n\\\n'))
        fout.write('";\n')
        fout.write('#endif\n')
        fout.write('#endif\n')

    fout.write(
        "static const entree::DTEnsemble<node_label, n_total_nodes, n_trees, n_classes, input_arr_t, score_t, threshold_t, {}> bdt = \n".format("true" if ensemble_dict.get('direct', False) else "false"))
    fout.write("{ // The struct\n")
    newline = "\t" + str(ensemble_dict.get('norm', 1)) + ", // The normalisation\n"
    fout.write(newline)
    newline = "\t{"
    if ensemble_dict['n_classes'] > 2 or ensemble_dict.get('direct', False):
        for iip, ip in enumerate(ensemble_dict['init_predict']):
            if iip < len(ensemble_dict['init_predict']) - 1:
                newline += '{},'.format(ip)
            else:
                newline += '{}}}, // The init_predict\n'.format(ip)
    else:
        newline += str(ensemble_dict['init_predict'][0]) + '},\n'
    fout.write(newline)
    fout.write("\t{" + ", ".join(["{" + ", ".join([str(len(tree['parent'])) for tree in trees]) + "}" for trees in ensemble_dict['trees']]) + "},\n")
    for ifield, field in enumerate(tree_fields):
        fout.write("\t{" + ", ".join([str(value) for trees in ensemble_dict['trees'] for tree in trees for value in tree[field]]) + "}")
        if ifield < len(tree_fields) - 1:
            fout.write(",")
        fout.write("\n")
    fout.write('};\n')

    fout.write('}\n')
    fout.write('}\n')
    fout.write('\n#endif')
    fout.close()

def auto_config():
    config = {'ProjectName': 'my_prj',
              'OutputDir': 'my-entree-prj',
              'Precision': 'double',
              'DisablePadding': True}
    return config


def decision_function(X, config, trees=False):
    raise Error("Not supported!")


def sim_compile(config):
    return


def build(config, reset=False, csim=False, synth=True, cosim=False, export=False):
    raise Error("Not supported!")
