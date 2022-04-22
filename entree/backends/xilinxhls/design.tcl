{# D A   T E S T A R E #}
     if cfg.get('PDR', False) == True:
        file = open(os.path.join(filedir, 'system-template/reconfigurable_system/scripts/design.tcl'), 'r')
        fout = open('{}/{}_reconfigurable_system/scripts/design.tcl'.format(cfg['OutputDir'], cfg['ProjectName']) , 'w')

        trees_per_bank = int(cfg['TreesPerBank'])
        rp_variants = math.ceil(tree_count / (trees_per_bank * bank_count))
#############################################################################################################################################
        {%- for line in file %}
            
            {%- if '## hls-fpga-machine-learning insert project-part' in line %}
                {%- set line = line.replace('## hls-fpga-machine-learning insert project-part', cfg['XilinxPart']) %}
            {%- elif '## hls-fpga-machine-learning insert rp-module-definition' in line %}
                {%- set line = '' %}

                {%- set curr_bank = 0 %}
                {%- set curr_tree_in_bank = 0 %}
                {%- set curr_variant = 0 %}

                {%- for itree, trees in enumerate(ensemble_dict['trees']) %}
                    {%- for iclass, tree in enumerate(trees) %}
                        {%- if (curr_variant == 0) %}
                            {%- set line = '%s set module_{bank}_{tree} "top_system_tree_{bank}_{tree}_0_tree_wrapper_tree_bb_0"\n'|format(line,bank = curr_bank,tree = curr_tree_in_bank)
                        {%- endif %}
                        {%-- set line %}
                         {{line}} set module_{{curr_bank}}_{{curr_tree_in_bank}}_variant{{curr_variant}} "tree_cl{{iclass}}_{{tree_in_class}}" 
                         set variant $module_{{curr_bank}}_{{curr_tree_in_bank}}_variant{{curr_variant}} 
                         add_module $variant
                         set_attribute module $variant moduleName   $module_{curr_{bank}}_{{curr_tree_in_bank}}
                         set_attribute module $variant prj          $prjDir/$variant.prj
                         set_attribute module $variant xdc          $ipDir/$variant/contraints/TOP_FUNCTION_ooc.xdc
                         set_attribute module $variant synth        ${{run.rmSynth}}
                         
                        {%-- endset %}
                        {%- set curr_variant = curr_variant + 1 %}

                        {%- if (curr_variant >= rp_variants) %}
                            {%- set curr_variant = 0 %}
                            {%- set curr_tree_in_bank = curr_tree_in_bank + 1 %}
                            {%- if (curr_tree_in_bank >= trees_per_bank) %}
                                {%- curr_tree_in_bank = 0 %}
                                {%- curr_bank = curr_bank + 1 %}
                            {%- endif %}
                        {%- endif %}
                    {%- endfor %}
                {%- endfor %}
                {%- set line = '%s \n' |format(line) %}
                {%- set line = '%s \n' |format(line) %}

                {%- for ibank in range(bank_count) %}
                    {%- for itree in range(trees_per_bank) %}
                        {%- set line = '%s set module_%d_%d_inst "top_system_i/tree_%d_%d/inst/tree_bb"\n'|format(line,ibank,itree,ibank,itree) %}
                    {%- endfor %}
                {%- endfor %}
                
                {%- set line = '%s \n' |format(line) %}
                {%- set line = '%s \n'|format(line) %}

            {%- elif '## hls-fpga-machine-learning insert rp-configuration' in line %}
                {%- set line = '' %}

                {%- for i_config in range(rp_variants) %}
                    {%- set line = '%s set config "Config_%d" \n'|format(line,i_config); %}
                    {%- set line = '%s \n';|format(line) %}
                    {%- set line = '%s add_implementation $config\n';
                    {%- set line = '%s set_attribute impl $config top             $top\n';|format(line) %}
                    {%- set line = '%s set_attribute impl $config pr.impl         1\n';|format(line) %}
                    {%- set line = '%s set_attribute impl $config implXDC         [list $xdcDir/top_system_pblock.xdc \\\n';|format(line) %}
                    {%- set line = '%s                                         ]\n';|format(line) %}
                    {%- set line = '%s set_attribute impl $config impl            ${run.prImpl} \n';|format(line) %}
                    {% if implement == 0%}
                    {%- set line = '%s set_attribute impl $config partitions      [list [list $static           $top           {}] \\\n'|format(line,implement %}
                    {% else %}
                    {%- set line = '%s set_attribute impl $config partitions      [list [list $static           $top           {}] \\\n'|format(line,import%}
                    {% endif %}
                    {% for i_bank in range(bank_count) %}
                        for i_tree in range(trees_per_bank):
                            {%- set line %}
                            {{line}}                                                 [list [ if {{ [info exists module_{{i_bank}}_{{i_tree}}_variant{{i_config}}] == 1 }} {{set module_{{i_bank}}_{{i_tree}}_variant{{i_config}}}} {{set module_0_0_variant0}} ] $module_{{i_bank}}_{{i_tree}}_inst [ if {{ [info exists module_{{i_bank}}_{{i_tree}}_variant{{i_config}}] == 1 }} {{expr {{{{implement}}}}}} {{expr {{{{greybox}}}}}} ]] \\\n'
                            {% endset %}    
                    {% endfor %}
                    {%- set line = '%s                                         ]\n';|format(line) %}
                    {%- set line = '%s set_attribute impl $config verify          ${run.prVerify} \n';|format(line) %}
                    {%- set line = '%s set_attribute impl $config bitstream       ${run.writeBitstream} \n';|format(line) %}
                    {%- set line = '%s set_attribute impl $config cfgmem.pcap     1\n';|format(line) %}
                    {%- set line = '%s \n';
                {%- endofor %}
                {%- set line = '%s \n';
            {%- elif '## hls-fpga-machine-learning insert rp-flat-configuration' in line %}
                {% set line = '' %}
                {%- set line = '%s add_implementation Flat\n'|format(line) %}
                {%- set line = '%s set_attribute impl Flat top          $top\n'|format(line) %}
                {%- set line = '%s set_attribute impl Flat implXDC      [list $xdcDir/top_system_pblock.xdc \\\n'|format(line) %}
                {%- set line = '%s                                     ]\n'|format(line) %}
                {%- set line = '%s set_attribute impl Flat partitions   [list [list $static           $top           implement] \\\n'|format(line) %}
                {% for i_bank in range(bank_count) %}
                    {% for i_tree in range(trees_per_bank) %}
                        {%- set line = '%s                                                 [list $module_0_0_00 $module_%d_%d_inst greybox] \\\n'|format(line,i_bank,i_tree) %}
                    {%endfor%}
                {%endfor%}
                {%- set line = '%s                                     ]\n'|format(line) %}
                {%- set line = '%s set_attribute impl Flat impl         ${run.flatImpl}\n'|format(line) %}
            {%- endif %}
            {{line}}
        {%- endfor %}
