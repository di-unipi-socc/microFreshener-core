
from abc import ABCMeta, abstractmethod
from .smell import NodeSmell, SingleLayerTeamsSmell, EndpointBasedServiceInteractionSmell, NoApiGatewaySmell, TightlyCoupledTeamsSmell, \
    WobblyServiceInteractionSmell, SharedPersistencySmell, MultipleServicesInOneContainerSmell, SharedBoundedContextSmell
from ..model import Service, Datastore, CommunicationPattern, MessageRouter, Compute
from ..model.type import MICROTOSCA_NODES_MESSAGE_ROUTER
from ..model import MicroToscaModel
from ..model.groups import Edge, Team
from typing import List

from ..helper.decorator import visitor

import sys

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
        for up_rt in node.incoming_interactions:
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
        for rt in node.interactions:
            if ((isinstance(rt.target, Service) or isinstance(rt.target, MessageRouter)) and rt.circuit_breaker == False and rt.timeout == False):
                smell.addLinkCause(rt)
        return smell

    @visitor(MicroToscaModel)
    def snif(self, micro_model):
        print("visiting al lthe nodes in the graph")


class SharedPersistencySmellSniffer(NodeSmellSniffer):

    def __str__(self):
        return 'SharedPersistencySmellSniffer({})'.format(super(NodeSmellSniffer, self).__str__())

    @visitor(Datastore)
    def snif(self, Datastore)->SharedPersistencySmell:
        smell = SharedPersistencySmell(Datastore)
        nodes = set(link.source for link in Datastore.incoming_interactions)
        if (len(nodes) > 1):
            for link in Datastore.incoming_interactions:
                smell.addLinkCause(link)
        return smell

    @visitor(MicroToscaModel)
    def snif(self, micro_model):
        print("visiting all the nodes in the graph")


class NoApiGatewaySmellSniffer(GroupSmellSniffer):

    def __str__(self):
        return 'NoApiGatewaySmellSniffer({})'.format(super(GroupSmellSniffer, self).__str__())

    @visitor(Edge)
    def snif(self, group: Edge) -> [NoApiGatewaySmell]:
        foundNoApiGatewaySmells = []
        for node in group.members:
            if not isinstance(node, MessageRouter):
                smell = NoApiGatewaySmell(node)
                smell.addNodeCause(node)
                foundNoApiGatewaySmells.append(smell)
        return foundNoApiGatewaySmells


class SingleLayerTeamsSmellSniffer(GroupSmellSniffer):

    def __str__(self):
        return 'SingleLayerTeamsSmellSniffer({})'.format(super(GroupSmellSniffer, self).__str__())

    def _not_internally_linked(self, node):
        same_squad = self.micro_model.squad_of(node)
        for link in (node.interactions + node.incoming_interactions):
            source_squad = self.micro_model.squad_of(link.source)
            target_squad = self.micro_model.squad_of(link.target)
            if (link.target is node and source_squad is same_squad) or (link.source is node and target_squad is same_squad):
                return False
        return True


    @visitor(Team)
    def snif(self, group: Team) -> SingleLayerTeamsSmell:
        smell = SingleLayerTeamsSmell(group)
        for node in group.members:
            for relationship in node.interactions:
                source_node = relationship.source
                target_node = relationship.target
                source_squad = self.micro_model.squad_of(source_node)
                target_squad = self.micro_model.squad_of(target_node)
                if (source_squad is not None and
                    target_squad is not None and
                    source_squad != target_squad and
                    isinstance(source_node, Service) and
                    not isinstance(target_node, Service) and
                    (isinstance(target_node, Datastore) or self._not_internally_linked(target_node))):
                        smell.addLinkCause(relationship)
        return smell

class MultipleServicesInOneContainerSmellSniffer(NodeSmellSniffer):

    def __str__(self):
        return 'MultipleServicesInOneContainerSmellSniffer({})'.format(super(NodeSmellSniffer, self).__str__())

    @visitor(Compute)
    def snif(self, node) -> MultipleServicesInOneContainerSmell:
        smell = MultipleServicesInOneContainerSmell(node)
        nodes = set(link.source for link in node.deploys)
        if (len(nodes) > 1):
            for link in node.deploys:
                smell.addLinkCause(link)
        return smell

    @visitor(MicroToscaModel)
    def snif(self, micro_model):
        print("visiting all the nodes in the graph")

class TightlyCoupledTeamsSmellSniffer(GroupSmellSniffer):

    def __str__(self):
        return 'TightlyCoupledTeamsSmellSniffer({})'.format(super(GroupSmellSniffer, self).__str__())
    
    GRAPH_DEGREE_COUPLING = "graph-degree-coupling"

    def _get_coupling_measure(self, criterion):
        if criterion == self.GRAPH_DEGREE_COUPLING:
            return self._graph_degree_coupling

    def _graph_degree_coupling(self, link):
        source_node = link.source
        target_node = link.target
        if source_node != target_node:
            return 1
        else:
            return sys.maxsize

    @visitor(Team)
    def snif(self, group: Team) -> TightlyCoupledTeamsSmell:
        smell = TightlyCoupledTeamsSmell(group)
        coupling = self._get_coupling_measure(self.GRAPH_DEGREE_COUPLING)
        for node in group.members:
            coupled_squads = { group: 0 }
            for relationship in (node.interactions + node.incoming_interactions):
                source_node = relationship.source
                source_squad = self.micro_model.squad_of(source_node)
                target_node = relationship.target
                target_squad = self.micro_model.squad_of(target_node)
                if node is source_node and target_squad is not None:
                    coupled_squads[target_squad] = coupled_squads.get(target_squad, 0) + coupling(relationship)
                elif node is target_node and source_squad is not None:
                    coupled_squads[source_squad] = coupled_squads.get(source_squad, 0) + coupling(relationship)
            most_interacting_squads = [squad for squad, count in coupled_squads.items() if count == max(coupled_squads.values())]
            if group not in most_interacting_squads:
                smell.addNodeCause(node)
        return smell

class SharedBoundedContextSmellSniffer(GroupSmellSniffer):

    def __str__(self):
        return 'SharedBoundedContextSmellSniffer({})'.format(super(GroupSmellSniffer, self).__str__())

    def _is_datastore_linked_to_other_squads(self, node, nsquads, *args, **kwargs):
        squads = []
        for link in node.incoming_interactions:
            source_node = link.source
            source_squad = self.micro_model.squad_of(source_node)
            if source_squad is not None:
                if source_squad not in squads and source_squad not in kwargs.get('exclude', []):
                    squads.append(source_squad)
                if len(squads) > nsquads:
                    return True
        return False

    @visitor(Team)
    def snif(self, group: Team) -> SharedBoundedContextSmell:
        smell = SharedBoundedContextSmell(group)
        for node in group.members:
            if(isinstance(node, Datastore)):
                if self._is_datastore_linked_to_other_squads(node, 2):
                    smell.addLinkCause(relationship)
            elif(isinstance(node, Service)):
                for relationship in node.interactions:
                    target_node = relationship.target
                    if isinstance(target_node, Datastore):
                        target_squad = self.micro_model.squad_of(target_node)
                        if target_squad is not group and self._is_datastore_linked_to_other_squads(target_node, 1, exclude=group):
                                smell.addLinkCause(relationship)
        return smell
