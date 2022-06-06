# This source file comes from the Conifer open-source project 
# (https://github.com/thesps/conifer)

import sys
import importlib.util

import os
from jinja2 import Environment, FileSystemLoader

templating_environment = Environment(loader=FileSystemLoader(os.path.dirname(os.path.abspath(__file__))))

SPEC_WRITER = importlib.util.find_spec('.writer', __name__)

writer = importlib.util.module_from_spec(SPEC_WRITER)
if '_tool' in locals() != None:
    writer._tool = _tool
SPEC_WRITER.loader.exec_module(writer)

write = writer.write
auto_config = writer.auto_config
decision_function = writer.decision_function
sim_compile = writer.sim_compile
build = writer.build

del SPEC_WRITER
