"""
Use of MicroTosca package
"""

import os

# from six import print_
from toscaparser.common.exception import ValidationError
from toscaparser.tosca_template import ToscaTemplate

from microtosca.graph.nodes import Service, Database, CommunicationPattern
from microtosca.graph.relationships import InteractsWith
from microtosca.graph.template import MicroToscaTemplate
from microtosca.analyser import MicroToscaAnalyser
from microtosca.loader import YmlLoader

import pprint

example = 'data/examples/helloworld_squads.yml'
path_refactored = '/home/dido/code/micro-tosca/data/examples/helloworld.refactored.yml'

path_to_yml = os.path.join(os.path.dirname(os.path.realpath(__file__)), example)

#**********************************
#        VALIDATOR: Open stack
# *********************************
tosca = ToscaTemplate(path_to_yml, None)

if tosca.version:
    print("\nversion: " + tosca.version)
    
#********************************
#         LOADER: yml 
#*******************************
loader = YmlLoader()
microtosca_template = loader.parse(path_to_yml)
microtosca_template.update() # create object pointers and up_requirements

#*******************************
#         ANALYSER
#*******************************

analyser = MicroToscaAnalyser(microtosca_template)
res = analyser.analyse()
pprint.pprint(res)

#*******************************
#         OUTPUTTER: json
#*******************************

# import json

# graph = dict()

# graph['nodes'] = [ repr(n) for n in micro_template.nodes]
# print(graph)