
from abc import ABCMeta, abstractmethod
from .smell import NodeSmell, CrossTeamDataManagementSmell, EndpointBasedServiceInteractionSmell, NoApiGatewaySmell, WobblyServiceInteractionSmell, SharedPersistencySmell
from ..model import Service, Database, CommunicationPattern, MessageRouter
from ..model.type import MICROTOSCA_NODES_MESSAGE_ROUTER
from ..model import MicroToscaModel
from ..model.groups import Edge, Team
from typing import List

from ..helper.decorator import visitor


class NodeSmellSniffer(metaclass=ABCMeta):

    @abstractmethod
    def snif(self, node)->NodeSmell:
        pass


class GroupSmellSniffer(metaclass=ABCMeta):

    def __init__(self, micromodel: MicroToscaModel):
        self.micro_model = micromodel

    @abstractmethod
    def snif(self, group):
        pass



class EndpointBasedServiceInteractionSmellSniffer(NodeSmellSniffer):

    def __str__(self):
        return 'EndpointBasedServiceInteractionSniffer({})'.format(super(NodeSmellSniffer, self).__str__())

    @visitor(Service)
    def snif(self, node):
        smell = EndpointBasedServiceInteractionSmell(node)
        for up_rt in node.up_run_time_requirements:
            if(isinstance(up_rt.source, Service)) and up_rt.dynamic_discovery == False:
                smell.addLinkCause(up_rt)
        return smell

    @visitor(MicroToscaModel)
    def snif(self, micro_model):
        print("visiting all the nodes in the graph")


class WobblyServiceInteractionSmellSniffer(NodeSmellSniffer):

    def __str__(self):
        return 'WobblyServiceInteractionSmellSniffer({})'.format(super(NodeSmellSniffer, self).__str__())

    @visitor(Service)
    def snif(self, node):
        smell = WobblyServiceInteractionSmell(node)
        for rt in node.run_time:
            if ((isinstance(rt.target, Service) or isinstance(rt.target, MessageRouter)) and rt.circuit_breaker == False and rt.timeout == False):
                smell.addLinkCause(rt)
        return smell

    @visitor(MicroToscaModel)
    def snif(self, micro_model):
        print("visiting al lthe nodes in the graph")


class SharedPersistencySmellSniffer(NodeSmellSniffer):

    def __str__(self):
        return 'SharedPersistencySmellSniffer({})'.format(super(NodeSmellSniffer, self).__str__())

    @visitor(Database)
    def snif(self, database)->SharedPersistencySmell:
        smell = SharedPersistencySmell(database)
        nodes = set(link.source for link in database.incoming)
        if (len(nodes) > 1):
            for link in database.incoming:
                smell.addLinkCause(link)
        return smell

    @visitor(MicroToscaModel)
    def snif(self, micro_model):
        print("visiting all the nodes in the graph")


class NoApiGatewaySmellSniffer(GroupSmellSniffer):

    def __str__(self):
        return 'NoApiGatewaySmellSniffer({})'.format(super(GroupSmellSniffer, self).__str__())

    @visitor(Edge)
    def snif(self, group: Edge)->[NoApiGatewaySmell]:
        foundNoApiGatewaySmells = []
        for node in group.members:
            if not isinstance(node, MessageRouter):
                smell = NoApiGatewaySmell(node)
                smell.addNodeCause(node)
                foundNoApiGatewaySmells.append(smell)
        return foundNoApiGatewaySmells


class CrossTeamDataManagementSmellSniffer(GroupSmellSniffer):

    def snif(self, group: Team)->CrossTeamDataManagementSmell:
        smell = CrossTeamDataManagementSmell(group)
        for node in group.members:
            for relationship in node.relationships:
                source_node = relationship.source
                target_node = relationship.target
                source_squad = self.micro_model.squad_of(source_node)
                target_squad = self.micro_model.squad_of(target_node)
                if (isinstance(source_node, Service) and isinstance(target_node, Database)
                        and source_squad != target_squad):
                    smell.addLinkCause(relationship)
        return smell

    def __str__(self):
        return 'CrossTeamDataManagementSmellSniffer({})'.format(super(GroupSmellSniffer, self).__str__())
