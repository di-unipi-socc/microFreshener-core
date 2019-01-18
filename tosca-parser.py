"""
Use of microanalyser package
"""

import os

# from six import print_
from toscaparser.common.exception import ValidationError
from toscaparser.tosca_template import ToscaTemplate

from microanalyser.model.nodes import Service, Database, CommunicationPattern
from microanalyser.model.relationships import InteractsWith
from microanalyser.model.template import MicroModel
from microanalyser.analyser import MicroAnalyser
from microanalyser.loader import MicroToscaLoader

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
loader = MicroToscaLoader()
microtosca_template = loader.load(path_to_yml)
microtosca_template.update() # create object pointers and up_requirements

#*******************************
#         ANALYSER
#*******************************

analyser = MicroAnalyser(microtosca_template)
# res = analyser.analyse()
# pprint.pprint(res)

# print(analyser.analyse_node('shipping'))
# print(analyser.analyse_node('order'))
print(analyser.analyse_squad('group2'))


#*******************************
#         OUTPUTTER: json
#*******************************

# import json

# model = dict()

# model['nodes'] = [ repr(n) for n in micro_template.nodes]
# print(model)