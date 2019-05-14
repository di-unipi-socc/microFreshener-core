
import json
from ..model.template import MicroModel
from ..model.nodes import Service, Database, CommunicationPattern, MessageBroker, MessageRouter
from ..model.groups import Edge, Squad
from ..logging import MyLogger
from .iloader import Loader
from ..model.type import API_GATEWAY, MESSAGE_BROKER, MESSAGE_ROUTER, CIRCUIT_BREAKER, SQUAD, EDGE, INTERACT_WITH, RUN_TIME, DEPLOYMENT_TIME
from ..model.type  import INTERACT_WITH_TIMEOUT_PROPERTY, INTERACT_WITH_DYNAMIC_DISCOVEY_PROPERTY, INTERACT_WITH_CIRCUIT_BREAKER_PROPERTY

from ..errors import ImporterError
logger = MyLogger().get_logger()


class JSONLoader(Loader):

    def load(self, path_to_json)->MicroModel:
        logger.info("Loading JSON file: {}".format(path_to_json))
        with open(path_to_json) as f:
            data = json.load(f)
            self.micro_model = MicroModel(data['name'])
            self._load_nodes(data)
            self._load_links(data)
            self._load_groups(data)
            return self.micro_model

    def _load_nodes(self, json_data):
        for node in json_data['nodes']:
            type_node = node['type']
            name_node = node['name']
            if(type_node == 'service'):
                # logger.debug("Created service {}".format(name_node))
                el = Service(name_node)
            elif(type_node == 'messagebroker'):
                el = MessageBroker(name_node)
            elif(type_node == "messagerouter"):
                el = MessageRouter(name_node)
            elif(type_node == 'database'):
                # logger.debug("Created Database {}".format(name_node))
                el = Database(name_node)
            else:
                raise ImporterError(
                    "{} Node type is not recognized".format(type_node))
            self.micro_model.add_node(el)
            logger.info(f"Added node {el.name}")


    def _load_links(self, json_data):
        if("links") in json_data:
            for link in json_data['links']:
                logger.info(f"link: {link}")
                ltype = link['type']
                source = self.micro_model[link['source']]
                target = self.micro_model[link['target']]
                
                (is_timeout, is_circuit_breaker,
                is_dynamic_discovery) = self._get_links_properties(link)
                if(ltype == 'runtime'):
                    source.add_run_time(target, is_timeout,
                                        is_circuit_breaker, is_dynamic_discovery)
                elif (ltype == 'deploymenttime'):
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
        if INTERACT_WITH_TIMEOUT_PROPERTY in link_json:
            is_timeout = link_json[INTERACT_WITH_TIMEOUT_PROPERTY]
        if INTERACT_WITH_CIRCUIT_BREAKER_PROPERTY in link_json:
            is_circuit_breaker = link_json[INTERACT_WITH_CIRCUIT_BREAKER_PROPERTY]
        if INTERACT_WITH_DYNAMIC_DISCOVEY_PROPERTY in link_json:
            is_dynamic_discovery = link_json[INTERACT_WITH_DYNAMIC_DISCOVEY_PROPERTY]
        return (is_timeout, is_circuit_breaker, is_dynamic_discovery)

    def _load_groups(self, json_data):
        if('groups' in json_data):
            for group in json_data['groups']:
                group_type = group['type']
                group_name = group['name']
                if(group_type == 'edgegroup'):
                    edge = Edge(group_name)
                    for member_name in group['members']:
                        member = self.micro_model.get_node_by_name(member_name)
                        edge.add_member(member)
                        logger.debug("Added {} to group:{}  name:{}".format(
                            member_name, group_type, group_name))
                    self.micro_model.add_group(edge)
                elif (group_type == 'squadgroup'):
                    logger.debug("Adding Squad group".format(group_name))
                    squad = Squad(group_name)
                    for member_name in group['members']:
                        member = self.micro_model.get_node_by_name(member_name)
                        squad.add_member(member)
                        logger.debug("Added {} to group:{}  name:{}".format(
                            member_name, group_type, group_name))
                    self.micro_model.add_group(squad)
                else:
                    raise ImporterError(
                        "Group {} is not a valid type".format(group_type))
