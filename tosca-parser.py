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
from microanalyser.analyser.principles import PRINCIPLES
import pprint

example = 'data/examples/helloworld_squads.yml'
json_ex = 'data/examples/hello-world-ok.json'
path_refactored = '/home/dido/code/micro-tosca/data/examples/helloworld.refactored.yml'

path_to_yml = os.path.join(os.path.dirname(os.path.realpath(__file__)), example)
path_to_json= os.path.join(os.path.dirname(os.path.realpath(__file__)), json_ex )


#**********************************
#        VALIDATOR: Open stack
# *********************************
tosca = ToscaTemplate(path_to_yml, None)

if tosca.version:
    print("\nversion: " + tosca.version)
    
#********************************
#         LOADER: yml 
#*******************************

# loader = MicroToscaLoader()
# micro_model = loader.load(path_to_yml)
# micro_model.update() # create object pointers and up_requirements

#********************************
#         LOADER: Json 
#*******************************
# loader = JSONLoader()
# micro_model = loader.load(path_to_json)
# micro_model.update()

loader = JSONLoader()
micro_model = loader.load(path_to_json)


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

analyser = MicroAnalyser(micro_model)

# pprint.pprint(analyser.analyse_node('order_db')['antipatterns'][0].interactions)
# for n in micro_model.nodes:
#     print(n.name + "\n")
#     for rel in n.neighbors:
#         print(rel.name) 

# for n in micro_model.nodes:
#     print("\n" + n.name )
#     for rel in n.incoming:
#          print(rel) 

# analyse a sungle node
# res = analyser.analyse() #nodes_to_exclude = [], principles_to_exclude=[], config_nodes ={}
# pprint.pprint(res)
n = micro_model.findByName('order')
# print(n)
pprint.pprint(analyser.analyse_node(n, PRINCIPLES)) #, principles_to_discard=['horizzontallyScalable', 'faultResilience']))
# pprint.pprint(analyser.analyse_node('order_db', constraints=[SHARED_PERSISTNECY]))

# analyse a single squad
#pprint.pprint(analyser.analyse_squad('group2'))

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
#         OUTPUTTER: json
#*******************************

# out = JSONTransformer()
# r = out.transform(micro_model)
# pprint.pprint(r)