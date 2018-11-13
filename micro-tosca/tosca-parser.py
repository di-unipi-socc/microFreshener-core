"""
Parser of Tosca file
"""

import toscaparser
from toscaparser.tosca_template import ToscaTemplate


path = '/home/dido/code/micro-tosca/data/examples/helloworld.yml'

import os
dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)

tosca = ToscaTemplate(path, None)

version = tosca.version
print(type(tosca))
if tosca.version:
    print("\nversion: " + version)

if hasattr(tosca, 'description'):
    description = tosca.description
    if description:
        print("\ndescription: " + description)

if hasattr(tosca, 'inputs'):
    inputs = tosca.inputs
    if inputs:
        print("\ninputs:")
        for input in inputs:
            print("\t" + input.name)

if hasattr(tosca, 'nodetemplates'):
    nodetemplates = tosca.nodetemplates
    if nodetemplates:
        print("\nnodetemplates:")
        for node in nodetemplates:
            print("{}".format(node.type))
