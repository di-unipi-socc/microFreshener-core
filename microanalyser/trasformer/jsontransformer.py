import json

from ..model.template import MicroModel
from ..model.relationships import RunTimeInteraction, DeploymentTimeInteraction
from ..model.nodes import Root, Service, Database, CommunicationPattern, MessageBroker, MessageRouter
from ..model.groups import Edge, Squad

from ..model.type import API_GATEWAY, MESSAGE_BROKER, CIRCUIT_BREAKER
from ..model.type import INTERACT_WITH_TIMEOUT_PROPERTY, INTERACT_WITH_CIRCUIT_BREAKER_PROPERTY, INTERACT_WITH_DYNAMIC_DISCOVEY_PROPERTY
from ..errors import ExporterError
from .itransformer import Transformer

class JSONTransformer(Transformer):

    def __init__(self):
        pass

    # Transform a microModel Oject to a Dicionary format.
    # @input:  microModel
    # @return: python dictionary
    def transform(self, micro_model:MicroModel):
        return self.serialize(micro_model)
        # TODO: returns a JSON object instead of dict
        # ATTENTION: in the restfule api the Response() object requires a dict that are than converted into json
        # return json.dumps(self.serialize(micro_model), ensure_ascii=False)

    def serialize(self, obj):
        d = {}
        if (isinstance(obj, MicroModel)):
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
            dict_node['type'] = "service"
        elif(isinstance(node, Database)):
            dict_node['type'] = "database"
        elif(isinstance(node, MessageBroker)):
            dict_node['type'] = "messagebroker"
        elif(isinstance(node, MessageRouter)):
            dict_node['type'] = "messagerouter"
        else:
            raise ExporterError(f"Node {n} not recognized")
        return dict_node

    def _transform_relationship(self, relationship):
        nrel = {}
        nrel['target'] = relationship.target.name
        nrel['source'] = relationship.source.name
        nrel[INTERACT_WITH_TIMEOUT_PROPERTY] = relationship.timeout
        nrel[INTERACT_WITH_CIRCUIT_BREAKER_PROPERTY] = relationship.circuit_breaker
        nrel[INTERACT_WITH_DYNAMIC_DISCOVEY_PROPERTY] = relationship.dynamic_discovery
        if(isinstance(relationship, DeploymentTimeInteraction)):
            nrel['type'] = 'deploymenttime'
        elif(isinstance(relationship, RunTimeInteraction)):
            nrel['type'] = 'runtime'
        else:
            raise ExporterError("{} Relationship not recognized.".format(relationship))
        return nrel

    def _transform_group(self, group):
        g_dict = {}
        g_dict['name'] = group.name
        if(isinstance(group, Edge)):
            g_dict['type'] = "edgegroup"
        elif (isinstance(group, Squad)):
            g_dict['type'] = "squadgroup"
        else:
            raise ExporterError("Group type {} not recognized.".format(group))
        members = []
        for member in group.members:
            members.append(member.name)
        g_dict['members'] = members
        return g_dict
