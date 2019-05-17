from typing import List
from ..model import Root
from ..model import Relationship
from .costants import SMELL_ENDPOINT_BASED_SERVICE_INTERACTION, SMELL_NO_API_GATEWAY, SMELL_SHARED_PERSITENCY, SMELL_WOBBLY_SERVICE_INTERACTION_SMELL, SMELL_CROSS_TEAM_DATA_MANAGEMENT
from .costants import REFACTORING_ADD_SERVICE_DISCOVERY, REFACTORING_ADD_MESSAGE_ROUTER, REFACTORING_ADD_MESSAGE_BROKER, REFACTORING_ADD_CIRCUIT_BREAKER, REFACTORING_USE_TIMEOUT, REFACTORING_MERGE_SERVICES, REFACTORING_SPLIT_DATABASE, REFACTORING_ADD_DATA_MANAGER, REFACTORING_ADD_API_GATEWAY, REFACTORING_ADD_TEAM_DATA_MANAGER, REFACTORING_CHANGE_DATABASE_OWENRSHIP, REFACTORING_CHANGE_SERVICE_OWENRSHIP
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
        return len(self.getLinkCause()) == 0 and len(self.getNodeCause()) == 0

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
    name: str = SMELL_ENDPOINT_BASED_SERVICE_INTERACTION

    def __init__(self, node):
        super(EndpointBasedServiceInteractionSmell,
              self).__init__(self.name, node)

    def __str__(self):
        return 'EndpointBasedServiceInteractionSmell({})'.format(super(NodeSmell, self).__str__())

    def to_dict(self):
        sup_dict = super(EndpointBasedServiceInteractionSmell, self).to_dict()
        return {**sup_dict, **{"refactorings": [
            {"name": REFACTORING_ADD_SERVICE_DISCOVERY, "description": "Add Service discovery"},
            {"name": REFACTORING_ADD_MESSAGE_ROUTER, "description": "Add a message router"},
            {"name": REFACTORING_ADD_MESSAGE_BROKER, "description": " Add message broker"}
        ]}}


class WobblyServiceInteractionSmell(NodeSmell):
    name: str = SMELL_WOBBLY_SERVICE_INTERACTION_SMELL

    def __init__(self, node):
        super(WobblyServiceInteractionSmell, self).__init__(self.name, node)

    def __str__(self):
        return 'WobblyServiceInteractionSmell({})'.format(super(NodeSmell, self).__str__())

    def to_dict(self):
        sup_dict = super(WobblyServiceInteractionSmell, self).to_dict()
        return {**sup_dict, **{"refactorings": [
            {"name": REFACTORING_ADD_MESSAGE_BROKER, "description": "Add Message broker"},
            {"name": REFACTORING_ADD_CIRCUIT_BREAKER, "description": " Add Circuit breaker"},
            {"name": REFACTORING_USE_TIMEOUT, "description": "Use timeouts in the interaction"}]}}

class SharedPersistencySmell(NodeSmell):
    name: str = SMELL_SHARED_PERSITENCY

    def __init__(self, node):
        super(SharedPersistencySmell, self).__init__(self.name, node)

    def __str__(self):
        return 'SharedPersistencySmell({})'.format(super(NodeSmell, self).__str__())

    def to_dict(self):
        sup_dict = super(SharedPersistencySmell, self).to_dict()
        return {**sup_dict, **{"refactorings": [
            {"name": REFACTORING_MERGE_SERVICES,"description": "Merge services accesing the same database"},
            {"name": REFACTORING_SPLIT_DATABASE, "description": "Split the database."},
            {"name": REFACTORING_ADD_DATA_MANAGER, "description": " Add Data manager"}]}}

class NoApiGatewaySmell(NodeSmell):
    name: str = SMELL_NO_API_GATEWAY

    def __init__(self, node):
        super(NoApiGatewaySmell, self).__init__(self.name, node)

    def __str__(self):
        return 'NoApiGateway({})'.format(super(NoApiGatewaySmell, self).__str__())

    def to_dict(self):
        sup_dict = super(NoApiGatewaySmell, self).to_dict()
        return {**sup_dict, **{"refactorings": [{
            "name": REFACTORING_ADD_API_GATEWAY, "description": "Add an Api Gateway between the external user"}]}}

class CrossTeamDataManagementSmell(GroupSmell):
    name: str = SMELL_CROSS_TEAM_DATA_MANAGEMENT

    def __init__(self, group):
        super(CrossTeamDataManagementSmell, self).__init__(self.name, group)

    def __str__(self):
        return 'CrossTeamDataManagement({})'.format(super(CrossTeamDataManagementSmell, self).__str__())

    def to_dict(self):
        sup_dict = super(CrossTeamDataManagementSmell, self).to_dict()
        return {**sup_dict, **{"refactorings": [
            {"name": REFACTORING_ADD_TEAM_DATA_MANAGER, "description": "Move the database to another team"},
            {"name": REFACTORING_CHANGE_DATABASE_OWENRSHIP, "description": "Move the database to another team"},
            {"name": REFACTORING_CHANGE_SERVICE_OWENRSHIP, "description": "Move the service to another team"},
            ]}}