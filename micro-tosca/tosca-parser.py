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

path = '/home/dido/code/micro-tosca/data/examples/helloworld.yml'
path_write = '/home/dido/code/micro-tosca/data/examples/helloworld.refactored.yml'



dir_path = os.path.dirname(os.path.realpath(__file__))



# CUSTOM NODE TYPEs
SERVICE = 'micro.nodes.Service'
COMMUNICATION_PATTERN = 'micro.nodes.CommunicationPattern'
DATABASE = 'micro.nodes.Database'
MESSAGE_BROKER = 'micro.nodes.MessageBroker'


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




def update_req_runtime(node, old, new):
    if 'requirements' in node:
        for r in node['requirements']:
            (k, v), = r.items()
            print(k,v)
            if 'run_time' == k and v == old  :
                if not isinstance(v, dict):
                    r[k] = new
                else:
                    r[k]['node'] = new
                return True
    return False



def get_node_type(ruamel_commented_map):
    return ruamel_commented_map['type'] 

def get_requirements(ruamel_commented_map):
    return ruamel_commented_map['requirements'] 

# From YAML to ruamel.YAML
yaml = ruamel.yaml.YAML(typ='rt') 
micro_yml = yaml.load(Path(path))

# From raumel.YAML to MicroTemplate
micro_template= MicroToscaTemplate('micro.tosca')

nodes_ruamel = micro_yml.get('topology_template').get('node_templates')
for (node_name, CommentedMap) in nodes_ruamel.items():
    node_type = get_node_type(CommentedMap)
    if node_type== SERVICE:
        s = Service(node_name)
        for req in get_requirements(CommentedMap):
            for (name, value) in req.items(): #  name:  run_time | deployemnt_time, value: <node_name> | realtioship ??
                if(name == RUN_TIME): #   
                    s.add_run_time(value)
                if(name == DEPLOYMENT_TIME): 
                    s.add_deployment_time(value)
        micro_template.push(s)
    if node_type == COMMUNICATION_PATTERN:
        micro_template.push(CommunicationPattern(node_name))
    if node_type == DATABASE:
        micro_template.push(Database(node_name))

print(micro_template)



""" 
print(type(order))
update_req_runtime(order, 'rabbitmq','ddd')


yaml.dump(micro_yml, Path(path_write)) """