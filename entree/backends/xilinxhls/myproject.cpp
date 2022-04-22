#include "BDT.h"
#include "parameters.h"
{{ "#include \"%s.h\" "|format(projectname) }}
   

{% if not cfg_get %}

// Monolithic IP
{{ "void %s(input_t *x, score_t *score/*, score_t tree_scores[BDT::fn_classes(n_classes) * n_trees]*/){"|format(projectname) }}
    #pragma HLS INTERFACE s_axilite port=return
    #pragma HLS INTERFACE m_axi depth=n_features bundle=x port=x
    #pragma HLS INTERFACE s_axilite port=x
    #pragma HLS INTERFACE m_axi depth=n_classes bundle=score port=score
    #pragma HLS INTERFACE s_axilite port=score
    
    input_arr_t x_local;
    #pragma HLS array_partition variable=x_local
    
    score_arr_t score_local;
    #pragma HLS array_partition variable=score_local
    
    pre_load: for (unsigned int i = 0; i < n_features; i++) {
        #pragma HLS unroll
        x_local[i] = x[i];
    }
    
    score_t tree_scores[BDT::fn_classes(n_classes) * n_trees];
    
    bdt.decision_function(x_local, score_local, tree_scores);
    
    post_store: for (unsigned int i = 0; i < n_classes; i++) {
        #pragma HLS unroll
        score[i] = score_local[i];
    }
}
        
{% else %}
// Reconfigurable set of IPs
        
// ENUMERATOR
{{"void %s__enumerator(hls::stream<idless_input_arr_s_t> &input_stream, hls::stream<input_arr_s_t> &output_stream){"|format(projectname) }}
    #pragma HLS INTERFACE axis register port=input_stream
    #pragma HLS INTERFACE axis register port=output_stream
    #pragma HLS INTERFACE ap_ctrl_none port=return
    static BDT::Enumerator<max_parallel_samples, sample_id_size, n_features, idless_input_arr_s_t, input_arr_s_t> en;
    en.top_function(input_stream, output_stream);}

// BANK BUFFER IP
    {% for ibank in range(1, bank_count + 1) %}
{{"void %s__bank_buffer_%d(hls::stream<input_arr_s_t> &input_stream, hls::stream<input_arr_s_t> &output_stream, hls::stream<bank_command_s_t> &command_stream){"| format(projectname, ibank) }}
    #pragma HLS INTERFACE axis register port=input_stream
    #pragma HLS INTERFACE axis register port=output_stream
    #pragma HLS INTERFACE axis register port=command_stream
    #pragma HLS INTERFACE ap_ctrl_none port=return
{{ "    static BDT::Bank_buffer<input_arr_s_t, bank_command_s_t, max_parallel_samples, bank_count> bb(%d);"|format(ibank) }}
    bb.top_function(input_stream, output_stream, command_stream);}
    {% endfor %}
// TREE IPs
    {% for itree, trees in ensemble_trees %}
        {% for iclass, tree in enumerate_tree %}
{{ "void %s__tree_cl%d_%d(hls::stream<input_arr_s_t> &input_stream, hls::stream<tree_score_s_t> &output_stream){"|format(projectname, iclass, itree) }}
    #pragma HLS INTERFACE axis register port=input_stream
    #pragma HLS INTERFACE axis register port=output_stream
    #pragma HLS INTERFACE ap_ctrl_none port=return
    input_arr_s_t input;
    input_stream >> input;
{{"    auto output_data = bdt.trees[%d][%d].decision_function(input.data);"|format(itree, iclass) }}
    tree_score_s_t output;
    output.data = output_data;
    output.keep = -1;
    output.strb = 0;
    output.id = input.id;
{{"    output.dest = %d;"|format(iclass) }}
    output_stream << output;}
 
                 {% endfor %}
    {% endfor %}       
        
// IDLE TREE IP
{{"void %s__tree_idle(hls::stream<input_arr_s_t> &input_stream, hls::stream<tree_score_s_t> &output_stream){"|format(projectname) }}
    #pragma HLS INTERFACE axis register port=input_stream
    #pragma HLS INTERFACE axis register port=output_stream
    #pragma HLS INTERFACE ap_ctrl_none port=return
    input_arr_s_t input;
    input_stream >> input;
    tree_score_s_t output;
    output.data = 0;
    output.keep = 0;
    output.strb = 0;
    output.id = input.id;
    output.dest = -1;
    output_stream << output;}
        

// VOTE BUFFER IP
{{ "void %s__vote_buffer(hls::stream<tree_score_s_t> &input_stream, hls::stream<tree_score_s_t> &output_stream, bool &irq){"|format(projectname) }}
    #pragma HLS INTERFACE axis register port=input_stream
    #pragma HLS INTERFACE axis register port=output_stream
    #pragma HLS INTERFACE ap_none register port=irq
    #pragma HLS INTERFACE ap_ctrl_none port=return
    static BDT::Vote_buffer<tree_score_s_t> vb;
    vb.top_function(input_stream, output_stream, irq);}
                

// VOTING STATION IPs
    {% for iclass in range(class_count) %}
{{" void %s__voting_station_cl%d(hls::stream<tree_score_s_t>  &input_score_stream, hls::stream<class_score_s_t> &output_score_stream){"|format(projectname, iclass) }}
    #pragma HLS INTERFACE axis register port=input_score_stream
    #pragma HLS INTERFACE axis register port=output_score_stream
    #pragma HLS INTERFACE ap_ctrl_none port=return
{{"    static BDT::Voting_station<n_classes, tree_score_s_t, class_score_s_t, score_t, max_parallel_samples> vs(%d, bdt.init_predict[%d], bdt.normalisation);"|format(iclass,iclass) }}
{{"    vs.top_function(input_score_stream, output_score_stream);}" }}
    {% endfor %}
            
{% endif %}