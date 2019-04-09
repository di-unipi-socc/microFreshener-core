import sys
from ruamel.yaml import YAML
from ruamel.yaml.compat import StringIO

from ..model.template import MicroModel
from ..model.relationships import RunTimeInteraction, DeploymentTimeInteraction
from ..model.nodes import Root, Service, Database, CommunicationPattern
from ..model.groups import RootGroup, Edge, Squad
from ..loader.type import SERVICE, DATABASE, COMMUNICATION_PATTERN, EDGE, SQUAD, API_GATEWAY, CIRCUIT_BREAKER, MESSAGE_BROKER


class MyYAML(YAML):
    def dump(self, data, stream=None, **kw):
        inefficient = False
        if stream is None:
            inefficient = True
            stream = StringIO()
        YAML.dump(self, data, stream, **kw)
        if inefficient:
            return stream.getvalue()


class YMLTransformer(object):

    def __init__(self):
        self.yaml = MyYAML()

    # Transform a microModel Oject to YML format
    # @params:  microModel
    # @return:  string
    def transform(self, micro_model: MicroModel):
        return self.yaml.dump(self._to_dict(micro_model))

    def _to_dict(self, micro_model):

        yml_dict = self._get_metadata()

        topology_template = {}
        node_templates = dict()
        for node in micro_model.nodes:
            node_templates[node.name] = self._node_to_dict(node)
        topology_template['node_templates'] = node_templates

        groups = dict()
        for group in micro_model.groups:
            groups[group.name] = self._group_to_dict(group)
        topology_template["groups"] = groups
        yml_dict['topology_template'] = topology_template
        return yml_dict

    def _get_metadata(self):
        d_metadata = dict(tosca_definitions_version="tosca_simple_yaml_1_0", description="",
                          imports=[{"micro": "../../data/micro-tosca-types.yml"}])
        return d_metadata

    def _group_to_dict(self, group: RootGroup):
        d_group = {}
        group_type = ""
        if (isinstance(group, Edge)):
            group_type = EDGE
        elif (isinstance(group, Squad)):
            group_type = SQUAD
        else:
            raise ValueError("{} group not recognized".format(group))
        d_group['type'] = group_type

        members = [member.name for member in group.members]
        d_group['members'] = members
        return d_group

    def _node_to_dict(self, node: Root):
        # {"order":{"type":"micro.nodes.Service", "requirements":[{"run_time": "order_db"}]}}
        d_node = {}
        node_type = ""
        if(isinstance(node, Service)):
            node_type = SERVICE
        elif(isinstance(node, Database)):
            node_type = DATABASE
        elif(isinstance(node, CommunicationPattern)):
            node_type = node.concrete_type
        else:
            raise ValueError("{} Type not recognized".format(node))
        d_node['type'] = node_type

        requirements = []
        for rel in node.relationships:
            d_rel = {}
            if(isinstance(rel, DeploymentTimeInteraction)):
                d_rel['deployment_time'] = rel.target.name
            elif(isinstance(rel, RunTimeInteraction)):
                d_rel['run_time'] = rel.target.name
            else:
                raise ValueError('{} relationship not recognized.'.format(rel))
            requirements.append(d_rel)
        if(requirements):
            d_node['requirements'] = requirements
        return d_node
