
import json
from ..model import MicroToscaModel
from ..model import Service, Database, CommunicationPattern, MessageBroker, MessageRouter
from ..model.groups import Edge, Team
from ..logging import MyLogger
from .iimporter import Importer
from ..model.type import  MICROTOSCA_NODES_MESSAGE_BROKER, MICROTOSCA_NODES_MESSAGE_ROUTER, MICROTOSCA_GROUPS_TEAM, MICROTOSCA_GROUPS_EDGE, MICROTOSCA_RELATIONSHIPS_INTERACT_WITH
from ..model.type  import MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_TIMEOUT_PROPERTY, MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_DYNAMIC_DISCOVEY_PROPERTY, MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_CIRCUIT_BREAKER_PROPERTY
from .jsontype import JSON_RUN_TIME, JSON_DEPLOYMENT_TIME, JSON_NODE_SERVICE, JSON_NODE_DATABASE, JSON_NODE_MESSAGE_BROKER, JSON_NODE_MESSAGE_ROUTER
from .jsontype import  JSON_GROUPS_EDGE, JSON_GROUPS_TEAM

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
        for node in json_data['nodes']:
            type_node = node['type']
            name_node = node['name']
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
            self.micro_model.add_node(el)
            logger.debug(f"Added node {el.name}")

    def _load_links(self, json_data):
        if("links") in json_data:
            for link in json_data['links']:
                logger.debug(f"link: {link}")
                ltype = link['type']
                source = self.micro_model[link['source']]
                target = self.micro_model[link['target']]
                (is_timeout, is_circuit_breaker,
                is_dynamic_discovery) = self._get_links_properties(link)
                if(ltype == JSON_RUN_TIME):
                    source.add_run_time(target, is_timeout,
                                        is_circuit_breaker, is_dynamic_discovery)
                elif (ltype == JSON_DEPLOYMENT_TIME):
                    source.add_deployment_time(
                        target, is_timeout, is_circuit_breaker, is_dynamic_discovery)
                else:
                    raise ImporterError(
                        "Link type {} is not recognized".format(ltype))
                logger.debug(f"Added link from {source} to {target}")

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
