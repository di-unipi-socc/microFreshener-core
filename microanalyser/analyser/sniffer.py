
from abc import ABCMeta, abstractmethod
from .smell import NodeSmell, EndpointBasedServiceInteractionSmell, NoApiGatewaySmell, WobblyServiceInteractionSmell, SharedPersistencySmell
from ..model.nodes import Service, Database, CommunicationPattern
from ..loader.type import API_GATEWAY
from ..model.template import MicroModel
from ..model.groups import Edge
from typing import List

from ..helper.decorator import visitor


class NodeSmellSniffer(metaclass=ABCMeta):

    @abstractmethod
    def snif(self, node)->NodeSmell:
        pass


class GroupSmellSniffer(metaclass=ABCMeta):

    @abstractmethod
    def snif(self, group):
        pass


class EndpointBasedServiceInteractionSmellSniffer(NodeSmellSniffer):

    def __str__(self):
        return 'DirectInteraction({})'.format(super(NodeSmellSniffer, self).__str__())

    # TODO: add decorator for sniffing only service node
    @visitor(Service)
    def snif(self, node):
        bad_interactions = [up_rt for up_rt in node.up_run_time_requirements if isinstance(
            up_rt.source, Service)]
        if (bad_interactions):
            return EndpointBasedServiceInteractionSmell(node, bad_interactions)
        else:
            return None

    @visitor(MicroModel)
    def snif(self, micro_model):
        print("visiting all the nodes in the graph")
        # for all nodes in  graph
        #  snif node


class WobblyServiceInteractionSmellSniffer(NodeSmellSniffer):

    def __str__(self):
        return 'WobblyServiceInteractionSmellSniffer({})'.format(super(NodeSmellSniffer, self).__str__())

    # TODO: add decorator for sniffing only service node
    @visitor(Service)
    def snif(self, node):
        # TODO: check also if there is a path from the node to a service node without a circuit breaker
        bad_interactions = [rt for rt in node.run_time if (
            isinstance(rt.target, Service)) and not rt.timedout]
        if (bad_interactions):
            return WobblyServiceInteractionSmell(node, bad_interactions)
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
            return SharedPersistencySmell(node, list(node.incoming))
        else:
            return None

    @visitor(MicroModel)
    def snif(self, micro_model):
        print("visiting all the nodes in the graph")
        # for all nodes in  graph
        #  snif node


class NoApiGatewaySmellSniffer(GroupSmellSniffer):

    def __str__(self):
        return 'NoApiGatewaySmellSniffer({})'.format(super(GroupSmellSniffer, self).__str__())

    # MAybe NoApiGatewaySmlle is a GroupSmell not a nodeSmell ?!!!
    def snif(self, group: Edge)->[NoApiGatewaySmell]:
        nodes_with_smell = []
        for node in group.members:
            if isinstance(node, CommunicationPattern) and node.concrete_type == API_GATEWAY:
                pass  # do not consider API_gateway nodes.
            else:
                gw_is_found = False
                # TODO: check if the node has not a "ignore once" or "ignore forever" flag.
                for up_relationship in node.incoming:
                    source = up_relationship.source
                    # check if the source node is in the same group
                    if isinstance(source, CommunicationPattern) and source in group:
                        if(source.concrete_type == API_GATEWAY):
                            gw_is_found = True
                if(not gw_is_found):
                    nodes_with_smell.append(node)

        return NoApiGatewaySmell(group, nodes_with_smell)
