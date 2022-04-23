{{ "#ifndef %s_H__\n#define %s_H__\n"|format(projectname|upper, projectname|upper ) }}
#include "BDT.h"
#include "parameters.h"

{%- if cfg_get %}
#include "hls_stream.h"
{%- endif%}


{%- if not cfg_get %}
// Monolithic IP
{{ "void %s(input_t *x, score_t *score/*, score_t tree_scores[BDT::fn_classes(n_classes) * n_trees]*/);"|format(projectname) }}
{%- else %}
// Reconfigurable set of IPs
        
// ENUMERTOR
{{ "void %s__enumerator(hls::stream<idless_input_arr_s_t> &input_stream, hls::stream<input_arr_s_t> &output_stream);"|format(projectname) }}

// BANK BUFFER IP
    {%- for ibank in range(1, bank_count + 1) %}
{{ "void %s__bank_buffer_%d(hls::stream<input_arr_s_t> &input_stream, hls::stream<input_arr_s_t> &output_stream, hls::stream<bank_command_s_t> &command_stream);"|format(projectname, ibank) }}
    {%- endfor %}
// TREE IPs
    {%- for itree, trees in ensemble_trees %}
        {%-for iclass, tree in enumerate_tree %}
{{ "void %s__tree_cl%d_%d(hls::stream<input_arr_s_t> &input_stream, hls::stream<tree_score_s_t> &output_stream);"|format(projectname, iclass, itree) }}
        {%- endfor %}
    {%- endfor %}

// IDLE TREE IP
{{ "void %s__tree_idle(hls::stream<input_arr_s_t> &input_stream, hls::stream<tree_score_s_t> &output_stream);"|format(projectname) }}

// VOTE BUFFER IP
{{ "void %s__vote_buffer(hls::stream<tree_score_s_t> &input_stream, hls::stream<tree_score_s_t> &output_stream, bool &irq);"|format(projectname) }}

// VOTING STATION IPs
        {%- set class_count = 1 %}
        {%- for itree, trees in ensemble_trees %}
            {%- if trees|length > class_count %}
                 {%- set class_count = trees|length %}
            {%- endif %}
        {%- endfor %}
        {%- for iclass in range(class_count) %}
{{ "void %s__voting_station_cl%d(hls::stream<tree_score_s_t>  &input_score_stream, hls::stream<class_score_s_t> &output_score_stream);"|format(projectname, iclass) }}
        {%- endfor %}

{%- endif %}
#endif

