'''
MicroModelModel module
'''
import six
from .nodes import Root, Service, Database, CommunicationPattern
from .relationships import DeploymentTimeInteraction, RunTimeInteraction
from .groups import Team, Edge
from ..errors import MicroToscaError
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
    def databases(self):
        return (v for k, v in self._nodes.items() if isinstance(v, Database))

    @property
    def communicationPatterns(self):
        return (v for k, v in self._nodes.items() if isinstance(v, CommunicationPattern))

    @property
    def groups(self):
        return (v for k, v in self._groups.items())

    @property
    def squads(self):
        return (v for k, v in self._groups.items() if isinstance(v, Team))
    
    @property
    def edges(self):
        return (v for k, v in self._groups.items() if isinstance(v, Edge))

    def get_squad(self, name):
        return self._groups.get(name, None)
    
    def get_group(self, name):
        return self._groups.get(name, None)

    def squad_of(self, node):
        for squad in self.squads:
            for member in squad.members:
                if(member == node):
                    return squad
        return None

    def add_node(self, node):
        self._nodes[node.name] = node
        logger.debug("Added node {}".format(node))

    def delete_node(self, node):
        for rel in node.relationships:
            rel.target.remove_incoming_relationship(
                rel)  # remove the up relationship
        logger.debug("{}: deleted node".format(self._nodes[node.name]))
        del self._nodes[node.name]

    def add_group(self, group):
        self._groups[group.name] = group
        logger.debug("Added group {}".format(group))
  
    def get_node_by_name(self, name):
        for node in self.nodes:
            if node.name == name:
                return node
        return None
  
    def findByName(self, n):
        for key, node in self._nodes.items(): 
            if (node.name == n):
                return node
        return None

    def __getitem__(self, name):
        return self._nodes.get(name, None)

    def __contains__(self, item):
        if isinstance(item, six.string_types):
            return self[item] is not None
        if isinstance(item, Root):
            return self[item.name] is not None
        return False

    def __str__(self):
        return ', '.join((i.name for i in self.nodes))

