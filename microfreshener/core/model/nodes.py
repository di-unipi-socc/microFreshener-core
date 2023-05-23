'''
nodes module
'''

from .relationships import DeploymentTimeInteraction, RunTimeInteraction, InteractsWith, DeployedOn
from ..logging import MyLogger
from ..errors import MicroToscaModelError

logger = MyLogger().get_logger()


class Root(object):

    def __init__(self, name):
        self.name = name

        # Requirements
        self._interactions = []

        # Incoming interaction of a node
        self.up_interactions = []


        # Outcoming DeployedOn relations
        self._deployed_on = []

    @property
    def interactions(self):
        return self._interactions

    @property
    def incoming_interactions(self):
        return self.up_interactions

    @property
    def deployed_on(self):
        return self._deployed_on

    def add_incoming_interaction(self, interaction):
        self.up_interactions.append(interaction)

    # Add a interactWith interaction from source node to target node.
    # Only Service and MessagRoouter can be source of a relation (checkd in the InteractWith costructor)
    def add_interaction(self, item, with_timeout=False, with_circuit_breaker=False, with_dynamic_discovery=False):
        if not isinstance(item, InteractsWith):
            item = InteractsWith(self, item, with_timeout=with_timeout,
                                 with_circuit_breaker=with_circuit_breaker,
                                 with_dynamic_discovery=with_dynamic_discovery)
        if (item in self._interactions):
            raise MicroToscaModelError(
                f"Interaction {item} from {self} to {item.target} already exist")
        self._interactions.append(item)
        if not isinstance(item.target, str):
            item.target.add_incoming_interaction(item)
        return item

    def remove_interaction(self, interaction):
        if interaction in self._interactions:
            self._interactions.remove(interaction)
        interaction.target.remove_incoming_interaction(interaction)

    def remove_incoming_interaction(self, interaction):
        if interaction in self.up_interactions:
            self.up_interactions.remove(interaction)

    # Adds a deployedOn interaction from source node (self) to target node. Only Service can be source of the relation
    # and only Compute can be the target
    def add_deployed_on(self, item):
        if not isinstance(item, DeployedOn):
            item = DeployedOn(source=self, target=item)

        if item in self._deployed_on:
            raise MicroToscaModelError(f"Interaction {item} from {self} to {item.target} already exist")

        self._deployed_on.append(item)
        if not isinstance(item.target, str):
            item.target.add_deploy(item)
        return item

    def remove_deployed_on(self, link):
        if link in self._deployed_on:
            self._deployed_on.remove(link)
        link.target.remove_deploy(link)

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name  # and type(self) == type(other)

    def __hash__(self):
        return hash(self.name)

    def to_dict(self):
        return {'name': self.name}


class Software(Root):

    def __init__(self, name):
        super(Software, self).__init__(name)


class Service(Software):

    def __init__(self, name):
        super(Service, self).__init__(name)

    def __str__(self):
        return '{} ({})'.format(self.name, 'service')


class Compute(Root):

    def __init__(self, name):
        super(Compute, self).__init__(name)

        # Incoming DeployedOn relations
        self._deploys: list = []

    def __str__(self):
        return '{} ({})'.format(self.name, 'compute')

    @property
    def deploys(self):
        return self._deploys

    def add_deploy(self, relation):
        self._deploys.append(relation)

    def remove_deploy(self, deploys):
        if deploys in self._deploys:
            self._deploys.remove(deploys)


class CommunicationPattern(Software):

    def __init__(self, name, short_name="CP"):
        super(CommunicationPattern, self).__init__(name)
        self.short_name = short_name

    def __str__(self):
        return '{} ({})'.format(self.name, self.short_name)


class MessageBroker(CommunicationPattern):

    def __init__(self, name):
        super(MessageBroker, self).__init__(name, "MB")

    def __str__(self):
        return '{} ({})'.format(self.name, self.short_name)


class Datastore(Root):

    def __init__(self, name):
        super(Datastore, self).__init__(name)

    def __str__(self):
        return '{} ({})'.format(self.name, 'Datastore')


class MessageRouter(CommunicationPattern):

    def __init__(self, name, label="MR"):
        self.label = label
        super(MessageRouter, self).__init__(name, label)


class KService(MessageRouter):

    def __init__(self, name, selector=None, stype=None):
        self._selector = selector  # {<key>:<value>}
        # LoadBalancer | NodePort :for knowing if the service is acessed by external
        self._type = stype

        super(KService, self).__init__(name, "KS")

    @property
    def service_type(self):
        return self._type

    @property
    def selector(self):
        return self._selector

    def is_external_accessed(self):
        return self.service_type == "LoadBalancer" or self.service_type == "NodePort"

    def __str__(self):
        return '{} ({})'.format(self.name, 'Kservice')


class KIngress(MessageRouter):

    def __init__(self, name, backends=[]):
        self.backend_services = backends
        super(KIngress, self).__init__(name, "KIngress")

    @property
    def backends(self):
        return self.backend_services

    def add_service_name(self, name):
        self.backend_services.append(name)


class KProxy(MessageRouter):

    def __init__(self, name):
        super(KProxy, self).__init__(name, "KProxy")
