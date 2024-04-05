from ..model import Relationship
from ..model import nodes
from .costants import SMELL_ENDPOINT_BASED_SERVICE_INTERACTION, SMELL_NO_API_GATEWAY, SMELL_SHARED_PERSISTENCY, SMELL_WOBBLY_SERVICE_INTERACTION_SMELL, SMELL_SINGLE_LAYER_TEAMS, SMELL_MULTIPLE_SERVICES_IN_ONE_CONTAINER, SMELL_TIGHTLY_COUPLED_TEAMS, SMELL_SHARED_BOUNDED_CONTEXT
from .costants import REFACTORING_ADD_SERVICE_DISCOVERY, REFACTORING_ADD_MESSAGE_ROUTER, REFACTORING_ADD_MESSAGE_BROKER, REFACTORING_ADD_CIRCUIT_BREAKER, REFACTORING_USE_TIMEOUT, REFACTORING_MERGE_SERVICES, REFACTORING_SPLIT_DATABASE, REFACTORING_ADD_DATA_MANAGER, REFACTORING_ADD_API_GATEWAY, REFACTORING_SPLIT_SERVICES, REFACTORING_SPLIT_TEAMS_BY_MICROSERVICE, REFACTORING_SPLIT_TEAMS_BY_COUPLING, REFACTORING_REORGANIZE_TEAMS_BY_BOUNDED_CONTEXT, REFACTORING_SPLIT_BOUNDED_CONTEXT_BY_TEAMS
class Smell(object):

    def __init__(self, name):
        self.nodes_cause = []
        self.links_cause = []
        self.name = name

    def addNodeCause(self, node):
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
            {"name": REFACTORING_ADD_MESSAGE_ROUTER, "description": "Add message router"},
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
        
        # add the message broker refactoring only if there exist
        # at least one target node that is not a messageRouter.
        add_mb_refactoring = False
        if isinstance(self.node, nodes.Service):
            for interaction in self.getLinkCause():
                if not isinstance(interaction.target, nodes.MessageRouter):
                    add_mb_refactoring = True
        
        refactorings = [{"name": REFACTORING_ADD_CIRCUIT_BREAKER, "description": " Add Circuit breaker"},
            {"name": REFACTORING_USE_TIMEOUT, "description": "Use timeouts in the interaction"}]
        if add_mb_refactoring:
            refactorings.insert(0,{"name": REFACTORING_ADD_MESSAGE_BROKER, "description": "Add Message broker"})
        return {**sup_dict, **{"refactorings": refactorings}}


class SharedPersistencySmell(NodeSmell):
    name: str = SMELL_SHARED_PERSISTENCY

    def __init__(self, node):
        super(SharedPersistencySmell, self).__init__(self.name, node)

    def __str__(self):
        return 'SharedPersistencySmell({})'.format(super(NodeSmell, self).__str__())

    def to_dict(self):
        sup_dict = super(SharedPersistencySmell, self).to_dict()
        return {**sup_dict, **{"refactorings": [
            {"name": REFACTORING_MERGE_SERVICES,"description": "Merge services accessing the same Datastore"},
            {"name": REFACTORING_SPLIT_DATABASE, "description": "Split the Datastore."},
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

class SingleLayerTeamsSmell(GroupSmell):
    name: str = SMELL_SINGLE_LAYER_TEAMS

    def __init__(self, group):
        super(SingleLayerTeamsSmell, self).__init__(self.name, group)

    def __str__(self):
        return 'SingleLayerTeams({})'.format(super(SingleLayerTeamsSmell, self).__str__())

    def to_dict(self):
        sup_dict = super(SingleLayerTeamsSmell, self).to_dict()
        return {**sup_dict, **{"refactorings": [
            {"name": REFACTORING_SPLIT_TEAMS_BY_MICROSERVICE, "description": "Split the teams by microservice."},
            ]}}

class MultipleServicesInOneContainerSmell(NodeSmell):
    name: str = SMELL_MULTIPLE_SERVICES_IN_ONE_CONTAINER

    def __init__(self, node):
        super(MultipleServicesInOneContainerSmell, self).__init__(self.name, node)

    def __str__(self):
        return 'MultipleServicesInOneContainerSmell({})'.format(super(NodeSmell, self).__str__())

    def to_dict(self):
        sup_dict = super(MultipleServicesInOneContainerSmell, self).to_dict()
        return {**sup_dict, **{"refactorings": [
            {"name": REFACTORING_SPLIT_SERVICES, "description": "Split containers in two pods"},
        ]}}

class TightlyCoupledTeamsSmell(GroupSmell):
    name: str = SMELL_TIGHTLY_COUPLED_TEAMS

    def __init__(self, group):
        super(TightlyCoupledTeamsSmell, self).__init__(self.name, group)

    def __str__(self):
        return 'TightlyCoupledTeams({})'.format(super(TightlyCoupledTeamsSmell, self).__str__())

    def to_dict(self):
        sup_dict = super(TightlyCoupledTeamsSmell, self).to_dict()
        return {**sup_dict, **{"refactorings": [
            {"name": REFACTORING_SPLIT_TEAMS_BY_COUPLING, "description": "Split the teams by coupling."},
            ]}}

class SharedBoundedContextSmell(GroupSmell):
    name: str = SMELL_SHARED_BOUNDED_CONTEXT

    def __init__(self, group):
        super(SharedBoundedContextSmell, self).__init__(self.name, group)

    def __str__(self):
        return 'SharedBoundedContext({})'.format(super(SharedBoundedContextSmell, self).__str__())

    def to_dict(self):
        sup_dict = super(SharedBoundedContextSmell, self).to_dict()
        return {**sup_dict, **{"refactorings": [
            {"name": REFACTORING_REORGANIZE_TEAMS_BY_BOUNDED_CONTEXT, "description": "Move the bounded context inside team borders."},
            {"name": REFACTORING_SPLIT_BOUNDED_CONTEXT_BY_TEAMS, "description": "Split bounded context among teams."},
            ]}}