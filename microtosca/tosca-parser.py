"""
Parser of Tosca file
"""

import ruamel.yaml
from pathlib import Path

import os

# from six import print_
from toscaparser.common.exception import ValidationError
from toscaparser.tosca_template import ToscaTemplate

from graph.nodes import Service, Database, CommunicationPattern
from graph.relationships import InteractsWith
from graph.template import MicroToscaTemplate
from analyser import MicroToscaAnalyser
from loader.yml import YmlLoader

import pprint

#path = '/home/dido/code/micro-tosca/data/examples/helloworld.yml'
path = '/home/dido/code/micro-tosca/data/examples/helloworld_squads.yml'

path_refactored = '/home/dido/code/micro-tosca/data/examples/helloworld.refactored.yml'

dir_path = os.path.dirname(os.path.realpath(__file__))

# CUSTOM NODE TYPEs
SERVICE = 'micro.nodes.Service'
COMMUNICATION_PATTERN = 'micro.nodes.CommunicationPattern'
DATABASE = 'micro.nodes.Database'

MESSAGE_BROKER = 'micro.nodes.MessageBroker'
CIRCUIT_BREAKER = 'micro.nodes.CircuitBreaker'

# CUSTOM RELATIONSHIP TYPES
INTERACT_WITH = 'micro.relationships.InteractsWith'
RUN_TIME = "run_time"
DEPLOYMENT_TIME = "deployment_time"

#**********************************
#        VALIDATOR: Open stack
# *********************************
tosca = ToscaTemplate(path, None)

if tosca.version:
    print("\nversion: " + tosca.version)

if hasattr(tosca, 'description'):
    description = tosca.description
    if description:
        print("\ndescription: " + description)

# if hasattr(tosca.topology_template, 'groups'):
#     groups = tosca.topology_template.groups
#     for g in groups:
#         print(g.name)
#         for m in g.members:
#             print(m)

#********************************
#         LOADER: yml 
#*******************************
loader = YmlLoader()
microtosca_template = loader.parse(path)
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