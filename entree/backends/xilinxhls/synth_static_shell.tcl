        {%- for line in file %}
            {%- if '## hls-fpga-machine-learning insert project-name' in line %}
            {{-"## hls-fpga-machine-learning insert project-name %s_system"|format(projectname) }}
            {%- else %}
            {{-line}}
            {%- endif %}
        {%- endfor %}
