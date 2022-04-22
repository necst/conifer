{# D A   T E S T A R E #}
{# #####################  M A I N ###################################################### #}
{%- if task=='main' %}   
    {%- for line in file %}
        {%- set line = line|replace('nnet_utils', relpath) %}
        {%- set line = line|replace('myproject', cfg['ProjectName']) %}
        {# if 'set_top' in line: #}
        {#  set   line = line|replace('myproject', '%s_decision_function'|format(cfg['ProjectName'])) #}
        {%- if 'set_part {xc7vx690tffg1927-2}' in line %}
            {%- set line = 'set_part {{%s}}'|format(cfg['XilinxPart']) %}
        {%- elif 'create_clock -period 5 -name default' in line %}
            {%- set line = 'create_clock -period %d -name default'|format(cfg['ClockPeriod']) %}
        {# Remove some lines #}
        {%- elif ('weights' in line) or ('-tb firmware/weights' in line)%}
            {%- set line = '' %}
        {%- elif '##hls-fpga-machine-learning insert individual-ips' in line %}
            {%- set line = '' %}
            {%- if cfg.get('PDR', False) == True %}
                {%- for ibank in range(1, bank_count + 1)%}
                    {%- set line = '%s source build_pdr_ips/bank_buffer_%d.tcl'|format(line,ibank) %}
                {%- endfor %}
                {%- for itree, trees in enumerate(ensemble_dict['trees']) %}
                    {%- for iclass, tree in enumerate(trees) %}
                        {%- set line ='%s source build_pdr_ips/tree_cl%d_%d.tcl'|format(line,iclass, itree) %}
                    {%- endfor %}
                {%- endfor %}       
                {% for iclass in range(class_count) %}
                    {%- set line = '%s source build_pdr_ips/voting_station_cl%d.tcl'|format(line,iclass) %}
                {%- endfor %}
            {%- endif %}
        {%- endif %}
        {{line}}
    {%- endfor %}
{%- endif %}

{# ################################## B A N K   B U F F E R ############################################################ #}
{%- if task=='bank_buffer' %} 
            {%- for line in file %}
                {%- set line = line|replace('myproject', cfg['ProjectName']) %}
                {%- set  line = line|replace('the_ip', 'bank_buffer_%d'|format(ibank)) %}
                {%- if 'set_part {xc7vx690tffg1927-2}' in line %}
                    {%- set line = 'set_part {{%s}}'|format(cfg['XilinxPart']) %}
                {%- elif 'create_clock -period 5 -name default' in line %}
                    {%- set line = 'create_clock -period %d -name default'|format(cfg['ClockPeriod']) %}
                {%- endif %}
                {{line}}
            {%- endfor %}
{%- endif %}

{# ################################ T R E E #####################################################################
{%- if task=='tree' %} 
                {%- for line in file %}
                    {%set line = line|replace('myproject', cfg['ProjectName']) %}
                    {%set line = line|replace('the_ip', 'tree_cl%d_%d'|format(iclass, itree)) %}

                    {%- if 'set_part {xc7vx690tffg1927-2}' in line %}
                        {%- set line = 'set_part {{%s}}'|format(cfg['XilinxPart']) %}
                    {%- elif 'create_clock -period 5 -name default' in line %}
                        {%- set line = 'create_clock -period %d -name default'|format(cfg['ClockPeriod']) %}
                    {%- endif %}

                    {{line}}
                {%- endfor %}
{%- endif %}

{# ########################### V O T I N G   S T A T I O N ####################################################### #}
{%- if task=='voting_station' %} 
            {%- for line in file %}
                {%- set line = line|replace('myproject', cfg['ProjectName']) %}
                {%- set line = line|replace('the_ip', 'voting_station_cl%d'|format(iclass)) %}

                {%- if 'set_part {xc7vx690tffg1927-2}' in line %}
                    {%- set line = 'set_part {{%s}}'|format(cfg['XilinxPart']) %}
                {%- elif 'create_clock -period 5 -name default' in line %}
                    {%- set line = 'create_clock -period %d -name default'|format(cfg['ClockPeriod']) %}
                {%- endif %}
                {{line}}
    {%- endfor %}
{%- endif %}


{# ############################### T R E E   I D L E ##################################################### #}
{%- if task=='tree_idle' %} 
        {%- for line in file %}
            {%- set line = line|replace('myproject', cfg['ProjectName']) %}
            {%- set line = line|replace('the_ip', 'tree_idle')%}

            {%- if 'set_part {xc7vx690tffg1927-2}' in line %}
                {%- set line = 'set_part {{%s}}'|format(cfg['XilinxPart']) %}
            {%-elif 'create_clock -period 5 -name default' in line %}
                {%- set line = 'create_clock -period %d -name default'|format(cfg['ClockPeriod'])%}
            {%- endif %}
            {{line}}
    {%- endfor %}
{%- endif %}

{# ######################### V O T E   B U F F E R #################################################### #}
{%- if task=='vote_buffer' %} 
        {%- for line in file %}
            {%- set line = line|replace('myproject', cfg['ProjectName'])%}
            {%- set line = line|replace('the_ip', 'vote_buffer')%}

            {%- if 'set_part {xc7vx690tffg1927-2}' in line%}
                {%- set line = 'set_part {{%s}}'|format(cfg['XilinxPart']) %}
            {%- elif 'create_clock -period 5 -name default' in line %}
                {%- set line = 'create_clock -period %d -name default'|format(cfg['ClockPeriod']) %}
            {%- endif %}
            {{line}}
    {%- endfor %}
{%- endif %}

{# ################################# E N U M E R E T O R ############################################ #}
{%- if task=='enumerator' %} 
        {%- for line in file %}
            {%- set line = line|replace('myproject', cfg['ProjectName']) %}
            {%- set line = line|replace('the_ip', 'enumerator') %}

            {%if 'set_part {xc7vx690tffg1927-2}' in line %}
                {%- set line = 'set_part {{%s}}'|format(cfg['XilinxPart']) %}
            {%elif 'create_clock -period 5 -name default' in line %}
                {%- set line = 'create_clock -period %d -name default'|format(cfg['ClockPeriod']) %}
            {%- endif %}
            {{line}}
    {%- endfor %}
{%- endif %}

