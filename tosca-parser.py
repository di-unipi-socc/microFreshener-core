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
from microanalyser.analyser.analyser import MicroAnalyser

from microanalyser.loader import YMLLoader
from microanalyser.loader import JSONLoader

from microanalyser.trasformer import JSONTransformer
from microanalyser.trasformer import YMLTransformer

from microanalyser.analyser.builder import AnalyserBuilder
from microanalyser.analyser.analyser import MicroAnalyser

from microanalyser.analyser.constant import INDEPENDENT_DEPLOYABILITY

from microanalyser.analyser.sniffer import EndpointBasedServiceInteractionSmellSniffer, NoApiGatewaySmellSniffer, WobblyServiceInteractionSmellSniffer, SharedPersistencySmellSniffer

import pprint

example = 'data/examples/helloworld_squads.yml'
json_ex = 'data/examples/helloworld.json'
yml_ex = 'data/examples/helloworld.yml'
# path_refactored = '/home/dido/code/micro-tosca/data/examples/helloworld.refactored.yml'

path_to_yml = os.path.join(os.path.dirname(os.path.realpath(__file__)), yml_ex)
path_to_json= os.path.join(os.path.dirname(os.path.realpath(__file__)), json_ex )


#**********************************
#        VALIDATOR: Open stack
# *********************************
tosca = ToscaTemplate(path_to_yml, None)

if tosca.version:
    print("\nversion: " + tosca.version)

#********************************
#         LOADER: yml, json
#*******************************
# Yml loader
loader = YMLLoader()
micro_model = loader.load(path_to_yml)
# micro_model.update() # create object pointers and up_requirements

exit()
#JSON loader
# loader = JSONLoader()
# micro_model = loader.load(path_to_json)

#********************************
#         MICRO MODEL
#*******************************
# add node
# s = Service(name="new")
# s.add_deployment_time(micro_model["order"])
# s.add_run_time(micro_model["order_db"])
# micro_model.add_node(s)

# remove node
#micro_model.delete_node(micro_model["new"])

#*******************************
#         ANALYSER
#*******************************

#analyser = AnalyserBuilder(micro_model).add_principle("IndependentDeployability").add_principle("HorizontalScalability").build()
an = MicroAnalyser(micro_model)
# an.add_node_smell_sniffer(EndpointBasedServiceInteractionSmellSniffer())
# an.add_node_smell_sniffer(WobblyServiceInteractionSmellSniffer())
# an.add_node_smell_sniffer(SharedPersistencySmellSniffer())
# an.add_group_smell_sniffer(NoApiGatewaySmellSniffer())
an.add_node_smell_sniffer(SharedPersistencySmellSniffer())
res = an.run()
# print(res)

#*******************************
#         PLANNER
#*******************************
# def merge_services(micro_model, shared_persistency):
#     copy_micro_model = micro_model.copy()
#     new_name = "_".join([node.name for node in shared_persistency.source_nodes])
#     new_service = Service(new_name)
    
#     for node in shared_persistency.source_nodes:
#         pass
#         copy_micro_model.delete_node(node)

#*******************************
#         TRANFORMER
#*******************************

transformer = YMLTransformer()
r = transformer.transform(micro_model)
pprint.pprint(r)

#*******************************
#         OUTPUTTER
#*******************************
# imput: dictionary,
# convert the dictionary into a format (json, yml) and output it into
# different types of output: console, file, socket ??