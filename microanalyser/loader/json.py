
import json
from ..model.template import MicroModel
from ..model.nodes import Service, Database, CommunicationPattern
from ..model.groups import Edge
from ..logging import MyLogger
from .iloader import Loader

logger = MyLogger().get_logger()


class JSONLoader(Loader):

    def load(self, path_to_json)->MicroModel:
        logger.info("Loading JSON file: {}".format(path_to_json))
        with open(path_to_json) as f:
            data = json.load(f)
            micro_model = MicroModel(data['name'])
            for node in data['nodes']:
                tnode = node['type']
                tname = node['name']
                if(tnode == 'service'):
                    # logger.debug("Created service {}".format(tname))
                    el = Service(tname)
                elif(tnode == 'communicationpattern'):
                    # logger.debug("Created Communication Pattern {}".format(tname))
                    el = CommunicationPattern(tname, 'messagebroker')
                elif(tnode == 'database'):
                    # logger.debug("Created Database {}".format(tname))
                    el = Database(tname)
                else:
                    raise Exception("NOde type is not recognized")
                micro_model.add_node(el)
                # logger.debug("Loaded node {}".format(tname))
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
