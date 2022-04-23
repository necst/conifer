{# ###################### #}
{# Usefull math functions #}
{# ###################### #}
{%- macro ceil(var)%}
     var|round(0,'ceil')
     {# macro returns string, so this function needs to be called as 'ceil(var)|int' #}
{%- endmacro %}

{%- macro log2(var)%}
     var|log(2)
{%- endmacro %}


{# ############################### #}
{#       READ && WRITE FILE        #}
{# ############################### #}
{%- for line in file %}
{%- set precision = cfg['Precision'].split('<')[1].split(',')[0]|int %} 
{%- if "## hls-fpga-machine-learning insert project-name" in line %}
{{-"## hls-fpga-machine-learning insert project-name %s_system"| format(cfg['ProjectName'])}}
{%- elif "## hls-fpga-machine-learning insert project-part" in line %}
{{-"## hls-fpga-machine-learning insert project-part %s"| format(cfg['XilinxPart'])}}
{%- elif "## hls-fpga-machine-learning insert project-board" in line %}
{{-"## hls-fpga-machine-learning insert project-board %s"| format(cfg['XilinxBoard'])}}
{%- elif "## hls-fpga-machine-learning insert sample_length" in line %}
{%- set num1 = (2**ceil(log2(precision))|int)*ensemble_dict['n_features'] %}
{{-"## hls-fpga-machine-learning insert sample_length %s"| format(num1|int|string)}}
{%- elif "## hls-fpga-machine-learning insert n-classes" in line %}
{{-"## hls-fpga-machine-learning insert n-classes %s"| format(class_count|int|string) }}
{%- elif "## hls-fpga-machine-learning insert result_lenght" in line %}
{%- set num2 = 8*ceil(precision)|int/8 %}
{{-"## hls-fpga-machine-learning insert result_lenght %s"| format(num2|int|string) }}
{%- elif "## hls-fpga-machine-learning insert output_length" in line %}
{%- set num3 =  2**ceil(log2(8*(ceil(precision)|int/8))|int)|int %}
{{-"## hls-fpga-machine-learning insert output_length %s"| format(num3|int|string) }}
{%- elif "## hls-fpga-machine-learning insert n-banks" in line %}
{{-"## hls-fpga-machine-learning insert n-banks %s"| format(bank_count|int|string) }}
{%- elif "## hls-fpga-machine-learning insert n-trees-per-bank" in line %}
{{-"## hls-fpga-machine-learning insert n-trees-per-bank %s"| format(cfg['TreesPerBank']|int|string) }}
{%- elif "## hls-fpga-machine-learning insert id-length" in line %}
{%- set num4 = ceil(log2(max_parallel_samples|int))|int+1 %}
{{-"## hls-fpga-machine-learning insert id-length %s"| format(num4|int|string) }}
{%- else  %}
{{-line }}
{%- endif %}
{%- if "##project_name##" in line %}
{{-"##project_name##, %s"|format(cfg['ProjectName']) }}
{%- endif %}
{%- endfor %}

{# ###################### #}
{# TODO: Manage clock     #}
{# ###################### #}
{#elif 'create_clock -period 5 -name default' in line: #}
{#    line = 'create_clock -period {} -name default\n'.format( #}
{#        cfg['ClockPeriod']) #}
{# fout.write(line) #}
        
        