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

def clean(varStr):
    return re.sub('\W|^(?=\d)','_', varStr)

def write(ensemble_dict, cfg):

    filedir = os.path.dirname(os.path.abspath(__file__))

    tree_count = 0
    class_count = 1
    for itree, trees in enumerate(ensemble_dict['trees']):
        tree_count += len(trees)
        if len(trees) > class_count:
            class_count = len(trees)

    os.makedirs('{}'.format(cfg['OutputDir']))

    dt_name = clean(cfg['ProjectName'])
    
    ###################
    # parameters.h
    ###################

    fout = open('{}/{}.h'.format(cfg['OutputDir'], 'parameters'), 'w')
    fout.write('#ifndef {}_HPP__\n'.format(dt_name.upper()))
    fout.write('#define {}_HPP__\n'.format(dt_name.upper()))
    fout.write('\n')
    fout.write('namespace {}_description {{\n'.format(dt_name))

    fout.write('static constexpr const std::string_view node_label = "{}";\n'.format(dt_name));

    fout.write('#ifdef ENTREE_REFLECTION_ENABLE\n')
    fout.write('#ifndef ENTREE_REFLECTION_LEVEL\n')
    fout.write('#define ENTREE_REFLECTION_LEVEL 1\n')
    fout.write('#endif\n')
    fout.write('#if (ENTREE_REFLECTION_LEVEL > 0)\n')
    fout.write('static const char* feature_labels[] = {\n')
    fout.write(',\n'.join(
        map(
            lambda i: '\t"'+str(i)+'"',
            cfg.get('FeatureList', [])
        )
    ) + '\n')
    fout.write('};\n')
    fout.write('static const char* class_labels[] = {\n')
    fout.write(',\n'.join(
        map(
            lambda i: '\t"'+str(i)+'"',
            cfg.get('ClassList', [])
        )
    ) + '\n')
    fout.write('};\n')
    fout.write('#endif\n')
    fout.write('#endif\n')
    fout.write('static const int n_trees = {};\n'.format(
        ensemble_dict['n_trees']))
    fout.write('static const int max_depth = {};\n'.format(
        ensemble_dict['max_depth']))
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
    fout.write('static const int n_classes = {};\n'.format(
        ensemble_dict['n_classes']))
    fout.write('enum Class {\n')
    fout.write(',\n'.join(
            map(
                lambda i: '\t'+clean(str(i))+'', 
                cfg.get('ClassList', [])
            )
        ) + '\n')
    fout.write('};\n')
    fout.write('typedef {} input_t;\n'.format(cfg['Precision']))
    fout.write('typedef input_t input_arr_t[n_features];\n')
    fout.write('typedef {} score_t;\n'.format(cfg['Precision']))
    fout.write('typedef score_t score_arr_t[n_classes];\n')
    # TODO score_arr_t
    fout.write('typedef input_t threshold_t;\n\n')
    
    if any('rules' in tree.keys() for trees in ensemble_dict['trees'] for tree in trees):
        fout.write('#ifdef ENTREE_REFLECTION_ENABLE\n')
        fout.write('#ifndef ENTREE_REFLECTION_LEVEL\n')
        fout.write('#define ENTREE_REFLECTION_LEVEL 1\n')
        fout.write('#endif\n')
        fout.write('#if (ENTREE_REFLECTION_LEVEL > 1)\n')
        fout.write('static const std::string_view rules = "\\n\\\n'.format(dt_name.upper()))
        for itree, trees in enumerate(ensemble_dict['trees']):
            for iclass, tree in enumerate(trees):
                if 'rules' in tree.keys():
                    fout.write('TREE #{}-{}:\\n\\\n'.format(itree, iclass))
                    fout.write(tree['rules'].replace('\n', '\\n\\\n'))
        fout.write('";\n')
        fout.write('#endif\n')
        fout.write('#endif\n')


    tree_fields = ['feature', 'threshold', 'value',
                   'children_left', 'children_right', 'parent']

    fout.write(
        "static const entree::BDT<node_label, n_trees, max_depth, n_classes, input_arr_t, score_t, threshold_t> bdt = \n")
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
    fout.write('\t}\n};\n')

    fout.write('}\n')
    fout.write('\n#endif')
    fout.close()

def auto_config():
    config = {'ProjectName': 'my_prj',
              'OutputDir': 'my-entree-prj',
              'Precision': 'double'}
    return config


def decision_function(X, config, trees=False):
    raise Error("Not supported!")


def sim_compile(config):
    return


def build(config, reset=False, csim=False, synth=True, cosim=False, export=False):
    raise Error("Not supported!")
