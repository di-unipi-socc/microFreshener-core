'''
nodes module
'''

from .relationships import DeploymentTimeInteraction, RunTimeInteraction, InteractsWith
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

    @property
    def interactions(self):
        return self._interactions

    @property
    def incoming_interactions(self):
        return self.up_interactions
    
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
            raise MicroToscaModelError(f"Interaction {item} from {self} to {item.target} already exist")
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


    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

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

class MessageRouter(CommunicationPattern):

    def __init__(self, name):
        super(MessageRouter, self).__init__(name, "MR")

class Datastore(Root):

    def __init__(self, name):
        super(Datastore, self).__init__(name)

    def __str__(self):
        return '{} ({})'.format(self.name, 'Datastore')


