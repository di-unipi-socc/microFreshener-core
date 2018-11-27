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

#*****************************************
#        VALIDATOR: Open stack
# *******************************************
tosca = ToscaTemplate(path, None)

if tosca.version:
    print("\nversion: " + tosca.version)

if hasattr(tosca, 'description'):
    description = tosca.description
    if description:
        print("\ndescription: " + description)

#**************************
#         LOADER: yml 
#*************************
loader = YmlLoader()
micro_template = loader.parse(path)
micro_template.update()

#**************************
#         ANALYSIS
#*************************

analyser = MicroToscaAnalyser(micro_template)

sd = analyser.shared_databases_antipatterns()
print("\nShared databases:")
print("\t".join([str(s) for s in sd]))

dt = analyser.deployment_time_interaction_antipattern()
print("\nDeployement time interaction nodes:")
for (s,value) in dt.items():
    print("{}:".format(s))
    print(''.join(str(e) for e in value))

dri = analyser.direct_run_time_interaction()
print("\nDirect run time interaction nodes:")
for (node,value) in dri.items():
    print("{}:".format(node))
    print(''.join(str(e) for e in value))

cf = analyser.cascading_failures()
print("\nCascading failure nodes:")
for (node,value) in cf.items():
    print("{}:".format(node))
    print(''.join(str(e) for e in value))

#**********************************************
#           OUTPUTTER: json
#*********************************************

import json

graph = dict()

graph['nodes'] = [ repr(n) for n in micro_template.nodes]
print(graph)
    
"""
print(type(order))
update_req_runtime(order, 'rabbitmq','ddd')

yaml.dump(micro_yml, Path(path_write)) """