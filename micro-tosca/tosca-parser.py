"""
Parser of Tosca file
"""

import ruamel.yaml
# from six import print_
from toscaparser.common.exception import ValidationError
from toscaparser.tosca_template import ToscaTemplate

from graph.nodes import Service, Database, CommunicationPattern
from graph.relationships import InteractsWith
from graph.template import Template

path = '/home/dido/code/micro-tosca/data/examples/helloworld.yml'

import os
dir_path = os.path.dirname(os.path.realpath(__file__))


# CUSTOM TYPE
SERVICE = 'micro.nodes.Service'
VOLUME = 'tosker.nodes.Volume'
SOFTWARE = 'tosker.nodes.Software'
IMAGE = 'tosker.artifacts.Image'
IMAGE_EXE = 'tosker.artifacts.Image.Service'
DOCKERFILE = 'tosker.artifacts.Dockerfile'
DOCKERFILE_EXE = 'tosker.artifacts.Dockerfile.Service'
PROTOCOL_POLICY = 'tosker.policies.Protocol'

# read Tosca yml file with Tosc Parser
tosca = ToscaTemplate(path, None)

# graph of the micro tosca
micro_tosca = Template('micro.tosca')

version = tosca.version

if tosca.version:
    print("\nversion: " + version)

if hasattr(tosca, 'description'):
    description = tosca.description
    if description:
        print("\ndescription: " + description)


if hasattr(tosca, 'topology_template'):
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
                print("service found"+ node.name)
            for relation in node.relationships:
                print(" \t{}".format(relation))
