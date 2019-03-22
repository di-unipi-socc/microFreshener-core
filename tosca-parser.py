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

from microanalyser.loader import MicroToscaLoader
from microanalyser.loader import JSONLoader

from microanalyser.trasformer import JSONTransformer
from microanalyser.trasformer import YMLTransformer

from microanalyser.analyser.principles import PRINCIPLES
from microanalyser.analyser.builder import AnalyserBuilder
from microanalyser.analyser.analyser import MicroAnalyser

from microanalyser.analyser.principles import IndependentDeployabilityPrinciple, HorizontalScalabilityPrinciple, NoApiGatewayAntipattern

from microanalyser.analyser.constant import INDEPENDENT_DEPLOYABILITY

from microanalyser.analyser.sniffer import EndpointBasedServiceInteractionSmellSniffer, NoApiGatewaySmellSniffer, WobblyServiceInteractionSmellSniffer, SharedPersistencySmellSniffer

import pprint

example = 'data/examples/helloworld_squads.yml'
json_ex = 'data/examples/helloworld.json'
# path_refactored = '/home/dido/code/micro-tosca/data/examples/helloworld.refactored.yml'

path_to_yml = os.path.join(os.path.dirname(os.path.realpath(__file__)), example)
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
# loader = MicroToscaLoader()
# micro_model = loader.load(path_to_yml)
# micro_model.update() # create object pointers and up_requirements

#JSON loader
loader = JSONLoader()
micro_model = loader.load(path_to_json)

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
#  shipping =  micro_model.get_node_by_name("shipping")
# ns = EndpointBasedServiceInteractionSmellSniffer()
# smell = ns.snif(shipping)
# print(smell.caused_by)

# order =  micro_model.get_node_by_name("rabbitmq")
# ag = NoApiGatewaySmellSniffer()
# res = ag.snif(order)
# print(res)

# order =  micro_model.get_node_by_name("order")
# ws = WobblyServiceInteractionSmellSniffer()
# smell = ws.snif(order)
# print(smell.caused_by)

# orderdb =  micro_model.get_node_by_name("orderdb")
# ws = SharedPersistencySmellSniffer()
# smell = ws.snif(orderdb)
# print([interaction.source.name for interaction in smell.caused_by])
# print(smell.caused_by)

#analyser = AnalyserBuilder(micro_model).add_principle("IndependentDeployability").add_principle("HorizontalScalability").build()
an = MicroAnalyser(micro_model)
an.add_smell_sniffer(EndpointBasedServiceInteractionSmellSniffer())
an.add_smell_sniffer(WobblyServiceInteractionSmellSniffer())
an.add_smell_sniffer(SharedPersistencySmellSniffer())

print(an.run())

# print(analyser.analyse())

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

# transformer = YMLTransformer()
# r = transformer.transform(micro_model)
# pprint.pprint(r)

#*******************************
#         OUTPUTTER
#*******************************
# imput: dictionary,
# convert the dictionary into a format (json, yml) and output it into
# different types of output: console, file, socket ??