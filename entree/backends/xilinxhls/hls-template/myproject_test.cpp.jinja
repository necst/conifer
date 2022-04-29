// cfg
// ensemble_dict['n_features']
// cfg_get=cfg.get('PDR', False)

    {%- for line in file %}
        {%- set indent = ' ' * (line|length - line|trim|length) %}
        {#- Insert numbers #}
        {%- if 'myproject' in line %}
            {{'myproject %s'|format(cfg['ProjectName'])}}
        {%- elif '//hls-fpga-machine-learning insert data' in line %}
            {%- set newline = line %}
            {%- set newline ="%s      std::vector<float>::const_iterator in_begin = in.cbegin(); \n"|format(newline) %}
            {%- set newline ="%s      std::vector<float>::const_iterator in_end;\n"|format(newline) %}
            {%- set newline ="%s      input_arr_t x;\n"|format(newline) %}
            {%- set newline ="%s      in_end = in_begin + (%d);\n"|format(newline,ensemble_dict['n_feures']) %}
            {%- if not cfg_get %}
                {%- set newline ="%s      std::copy(in_begin, in_end, x);\n"|format(newline) %}
            {%- else %}
                {%- set newline ="%s      std::copy(in_begin, in_end, in_pkt.data);\n"|format(newline) %}
            {%- endif %}
            {%- set newline ="%s      in_begin = in_end;\n"|format(newline) %}
            {#- brace-init zeros the array out because we use std=c++0x #}
            {%- set newline ="%s      score_arr_t score%d;\n"|format(newline,ensemble_dict['n_classes']) %}
            {%- set newline ="%s      score_t tree_scores[BDT::fn_classes(n_classes) * n_trees]%d;\n"|format(newline,ensemble_dict['n_classes']) %}
            # but we can still explicitly zero out if you want
            {%- set newline ="%s      std::fill_n(score, %d, 0.);\n"|format(newline,ensemble_dict['n_classes']) %}
            {%- if cfg_get %}
                {%- set newline ="%s      sample_stream[0] << in_pkt;\n"|format(newline) %}
            {%- endif %}
        {%- elif '//hls-fpga-machine-learning insert zero' in line %}
            {%- set newline = line %}
            {%- set newline ="%s    input_arr_t x;"|format(newline) %}
            {%- set newline ="%s    std::fill_n(x, %d, 0.);"|format(newline,ensemble_dict['n_features']) %}
            {%- set newline ="%s    score_arr_t score%d;"|format(newline,ensemble_dict['n_classes']) %}
            {%- set newline ="%s    score_t tree_scores[BDT::fn_classes(n_classes) * n_trees]%d;"|format(newline,ensemble_dict['n_classes']) %}
            {%- set newline ="%s    std::fill_n(score, %d, 0.);"|format(newline,ensemble_dict['n_classes']) %}
        {%- elif '//hls-fpga-machine-learning insert top-level-function' in line %}
            {%- set newline = line %}
            {%- if not cfg_get %} 
                {%- set top_level = "%s    %s(x, score/*, tree_scores*/);\n"|format(intent,cfg['ProjectName']) %}
            {%- else %}
                {#- // TODO: Use all the bank buffers and test reconfiguration #}
                {#- // TODO: Use vote buffers #}
                {%- set top_level = "%s    bank_command_s_t command_pkt;\n"|format(intent) %}
                {%- set top_level = "%s    %s command_pkt.data = 0b00111111;\n"|format(top_level,intent) %}
                {%- set top_level = "%s    %s command_pkt.dest = 0;\n"|format(top_level,intent) %}
                {%- set top_level = "%s    %s bank_command_stream[0] << command_pkt;\n"|format(top_level,intent) %}
                {%- set top_level = "%s    %s %s__bank_buffer_1(sample_stream[0], bank_stream[0], bank_command_stream[0]);\n"|format(top_level,intent,cfg['ProjectName']) %}
                {%- set top_level = "%s    %s axis_crossbar<input_arr_s_t, 1, n_trees * n_classes>(bank_stream, tree_stream);\n"|format(top_level,intent) %}
                {%- for itree, trees in ensemble_dict['trees']|enumerate %}
                    {%- for iclass, tree in trees|enumerate %}
                        {%- set top_level %}
                         {{ top_level}}  ({{intent}}  {cfg['ProjectName']}__tree_cl{{iclass}}_{itree}(tree_stream[{{itree}} * n_classes + {{iclass}}], aux_score_stream[{{itree}} * n_classes + {{iclass}}]);
                        {%- endset %}
                        {%- set top_level %} 
                        {{top_level}} ({{intent}}  tree_scores[{{itree}} * n_classes + {{iclass}}] = tee<tree_score_s_t, score_t>(aux_score_stream[{{itree}} * n_classes + {{iclass}}], score_stream[{{itree}} * n_classes + {{iclass}}]); 
                        {%- endset%}                
                    {%- endfor %}
                {%- endfor %}
                {%- set top_level = "%s %s axis_crossbar<tree_score_s_t, n_trees * n_classes, n_classes>(score_stream, in_class_stream);\n"|format(top_level,intent) %}
                {%- for iclass in range(class_count) %}
                    {%- set top_level = "%s %s while(!in_class_stream[%d].empty()) {{"|format(top_level,intent,iclass) %}
                    {%- set top_level = "%s %s  %s__voting_station_cl%d(in_class_stream[%d], out_class_stream[%d]);"|format(top_level,intent,cfg['ProjectName'],iclass,iclass,iclass) %}
                    {%- set top_level = "%s %s}}"|format(top_level,intent) %}
                {%- endfor %}
            {%- endif %}
            {%- set newline="%s %s"|format(newline,top_level) %}
        {%- elif '//hls-fpga-machine-learning insert predictions' in line %}
            {%- set newline = line %}
            {%- set newline="%s %s for(int i = 0; i < {}; i++) {{"|format(newline,intent,ensemble_dict['n_classes']) %}
            {%- set newline="%s %s   std::cout << pr[i] << " ";"|format(newline,intent) %}
            {%- set newline="%s %s }"|format(newline,intent) %}
            {%- set newline="%s %s std::cout << std::endl;"|format(newline,intent) %}
        {%- elif '//hls-fpga-machine-learning insert tb-output' in line %}
            {%- set newline = line %}
            {%- set newline="%s %s for(int i = 0; i < {}; i++) {{"|format(newline,intent,ensemble_dict['n_classes']) %}
            {%- set newline="%s %s   fout << score[i] << ;"|format(newline,intent) %}
            {%- set newline="%s %s }"|format(newline,intent) %}
        {%- elif '//hls-fpga-machine-learning insert output' in line or '//hls-fpga-machine-learning insert quantized' in line %}
            {%- set newline = line %}
            {%- set newline="%s %sfor(int i = 0; i < {}; i++) {{"|format(newline,intent,ensemble_dict['n_classes']) %}
            {%- set newline="%s %s   std::cout << score[i] << ;"|format(newline,intent) %}
            {%- set newline="%s %s }"|format(newline,intent) %}
            {%- set newline="%s %s std::cout << std::endl;"|format(newline,intent) %}
        {%- elif '//hls-fpga-machine-learning insert final-round' in line %}
            {%- set newline = line %}
            {%- if cfg_get %}
                {%- for iclass in range(class_count) %}
                    {%- set newline="%s %s %s__voting_station_cl%d(in_class_stream[%d], out_class_stream[%d]);"|format(newline,intent,cfg['ProjectName'],iclass,iclass,iclass) %}
                {%- endfor%}
            {%- endif%}
        {%- elif '//hls-fpga-machine-learning insert stream-check' in line %}
            {%- set newline = line %}
            {%- if cfg_get %}
                {%- set newline="%s %s"|format(newline,intent) %}
                {%- for iclass in range(class_count) %}
                    {%- set newline = '%s !out_class_stream[%d].empty()'|format(newline,iclass) %}
                    {%- if iclass < class_count - 1 %}
                        {%- set newline = '%s && '|format(newline) %}
                    {%- else %}
                    {%- endif %}
                {%- endfor %}
            {%- endif %}
        {%- else %}
        {%- set newline=line %}
        {%- endif %}
        {{- newline}}
    {%- endfor %}
    
/*
    {# include "BDT.h"\n') #}  
    {# include "firmware/parameters.h"\n') #}
    {# include "firmware/{}.h"\n'.format(cfg['ProjectName'])) #}
    {# fout.write('int main(){\n') #}
    {# fout.write('\tinput_arr_t x = {{{}}};\n'.format(str([0] * ensemble_dict['n_features'])[1:-1])); #}
    {# fout.write('\tscore_arr_t score;\n') #}
    {# fout.write('\t{}(x, score);\n'.format(cfg['ProjectName'])) #}
    {# fout.write('\tfor(int i = 0; i < n_classes; i++){\n') #}
    {# fout.write('\t\tstd::cout << score[i] << ", ";\n\t}\n') #}
    {# fout.write('\tstd::cout << std::endl;\n') #}
    {# fout.write('\treturn 0;\n}') #}
    {#  fout.close() #}
*/

