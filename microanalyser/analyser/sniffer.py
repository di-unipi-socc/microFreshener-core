
from abc import ABCMeta, abstractmethod
from .smell import NodeSmell, EndpointBasedServiceInteractionSmell, NoApiGatewaySmell, WobblyServiceInteractionSmell, SharedPersistencySmell
from ..model.nodes import Service, Database
from ..model.template import  MicroModel
from typing import List

from ..helper.decorator import visitor


class NodeSmellSniffer(metaclass=ABCMeta):
    
    def __init__(self):
        pass
    
    @abstractmethod
    def snif(self, node)->NodeSmell:
        pass

class EndpointBasedServiceInteractionSmellSniffer(NodeSmellSniffer):
    
    def __str__(self):
        return 'DirectInteraction({})'.format(super(NodeSmellSniffer, self).__str__())
    
    # TODO: add decorator for sniffing only service node
    @visitor(Service)
    def snif(self, node):
        print("Visiting service")
        bad_interactions = [up_rt for up_rt in node.up_run_time_requirements if isinstance(up_rt.source, Service)]
        if (bad_interactions):
            return  EndpointBasedServiceInteractionSmell(node, bad_interactions)
        else:
            return None
    
    @visitor(MicroModel)
    def snif(self, micro_model):
         print("visiting al lthe nodes in the graph")
         # for all nodes in  graph
         #  snif node

class WobblyServiceInteractionSmellSniffer(NodeSmellSniffer):
    
    def __str__(self):
        return 'WobblyServiceInteractionSmellSniffer({})'.format(super(NodeSmellSniffer, self).__str__())
    
    # TODO: add decorator for sniffing only service node
    @visitor(Service)
    def snif(self, node):
        # TODO: check also if there is a path from the node to a service node without a circuit breaker
        bad_interactions = [rt for rt in node.run_time if (isinstance(rt.target, Service))]
        if (bad_interactions):
            return  WobblyServiceInteractionSmell(node, bad_interactions)
        else:
            return None
    
    @visitor(MicroModel)
    def snif(self, micro_model):
         print("visiting al lthe nodes in the graph")
         # for all nodes in  graph
         #  snif node

class SharedPersistencySmellSniffer(NodeSmellSniffer):
    
    def __str__(self):
        return 'SharedPersistencySmellSniffer({})'.format(super(NodeSmellSniffer, self).__str__())

    @visitor(Database)
    def snif(self, node):
        if(len(set(node.incoming)) > 1): 
            return  SharedPersistencySmell(node, list(node.incoming))
        else:
            return None
    
    @visitor(MicroModel)
    def snif(self, micro_model):
         print("visiting al lthe nodes in the graph")
         # for all nodes in  graph
         #  snif node

class NoApiGatewaySmellSniffer(NodeSmellSniffer):
    
    def __str__(self):
        return 'NoApiGatewaySmellSniffer({})'.format(super(NodeSmellSniffer, self).__str__())
    
    # TODO: add decorator for snipffing only service node
    def snif(self, node):
        # TODO: check if the node is Edge node (is in the group of nodes taht can be accessed to the external)
        bad_interaction = []
        for up_rt in node.up_run_time_requirements:
            if isinstance(up_rt.source, CommunicationPattern):
                if(up_rt.source.concrete_type != "ApiGateway"):
                    smell.add_single_interaction(up_rt)
        if (bad_interaction):
            return  NoApiGatewaySmell(node, bad_interaction)
        else:
            None


    