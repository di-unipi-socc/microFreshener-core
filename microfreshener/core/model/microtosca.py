'''
MicroModelModel module
'''
import re

import six
from .nodes import Root, Service, Datastore, CommunicationPattern, MessageRouter, MessageBroker, Compute
from .groups import Team, Edge
from ..errors import MicroToscaModelError, MultipleEdgeGroupsError
from ..logging import MyLogger
from ..errors import RelationshipNotFoundError, GroupNotFoundError
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
    def computes(self):
        return (v for k, v in self._nodes.items() if isinstance(v, Compute))

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
    def teams(self):
        return (v for k, v in self._groups.items() if isinstance(v, Team))

    # deprecated
    @property
    def edges(self):
        return (v for k, v in self._groups.items() if isinstance(v, Edge))

    @property
    def edge(self):
        for k, v in self._groups.items():
            if isinstance(v, Edge):
                return v
        raise GroupNotFoundError("Edge group is missing")

    def add_node(self, node):
        self._nodes[node.name] = node
        logger.debug("Added node {}".format(node))
        return node
    
    def rename_node(self, node, new_name):
        old_name = node.name
        self._nodes[new_name] = self._nodes.pop(node.name)

        logger.debug(f"Renamed node {node.name} to {new_name}")
        node.name = new_name

        for name, group in self._groups.items():
            for name in list(group._members.keys()):
                if name == old_name:
                    del group._members[name]
                    group.add_member(node)


    def relink_incoming(self, current_node, target_node, source_nodes_to_be_discarded=[]):
        
        incoming_interactions = list(current_node.incoming_interactions)
        for incoming in incoming_interactions:
            if incoming.source not in source_nodes_to_be_discarded:
                incoming.source.remove_interaction(incoming)
                incoming.source.add_interaction(
                    target_node,
                    incoming.timeout,
                    incoming.circuit_breaker,
                    incoming.dynamic_discovery)
        # return target_node.add_interaction(current_node)

    def delete_node(self, node):
        for rel in node.interactions:
            rel.target.remove_incoming_interaction(rel)
        for up_rel in node.incoming_interactions:
            up_rel.source.remove_interaction(up_rel)

        if isinstance(node, Service):
            for dep in node.deployed_on:
                node.remove_deployed_on(dep)

        logger.debug(f"Deleted node {node}")
        del self._nodes[node.name]

    def add_interaction(self, source_node, target_node,
                        with_timeout=False,
                        with_circuit_breaker=False,
                        with_dynamic_discovery=False):
        return source_node.add_interaction(target_node,
                                           with_timeout,
                                           with_circuit_breaker,
                                           with_dynamic_discovery)

    def add_deployed_on(self, source_node, target_node):
        return source_node.add_deployed_on(item=target_node)

    def get_relationship(self, id):
        for node in self.nodes:
            for interaction in node.interactions:
                if(interaction.id == id):
                    return interaction
        raise RelationshipNotFoundError(f"Relationship with id {id} not found")

    def delete_relationship(self, interaction):
        interaction.source.remove_interaction(interaction)
        logger.debug(f"Removed {interaction} interaction")

    def add_group(self, group):
        if isinstance(group, Edge) and len(list(self.edges)) > 1:
            raise MultipleEdgeGroupsError("Cannot be more than one Edge group")
        self._groups[group.name] = group
        logger.debug("Added group {}".format(group))
        return self._groups[group.name]

    def get_group(self, name):
        if name not in self._groups.keys():
            raise GroupNotFoundError(f"Group {name} does not exists")
        return self._groups.get(name)

    # return the squad of a node
    def squad_of(self, node):
        for team in self.teams:
            for member in team.members:
                if(member == node):
                    return team
        return None

    # return the edge of a node
    def get_edge_of_node(self, node):
        for edge in self.edges:
            for member in edge.members:
                if(member == node):
                    return edge
        return None

    def get_subgraph(self, nodes):
        subMicroToscaModel = MicroToscaModel(self.name)
        for node in self.nodes:
            if node in nodes:
                newnode = subMicroToscaModel.add_node(node)
                for interaction in node.interactions:
                    if(interaction.target not in nodes):
                        newnode.remove_interaction(interaction)
                # add the group of the node in the subgraph
                team_of_node = self.squad_of(node)
                if team_of_node:
                    if team_of_node not in subMicroToscaModel.teams:
                        subMicroToscaModel.add_group(team_of_node)
                    else:
                        subMicroToscaModel.get_group(
                            team_of_node.name).add_member(node)

        return subMicroToscaModel

    def get_node_by_name(self, name: str, type = None):
        nodes_to_consider = [n for n in self.nodes if isinstance(n, type)] if type else self.nodes

        # Case: node.name == name
        for node in nodes_to_consider:
            if node.name == name:
                return node

        for node in nodes_to_consider:
            # Case: name is FQDN (name.ns.svc, name.ns.svc.cluster, name.ns.svc.cluster.local)
            match = re.match(name+r"([.][a-zA-Z]*){1,3}", node.name)
            if match and match.string == node.name:
                return node

            # Case: node.name is FQDN (name.ns.svc, name.ns.svc.cluster, name.ns.svc.cluster.local)
            match = re.match(node.name + r"([.][a-zA-Z]*){1,3}", name)
            if match and match.string == name:
                return node

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
