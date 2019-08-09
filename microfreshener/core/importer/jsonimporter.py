
import json
from ..model import MicroToscaModel
from ..model import Service, Database, CommunicationPattern, MessageBroker, MessageRouter
from ..model.groups import Edge, Team
from ..model.relationships import InteractsWith, DeploymentTimeInteraction, RunTimeInteraction

from ..logging import MyLogger
from .iimporter import Importer
from ..model.type import MICROTOSCA_NODES_MESSAGE_BROKER, MICROTOSCA_NODES_MESSAGE_ROUTER, MICROTOSCA_GROUPS_TEAM, MICROTOSCA_GROUPS_EDGE, MICROTOSCA_RELATIONSHIPS_INTERACT_WITH
from ..model.type import MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_TIMEOUT_PROPERTY, MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_DYNAMIC_DISCOVEY_PROPERTY, MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_CIRCUIT_BREAKER_PROPERTY
from .jsontype import JSON_RELATIONSHIP_INTERACT_WITH, JSON_RUN_TIME, JSON_DEPLOYMENT_TIME, JSON_NODE_SERVICE, JSON_NODE_DATABASE, JSON_NODE_MESSAGE_BROKER, JSON_NODE_MESSAGE_ROUTER
from .jsontype import JSON_GROUPS_EDGE, JSON_GROUPS_TEAM

from ..errors import ImporterError
logger = MyLogger().get_logger()


class JSONImporter(Importer):

    def Import(self, path_to_json)->MicroToscaModel:
        logger.info("Loading JSON file: {}".format(path_to_json))
        with open(path_to_json) as f:
            data = json.load(f)
            self.micro_model = MicroToscaModel(data['name'])
            self._load_nodes(data)
            self._load_links(data)
            self._load_groups(data)
            return self.micro_model

    def _load_nodes(self, json_data):
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
            el = Database(name_node)
        else:
            raise ImporterError(
                "{} Node type is not recognized".format(type_node))
        return el

    def _load_links(self, json_data):
        if("links") in json_data:
            for link in json_data['links']:
                (relation, source, target) = self.load_type_source_target_from_json(link)
                if(relation == JSON_RELATIONSHIP_INTERACT_WITH):
                    (with_timeout, with_circuit_breaker, with_dynamic_discovery) = self._get_links_properties(link)
                    source.add_interaction(target, with_timeout, with_circuit_breaker, with_dynamic_discovery)
                else:
                    raise ImporterError(f"Link type {relation} not recognized")
                # ltype = link['type']
                # source = self.micro_model[link['source']]
                # target = self.micro_model[link['target']]
                # (is_timeout, is_circuit_breaker,
                #  is_dynamic_discovery) = self._get_links_properties(link)
                # if(ltype == JSON_RUN_TIME):
                #     source.add_run_time(target, is_timeout,
                #                         is_circuit_breaker, is_dynamic_discovery)
                # elif (ltype == JSON_DEPLOYMENT_TIME):
                #     source.add_deployment_time(
                #         target, is_timeout, is_circuit_breaker, is_dynamic_discovery)
                # else:
                #     raise ImporterError(
                #         "Link type {} is not recognized".format(ltype))
                # logger.debug(f"Added link from {source} to {target}")

    def load_type_source_target_from_json(self, link_json):
        if "type" not in link_json:
            raise ImporterError(f"Attribute 'type' in missing in {link_json}")
        type_requirement = link_json['type']
        if "source" not in link_json:
            raise ImporterError(
                f"Attribute 'source' in missing in {link_json}")
        source_node = self.micro_model[link_json['source']]
        if "target" not in link_json:
            raise ImporterError(
                f"Attribute 'target' in missing in {link_json}")
        target_node = self.micro_model[link_json['target']]
        return (type_requirement, source_node, target_node)

    def _get_links_properties(self, link_json):
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
                        member = self.micro_model.get_node_by_name(member_name)
                        edge.add_member(member)
                        logger.debug("Added {} to group:{}  name:{}".format(
                            member_name, group_type, group_name))
                    self.micro_model.add_group(edge)
                elif (group_type == JSON_GROUPS_TEAM):
                    logger.debug("Adding Team group".format(group_name))
                    squad = Team(group_name)
                    for member_name in group['members']:
                        member = self.micro_model.get_node_by_name(member_name)
                        squad.add_member(member)
                        logger.debug("Added {} to group:{}  name:{}".format(
                            member_name, group_type, group_name))
                    self.micro_model.add_group(squad)
                else:
                    raise ImporterError(
                        "Group {} is not a valid type".format(group_type))
