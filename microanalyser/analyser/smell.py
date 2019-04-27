from typing import List
from ..model.nodes import Root
from ..model.relationships import Relationship


class Smell(object):

    def __init__(self, name):
        self.nodes_cause = []
        self.links_cause = []
        self.name = name

    def addNodeCause(self, node: Root):
        self.nodes_cause.append(node)

    def getNodeCause(self):
        return self.nodes_cause

    def addLinkCause(self, link: Relationship):
        self.links_cause.append(link)

    def getLinkCause(self):
        return self.links_cause

    def to_dict(self):
        return {"name": self.name,
                "nodes": [node.name for node in self.getNodeCause()],
                "links": [interation.to_dict() for interation in self.getLinkCause()]}

    def isEmpty(self):
        return len(self.getLinkCause()) == 0  and len(self.getNodeCause()) == 0

    def __hash__(self):
        return hash(self.name)


class NodeSmell(Smell):

    def __init__(self, name, node):
        super(NodeSmell, self).__init__(name)
        self._node = node

    @property
    def node(self):
        return self._node


class GroupSmell(Smell):

    def __init__(self, name, group):
        super(GroupSmell, self).__init__(name)
        self._group = group

    @property
    def group(self):
        return self._group


class EndpointBasedServiceInteractionSmell(NodeSmell):
    name: str = "EndpointBasedServiceInteractionSmell"

    def __init__(self, node):
        super(EndpointBasedServiceInteractionSmell,
              self).__init__(self.name, node)

    def __str__(self):
        return 'EndpointBasedServiceInteractionSmell({})'.format(super(NodeSmell, self).__str__())

    def to_dict(self):
        sup_dict = super(EndpointBasedServiceInteractionSmell, self).to_dict()
        return {**sup_dict, **{"refactorings": [
            {"name": "Add Service Discovery",
                "description": "Add Service discovery"},
            {"name": "Add Message Router", "description": "Add a message router"},
            {"name": "Add Message Broker", "description": " Add message broker"}
        ]}}


class WobblyServiceInteractionSmell(NodeSmell):
    name: str = "WobblyServiceInteractionSmell"

    def __init__(self, node):
        super(WobblyServiceInteractionSmell, self).__init__(self.name, node)

    def __str__(self):
        return 'WobblyServiceInteractionSmell({})'.format(super(NodeSmell, self).__str__())

    def to_dict(self):
        sup_dict = super(WobblyServiceInteractionSmell, self).to_dict()
        return {**sup_dict, **{"refactorings": [
            {"name": "Add Message Broker", "description": "Add Message broker"},
            {"name": "Add Circuit Breaker", "description": " Add Circuit breaker"},
            {"name": "Use Timeouts", "description": "Use timeouts"}]}}


class SharedPersistencySmell(NodeSmell):
    name: str = "SharedPersistencySmell"

    def __init__(self, node):
        super(SharedPersistencySmell, self).__init__(self.name, node)

    def __str__(self):
        return 'SharedPersistencySmell({})'.format(super(NodeSmell, self).__str__())

    def to_dict(self):
        sup_dict = super(SharedPersistencySmell, self).to_dict()
        return {**sup_dict, **{"refactorings": [
            {"name": "Merge services",
                "description": "Merge services accesing the same database"},
            {"name": "Split Database", "description": "Split the database."},
            {"name": "Add Data Manager", "description": " Add Data manager"}]}}


class NoApiGatewaySmell(GroupSmell):
    name: str = "NoApiGateway"

    def __init__(self, group):
        super(NoApiGatewaySmell, self).__init__(self.name, group)

    def __str__(self):
        return 'NoApiGateway({})'.format(super(NoApiGatewaySmell, self).__str__())

    def to_dict(self):
        sup_dict = super(NoApiGatewaySmell, self).to_dict()
        return {**sup_dict, **{"refactorings": [{
            "name": "Add Api Gateway", "description": "Add an Api Gateway between the external user"}]}}


class SingleLayerTeamSmell(GroupSmell):
    name: str = "SingleLayerTeam"

    def __init__(self, group):
        super(SingleLayerTeamSmell, self).__init__(self.name, group)

    def __str__(self):
        return 'SingleLayerTeam({})'.format(super(SingleLayerTeamSmell, self).__str__())

    def to_dict(self):
        sup_dict = super(SingleLayerTeamSmell, self).to_dict()
        return {**sup_dict, **{"refactorings": [{
            "name": "Move Database", "description": "Move the database to another team"}]}}
