# This source file comes from the Conifer open-source project 
# (https://github.com/thesps/conifer)

import sys
import importlib.util

import os
from jinja2 import Environment, FileSystemLoader

# Templates directory:
class TemplatesDir():
  def __new__(cls,dir):
    if not hasattr(cls, 'instance'):
      cls.instance = super(TemplatesDir, cls).__new__(cls)
      cls.env=Environment(loader=FileSystemLoader(dir))
    return cls.env

DefaultDir = os.path.dirname(os.path.abspath(__file__))
env=TemplatesDir(DefaultDir)

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
