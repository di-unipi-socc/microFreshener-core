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
from .analyser import MicroToscaAnalyser

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

# read Tosca yml file with Tosc Parser
tosca = ToscaTemplate(path, None)

version = tosca.version

if tosca.version:
    print("\nversion: " + version)

if hasattr(tosca, 'description'):
    description = tosca.description
    if description:
        print("\ndescription: " + description)

""" if hasattr(tosca, 'topology_template'):
    topology_template = tosca.topology_template
    if topology_template:
        print(topology_template)

    if hasattr(tosca, 'inputs'):
        inputs = tosca.inputs
        if inputs:
            print("\ninputs:")
            for input in inputs:
                print("\t" + input.name)

    if hasattr(tosca, 'nodetemplates'):
        for node in tosca.nodetemplates:
            if node.is_derived_from(SERVICE):
                print("service found "+ node.name)
            for relation in node.relationships:
                print(" \t{}".format(relation))
 """


# def update_req_runtime(node, old, new):
#     if 'requirements' in node:
#         for r in node['requirements']:
#             (k, v), = r.items()
#             print(k,v)
#             if 'run_time' == k and v == old  :
#                 if not isinstance(v, dict):
#                     r[k] = new
#                 else:
#                     r[k]['node'] = new
#                 return True
#     return False

def get_node_type(ruamel_commented_map):
    return ruamel_commented_map['type'] 

def get_requirements(ruamel_commented_map):
    return ruamel_commented_map['requirements'] 

# From YAML to ruamel.YAML
yaml = ruamel.yaml.YAML()#typ='safe') #typ='rt') 
micro_yml = yaml.load(Path(path))

# From raumel.YAML to MicroTemplate
nodes_ruamel = micro_yml.get('topology_template').get('node_templates')

micro_template = MicroToscaTemplate('micro.tosca')

for node_name, commented_map in nodes_ruamel.items():
    node_type = get_node_type(commented_map)
    if node_type == SERVICE:
        el = Service.from_yaml(node_name,commented_map)
    if node_type == MESSAGE_BROKER: # TODO: derived from CommunicationPattern
        el = CommunicationPattern.from_yaml(node_name,node_type,commented_map)
    if node_type == DATABASE:
        el = Database.from_yaml(node_name,commented_map)
    el.name = node_name
    micro_template.push(el)


def _add_pointer(template):
    for node in template.nodes:
        for rel in node.relationships:
            rel.target = template[rel.target]

def _add_back_links(template):
    for node in template.nodes:
        for rel in node.run_time:
            rel.target.up_run_time_requirements.append(rel)
        for rel in node.deployment_time:
            rel.target.up_deployment_time_requirements.append(rel)

print(micro_template)
# add pointers and up:requiremsnts
_add_pointer(micro_template)
_add_back_links(micro_template)

#**************************
#          Analysis
#*************************

analyser = Analyser ()
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

"""
print(type(order))
update_req_runtime(order, 'rabbitmq','ddd')


yaml.dump(micro_yml, Path(path_write)) """