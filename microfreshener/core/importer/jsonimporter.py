
import json
from ..model import MicroToscaModel
from ..model import Service, Datastore, CommunicationPattern, MessageBroker, MessageRouter

from ..model import KProxy, KService, KIngress
from ..model.groups import Edge, Team
from ..model.relationships import InteractsWith, DeploymentTimeInteraction, RunTimeInteraction

from ..logging import MyLogger
from .iimporter import Importer
from ..model.type import MICROTOSCA_NODES_MESSAGE_BROKER, MICROTOSCA_NODES_MESSAGE_ROUTER, MICROTOSCA_GROUPS_TEAM, MICROTOSCA_GROUPS_EDGE, MICROTOSCA_RELATIONSHIPS_INTERACT_WITH

from ..model.type import MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_TIMEOUT_PROPERTY, MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_DYNAMIC_DISCOVEY_PROPERTY, MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_CIRCUIT_BREAKER_PROPERTY
from .jsontype import JSON_RELATIONSHIP_INTERACT_WITH, JSON_RUN_TIME, JSON_DEPLOYMENT_TIME, JSON_NODE_SERVICE, JSON_NODE_DATABASE, JSON_NODE_MESSAGE_BROKER, JSON_NODE_MESSAGE_ROUTER
from .jsontype import JSON_NODE_MESSAGE_ROUTER_KINGRESS, JSON_NODE_MESSAGE_ROUTER_KPROXY, JSON_NODE_MESSAGE_ROUTER_KSERVICE
from .jsontype import JSON_GROUPS_EDGE, JSON_GROUPS_TEAM
import os

from ..errors import ImporterError
logger = MyLogger().get_logger()

