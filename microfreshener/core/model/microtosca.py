'''
MicroModelModel module
'''
import six
from .nodes import Root, Service, Datastore, CommunicationPattern, MessageRouter, MessageBroker
from .relationships import InteractsWith, DeploymentTimeInteraction, RunTimeInteraction
from .groups import Team, Edge
from ..errors import MicroToscaModelError
from ..logging import MyLogger

logger = MyLogger().get_logger()


class MicroToscaModel:

    def __init__(self, name):
        self._nodes = {}
        self._groups = {}
        self.name = name

    @property
    def nodes(self):
        return (v for k, v in self._nodes.items())

    @property
    def services(self):
        return (v for k, v in self._nodes.items() if isinstance(v, Service))

    @property
    def datastores(self):
        return (v for k, v in self._nodes.items() if isinstance(v, Datastore))

    @property
    def communication_patterns(self):
        return (v for k, v in self._nodes.items() if isinstance(v, CommunicationPattern))
    
    @property
    def message_routers(self):
        return (v for k, v in self._nodes.items() if isinstance(v, MessageRouter))
    
    @property
    def message_brokers(self):
        return (v for k, v in self._nodes.items() if isinstance(v, MessageBroker))

    @property
    def groups(self):
        return (v for k, v in self._groups.items())

    @property
    def squads(self):
        return (v for k, v in self._groups.items() if isinstance(v, Team))

    @property
    def edges(self):
        return (v for k, v in self._groups.items() if isinstance(v, Edge))

    def add_node(self, node):
        self._nodes[node.name] = node
        logger.debug("Added node {}".format(node))
        return node

    def delete_node(self, node):
        for rel in node.interactions:
            rel.target.remove_incoming_interaction(rel)
        for up_rel in node.incoming_interactions:
            up_rel.source.remove_interaction(up_rel)
        logger.debug(f"Deleted node {node}")
        del self._nodes[node.name]

    def get_relationship(self, id):
        for node in self.nodes:
            for interacion in node.interactions:
                if(interacion.id == id):
                    return interacion
        return None

    def delete_relationship(self, interaction):
        interaction.source.remove_interaction(interaction)
        logger.debug(f"Removed {interaction} interaction ")

    def add_group(self, group):
        self._groups[group.name] = group
        logger.debug("Added group {}".format(group))

    def get_group(self, name):
        return self._groups.get(name, None)

    def get_squad(self, name):
        return self._groups.get(name, None)

    def squad_of(self, node):
        for squad in self.squads:
            for member in squad.members:
                if(member == node):
                    return squad
        return None

    def __getitem__(self, name):
        node = self._nodes.get(name, None)
        if node is None:
            raise MicroToscaModelError(f"Node {name} does not exist")
        else:
            return node
        # return self._nodes.get(name, None)

    def __contains__(self, item):
        if isinstance(item, six.string_types):
            return self[item] is not None
        if isinstance(item, Root):
            return self[item.name] is not None
        return False

    def __str__(self):
        return ', '.join((i.name for i in self.nodes))
