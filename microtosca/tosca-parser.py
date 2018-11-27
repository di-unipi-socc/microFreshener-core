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

import json

path = '/home/dido/code/micro-tosca/data/examples/helloworld.yml'
path_write = '/home/dido/code/micro-tosca/data/examples/helloworld.refactored.yml'


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

#********************************
#         LOADER: yml 
#*******************************
loader = YmlLoader()
micro_template = loader.parse(path)
micro_template.update()

#*******************************
#         ANALYSIS
#*******************************

analyser = MicroToscaAnalyser(micro_template)
res = analyser.analyse()
print(res)

#*******************************
#           OUTPUTTER: json
#*******************************

# import json

# graph = dict()

# graph['nodes'] = [ repr(n) for n in micro_template.nodes]
# print(graph)