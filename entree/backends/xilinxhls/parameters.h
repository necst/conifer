
//    fout = open('{}/firmware/parameters.h'.format(cfg['OutputDir']), 'w')

// cfg=cfg
// esnemble_dict_n=ensemble_dict
// bank_count=bank_count
//max_parallel_samples = 6
// 

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////// D O N E ? /////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#ifndef BDT_PARAMS_H__\n#define BDT_PARAMS_H__
#include "BDT.h"
#include "ap_fixed.h"
{%- if cfg_get %}
#include "utils.h"
#include "ap_axi_sdata.h"

{{"static const int n_trees = %d;"|format(ensemble_dict['n_trees']) }}
{{"static const int max_depth = %d;"|format(ensemble_dict['max_depth']) }}
{{"static const int n_features = %d;"|format(ensemble_dict['n_features']) }}
{{"static const int n_classes = %d;"|format(ensemble_dict['n_classes']) }}
{{"typedef %d input_t;"|format(cfg['Precision']) }}
typedef input_t input_arr_t[n_features];
{{"typedef %d score_t;"|format(cfg['Precision']) }}
typedef score_t score_arr_t[n_classes];
    # TODO score_arr_t
typedef input_t threshold_t;

    {% if cfg.get('PDR', False) %}
        # TODO: Allow max_parallel_sample configuration
        {{"static const int max_parallel_samples = %d;"|format(max_parallel_samples) }}
        {{"static const int bank_count = %d;"|format(bank_count) }}
        static const int sample_id_size = bitsizeof(max_parallel_samples);
        static const int bank_address_size = bitsizeof(bank_count + 1);
        typedef hls::axis<ap_uint<8>, 0, 0, bank_address_size> bank_command_s_t;
        typedef hls::axis<input_arr_t, 0, 0, 0> idless_input_arr_s_t;
        typedef hls::axis<input_arr_t, 0, sample_id_size, 0> input_arr_s_t;
        typedef hls::axis<score_t, 0, sample_id_size, bitsizeof(n_classes)> tree_score_s_t;
        typedef hls::axis<score_t, 0, sample_id_size, 0> class_score_s_t;
    {% endif %}
    tree_fields = ['feature', 'threshold', 'value',
                   'children_left', 'children_right', 'parent']

    static const BDT::BDT<n_trees, max_depth, n_classes, input_arr_t, score_t, threshold_t> bdt = 
    { // The struct
    {{"%s, // The normalisation"|format(string(ensemble_dict['norm'])) }}
    {%- set newline = "{" %}
    {%- if ensemble_dict['n_classes'] > 2 %}
        {%- for iip, ip in enumerate(ensemble_dict['init_predict']) %}
            {%- if iip < len(ensemble_dict['init_predict']) - 1 %}
                {%- set newpath = "%s,"|format(ip) %}
                {%- set newline = "%s %s"|format(newline,newpath) %}
            {%- else %}
                {%- set newline ="%s %d}}, // The init_predict"|format(newline,ip) %}
            {%- endif %}
        {%- endfor %}
    {%- else %}
        {%- set newline = "%s %s},"|format(newline,string(ensemble_dict['init_predict'][0]))  %}
    {%- endif %}
    {{-newline}}

    {%- for itree, trees in enumerate(ensemble_dict['trees']) %}
    {{"{ // trees[%s]"|format(string(itree)) }}
    // loop over classes
        {%- for iclass, tree in enumerate(trees) %}
        {"{ // [%s]"|string(iclass)  %}
        // loop over fields
            {%- for ifield, field in enumerate(tree_fields) %}

/////////////////////////////////////////////////////////////////////////////////////////////////////////
                {%- set newline = "{, ?? }"|format(join(map(str, tree[field])) %}
////////////////////////////////////////////////////////////////////////////////////////////////////////////////
                {%- if ifield < len(tree_fields) - 1 %}
                    {% set newline ="%s , \n"|format(newline) %}
                {%- endif %}
                {{- newline}}
            {%- endfor %}
            {%- set newline ="%s"|newline%}
            {%- if iclass < len(trees) - 1 %}
                {%- set newline ="%s , \n"|format(newline) %}
            {{newline}}
            {%- endif %}
        {%- endfor %}
        {%- set newline = "}"%}
        {%- if itree < ensemble_dict['n_trees'] - 1 %}
            {%- set newline ="%s , \n"|format(newline) %}
        {{-newline}}
        {%- endif %}
    {%- endfor%}
    }
};

    #endif

{% endif %}
