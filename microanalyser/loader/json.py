
import json
from ..model.template import MicroModel
from ..model.nodes import Service, Database, CommunicationPattern
from ..model.groups import Edge
from ..logging import MyLogger
from .iloader import Loader
from .type import API_GATEWAY, MESSAGE_BROKER, CIRCUIT_BREAKER, SQUAD, EDGE, INTERACT_WITH, RUN_TIME, DEPLOYMENT_TIME

logger = MyLogger().get_logger()


class JSONLoader(Loader):

    def load(self, path_to_json)->MicroModel:
        logger.info("Loading JSON file: {}".format(path_to_json))
        with open(path_to_json) as f:
            data = json.load(f)
            micro_model = MicroModel(data['name'])
            for node in data['nodes']:
                type_node = node['type']
                name_node = node['name']
                if(type_node == 'service'):
                    # logger.debug("Created service {}".format(name_node))
                    el = Service(name_node)
                elif(type_node == 'communicationpattern'):
                    # logger.debug("Created Communication Pattern {}".format(name_node))
                    concrete_type_node = node['ctype']
                    if( concrete_type_node == "MessageBroker"):
                        el = CommunicationPattern(name_node, MESSAGE_BROKER)
                    elif (concrete_type_node == "ApiGateway"):
                        el = CommunicationPattern(name_node, API_GATEWAY)
                    elif concrete_type_node == "CircuitBreaker":
                        el = CommunicationPattern(name_node, CIRCUIT_BREAKER)
                    else:
                        raise Exception("concrete type {} is not recognized".format(concrete_type_node))

                elif(type_node == 'database'):
                    # logger.debug("Created Database {}".format(name_node))
                    el = Database(name_node)
                else:
                    raise Exception("{} Node type is not recognized".format(type_node))
                micro_model.add_node(el)
                # logger.debug("Loaded node {}".format(name_node))
            for link in data['links']:
                ltype = link['type']
                source = micro_model[link['source']]
                target = micro_model[link['target']]
                if(ltype == 'runtime'):
                    source.add_run_time(target)
                    # logger.debug("Added runtime link {} -> {}".format(source, target))
                elif (ltype == 'deploymenttime'):
                    # logger.debug("Added runtime link {} -> {}".format(source, target))
                    source.add_deployment_time(target)
                else:
                    raise Exception(
                        "Link type {} is not recognized".format(ltype))
            # Add groups into the model
            if('groups' in data):
                for group in data['groups']:
                    group_type = group['type']
                    group_name = group['name']
                    if(group_type == 'edgegroup'):
                        edge = Edge(group_name)
                        for member_name in group['members']:
                            member = micro_model.get_node_by_name(member_name)
                            edge.add_member(member)
                            logger.info("Added {} to group:{}  name:{}".format(
                                member_name, group_type, group_name))
                        micro_model.add_group(edge)
                    elif (group_type == 'squadgroup'):
                        logger.debug("Adding Squad group".format(group_name))
                    else:
                        raise Exception(
                            "Group type {} is not recognized".format(group_type))

            return micro_model
