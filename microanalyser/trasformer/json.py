import json

from ..model.template import MicroModel
from ..model.relationships import RunTimeInteraction, DeploymentTimeInteraction
from ..model.nodes import Root, Service, Database, CommunicationPattern
from ..model.groups import Edge, Squad

from ..loader.type import API_GATEWAY, MESSAGE_BROKER, CIRCUIT_BREAKER

class JSONTransformer(object):

    def __init__(self):
        pass

    # Transform a microModel Oject to a Dicionary format.
    # @input:  microModel
    # @return: JSON string
    def transform(self, micro_model):
        return self.serialize(micro_model)
        # TODO: returns a JSON object instead of dict
        # ATTENTIOn: in the restfule api the Response() object requires a dict that are than converted into json
        # return json.dumps(self.serialize(micro_model), ensure_ascii=False)

    def serialize(self, obj):
        d = {}
        if (isinstance(obj, MicroModel)):
            d["name"] = obj.name  # name of the models
            d['nodes'] = []      # nodes
            d['links'] = []      # links
            d['groups'] = []
            for n in obj.nodes:
                ndict = {}
                ndict['name'] = n.name
                if(isinstance(n, Service)):
                    ndict['type'] = "service"
                elif(isinstance(n, Database)):
                    ndict['type'] = "database"
                elif(isinstance(n, CommunicationPattern)):
                    ndict['type'] = "communicationpattern"
                    if(n.concrete_type == API_GATEWAY ):
                        ndict['ctype'] = "ApiGateway"
                    elif  (n.concrete_type == MESSAGE_BROKER ):
                        ndict['ctype'] = "MessageBroker"
                    elif  (n.concrete_type == CIRCUIT_BREAKERI ):
                        ndict['ctype'] = "CircuitBreaker"
                    else:
                        raise ValueError("Concrete type {} not recognized".format(n.concrete_type))
                else:
                    # TODO throw an excpetion ?? Node not found
                    ndict['type'] = None
                d['nodes'].append(ndict)

                for rel in n.relationships:
                    d['links'].append(self._transform_relationship(rel))
            for group in obj.groups:
                d['groups'].append(self._transform_group(group))
        return d

    def _transform_relationship(self, relationship):
        nrel = {}
        nrel['target'] = relationship.target.name
        nrel['source'] = relationship.source.name
        nrel['timeout'] = relationship.timedout
        if(isinstance(relationship, DeploymentTimeInteraction)):
            nrel['type'] = 'deploymenttime'
        elif(isinstance(relationship, RunTimeInteraction)):
            nrel['type'] = 'runtime'
        else:
            raise ValueError("{} Relationship not recognized.".format(relationship))
        return nrel

    def _transform_group(self, group):
        g_dict = {}
        g_dict['name'] = group.name
        if(isinstance(group, Edge)):
            g_dict['type'] = "edgegroup"
        elif (isinstance(group, Squad)):
            g_dict['type'] = "squadgroup"
        else:
            raise ValueError("Group type {} not recognized.".format(group))
        members = []
        for member in group.members:
            members.append(member.name)
        g_dict['members'] = members
        return g_dict
