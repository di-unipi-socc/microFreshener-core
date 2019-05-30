import json

from ..model import MicroToscaModel
from ..model  import RunTimeInteraction, DeploymentTimeInteraction
from ..model import Root, Service, Database, CommunicationPattern, MessageBroker, MessageRouter
from ..model.groups import Edge, Team

from ..model.type import  MICROTOSCA_NODES_MESSAGE_BROKER
from ..model.type import MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_TIMEOUT_PROPERTY, MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_CIRCUIT_BREAKER_PROPERTY, MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_DYNAMIC_DISCOVEY_PROPERTY
from ..errors import ExporterError
from .iexporter import Exporter
from ..importer.jsontype import JSON_NODE_DATABASE, JSON_NODE_MESSAGE_BROKER, JSON_NODE_MESSAGE_ROUTER, JSON_NODE_SERVICE
from ..importer.jsontype import JSON_DEPLOYMENT_TIME, JSON_RUN_TIME
from ..importer.jsontype import JSON_GROUPS_EDGE, JSON_GROUPS_TEAM

class JSONExporter(Exporter):

    def __init__(self):
        pass

    # Transform a microModel Oject to a Dicionary format.
    # @input:  microModel
    # @return: python dictionary
    def Export(self, micro_model:MicroToscaModel)->str:
        return self.serialize(micro_model)
        # TODO: returns a JSON object instead of dict
        # ATTENTION: in the restfule api the Response() object requires a dict that are than converted into json
        # return json.dumps(self.serialize(micro_model), ensure_ascii=False)

    def serialize(self, obj):
        d = {}
        if (isinstance(obj, MicroToscaModel)):
            d["name"] = obj.name # name of the models
            d['nodes'] = []      # nodes
            d['links'] = []      # links
            d['groups'] = []     # groups
            for node in obj.nodes:
                d['nodes'].append(self._transform_node(node))
                for rel in node.relationships:
                    d['links'].append(self._transform_relationship(rel))
            for group in obj.groups:
                d['groups'].append(self._transform_group(group))
        return d

    def _transform_node(self, node):
        dict_node = {}
        dict_node['name'] = node.name
        if(isinstance(node, Service)):
            dict_node['type'] = JSON_NODE_SERVICE
        elif(isinstance(node, Database)):
            dict_node['type'] = JSON_NODE_DATABASE
        elif(isinstance(node, MessageBroker)):
            dict_node['type'] = JSON_NODE_MESSAGE_BROKER
        elif(isinstance(node, MessageRouter)):
            dict_node['type'] = JSON_NODE_MESSAGE_ROUTER
        else:
            raise ExporterError(f"Node {n} not recognized")
        return dict_node

    def _transform_relationship(self, relationship):
        nrel = {}
        nrel['target'] = relationship.target.name
        nrel['source'] = relationship.source.name
        nrel[MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_TIMEOUT_PROPERTY] = relationship.timeout
        nrel[MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_CIRCUIT_BREAKER_PROPERTY] = relationship.circuit_breaker
        nrel[MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_DYNAMIC_DISCOVEY_PROPERTY] = relationship.dynamic_discovery
        if(isinstance(relationship, DeploymentTimeInteraction)):
            nrel['type'] = JSON_DEPLOYMENT_TIME
        elif(isinstance(relationship, RunTimeInteraction)):
            nrel['type'] = JSON_RUN_TIME
        else:
            raise ExporterError("{} Relationship not recognized.".format(relationship))
        return nrel

    def _transform_group(self, group):
        g_dict = {}
        g_dict['name'] = group.name
        if(isinstance(group, Edge)):
            g_dict['type'] = JSON_GROUPS_EDGE
        elif (isinstance(group, Team)):
            g_dict['type'] = JSON_GROUPS_TEAM
        else:
            raise ExporterError("Group type {} not recognized.".format(group))
        members = []
        for member in group.members:
            members.append(member.name)
        g_dict['members'] = members
        return g_dict