class JSONImporter(Importer):

    def Import(self, path_to_json)->MicroToscaModel:
        logger.info("Loading JSON file: {}".format(path_to_json))
        if os.path.exists(path_to_json):
            with open(path_to_json) as f:
                data = json.load(f)
        else:
            data = json.loads(path_to_json)
        self._load_microtosca(data)
        self._load_nodes(data)
        self._load_links(data)
        self._load_groups(data)
        return self.micro_model
       
    def load_json(self, path_to_json):
        with open(path_to_json) as f:
            data = json.load(f)
            return data
    
    def _load_microtosca(self, data_json):
        self.micro_model = MicroToscaModel(data_json['name'])

    def _load_nodes(self, json_data):
        if "nodes" in json_data:
            for jnode in json_data['nodes']:
                node = self.load_node_from_json(jnode)
                self.micro_model.add_node(node)
                logger.debug(f"Added node {node.name}")

    def load_node_from_json(self, json_node):
        if "type" not in json_node:
            raise ImporterError(f"Attribute 'type' in missing in {json_node}")
        type_node = json_node['type']
        if "name" not in json_node:
            raise ImporterError(f"Attribute 'name' in missing in {json_node}")
        name_node = json_node['name']
        if(type_node == JSON_NODE_SERVICE):
            # logger.debug("Created service {}".format(name_node))
            el = Service(name_node)
        elif(type_node == JSON_NODE_MESSAGE_BROKER):
            el = MessageBroker(name_node)
        elif(type_node == JSON_NODE_MESSAGE_ROUTER):
            el = MessageRouter(name_node)
        elif(type_node == JSON_NODE_DATABASE):
            el = Datastore(name_node)
        elif(type_node == JSON_NODE_MESSAGE_ROUTER_KSERVICE):
            el = KService(name_node)
        elif(type_node == JSON_NODE_MESSAGE_ROUTER_KPROXY):
            el = KProxy(name_node)
        elif(type_node == JSON_NODE_MESSAGE_ROUTER_KINGRESS):
            el = KIngress(name_node)
        else:
            raise ImporterError(
                "Node type {}  not recognized".format(type_node))
        return el

    def _load_links(self, json_data):
        if "links" in json_data:
            for link in json_data['links']:
                self.import_link_from_json(link)

    def import_link_from_json(self, link_json):
        type_rel = self.load_type_relationship_from_json(link_json)
        if(type_rel == JSON_RELATIONSHIP_INTERACT_WITH):
            interaction = self.load_interaction_from_json(link_json)
            source = self.load_source_node_from_json(link_json)
            return source.add_interaction(interaction)
        else:
            raise ImporterError(f"Link type {type_rel} not recognized")

    def load_interaction_from_json(self, link_json):
        source_node = self.load_source_node_from_json(link_json)
        target_node = self.load_target_node_from_json(link_json)
        (with_timeout, with_circuit_breaker,
         with_dynamic_discovery) = self.get_properties_of_interaction_from_json(link_json)
        return InteractsWith(source_node, target_node, with_timeout, with_circuit_breaker,
                             with_dynamic_discovery)
    
    # def load_node_id_from_json(self, link_json):
    #     if "id" not in link_json:
    #         raise ImporterError(
    #             f"Attribute 'id' in missing in {link_json}")
    #     return link_json['id']

    def load_source_node_from_json(self, link_json):
        if "source" not in link_json:
            raise ImporterError(
                f"Attribute 'source' in missing in {link_json}")
        source_node = self.micro_model[link_json['source']]
        return source_node

    def load_target_node_from_json(self, link_json):
        if "target" not in link_json:
            raise ImporterError(
                f"Attribute 'target' in missing in {link_json}")
        target_node = self.micro_model[link_json['target']]
        return target_node

    def load_type_relationship_from_json(self, link_json):
        if "type" not in link_json:
            raise ImporterError(f"Attribute 'type' in missing in {link_json}")
        type_requirement = link_json['type']
        return type_requirement

    # def load_type_source_target_from_json(self, link_json):
    #     if "type" not in link_json:
    #         raise ImporterError(f"Attribute 'type' in missing in {link_json}")
    #     type_requirement = link_json['type']
    #     if "source" not in link_json:
    #         raise ImporterError(
    #             f"Attribute 'source' in missing in {link_json}")
    #     source_node = self.micro_model[link_json['source']]
    #     if "target" not in link_json:
    #         raise ImporterError(
    #             f"Attribute 'target' in missing in {link_json}")
    #     target_node = self.micro_model[link_json['target']]
    #     return (type_requirement, source_node, target_node)

    def get_properties_of_interaction_from_json(self, link_json):
        is_timeout = False
        is_circuit_breaker = False
        is_dynamic_discovery = False
        if MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_TIMEOUT_PROPERTY in link_json:
            is_timeout = link_json[MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_TIMEOUT_PROPERTY]
        if MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_CIRCUIT_BREAKER_PROPERTY in link_json:
            is_circuit_breaker = link_json[MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_CIRCUIT_BREAKER_PROPERTY]
        if MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_DYNAMIC_DISCOVEY_PROPERTY in link_json:
            is_dynamic_discovery = link_json[MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_DYNAMIC_DISCOVEY_PROPERTY]
        return (is_timeout, is_circuit_breaker, is_dynamic_discovery)

    def _load_groups(self, json_data):
        if('groups' in json_data):
            for group in json_data['groups']:
                group_type = group['type']
                group_name = group['name']
                if(group_type == JSON_GROUPS_EDGE):
                    edge = Edge(group_name)
                    for member_name in group['members']:
                        member = self.micro_model[member_name]
                        edge.add_member(member)
                        logger.debug("Added {} to group:{}  name:{}".format(
                            member_name, group_type, group_name))
                    self.micro_model.add_group(edge)
                elif (group_type == JSON_GROUPS_TEAM):
                    logger.debug("Adding Team group".format(group_name))
                    squad = Team(group_name)
                    for member_name in group['members']:
                        member = self.micro_model[member_name]
                        squad.add_member(member)
                        logger.debug("Added {} to group:{}  name:{}".format(
                            member_name, group_type, group_name))
                    self.micro_model.add_group(squad)
                else:
                    raise ImporterError(
                        "Group {} is not a valid type".format(group_type))
