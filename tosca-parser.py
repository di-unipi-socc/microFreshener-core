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
from microanalyser.model.antipatterns import DEPLOYMENT_INTERACTION, DIRECT_INTERACTION, SHARED_PERSISTENCY
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

res = analyser.analyse(nodes_to_exclude = [], principles_to_exclude=[], config_nodes ={})
pprint.pprint(res)
# pprint.pprint(analyser.analyse_node('shipping', config_analysis={'antipatterns':[SHARED_PERSISTENCY]})) # constraints=[DEPLOYMENT_INTERACTION]

# pprint.pprint(analyser.analyse_node('order_db'))
# pprint.pprint(analyser.analyse_node('order_db', constraints=[SHARED_PERSISTNECY]))

#pprint.pprint(analyser.analyse_squad('group2'))


#*******************************
#         OUTPUTTER: json
#*******************************
