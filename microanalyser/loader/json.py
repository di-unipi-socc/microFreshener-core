
import json
from ..model.template import MicroModel
from ..model.nodes import Service, Database, CommunicationPattern
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
                tid = node['id']
                tname = node['name']
                if(tnode == 'service'):
                    # logger.debug("Created service {}".format(tname))
                    el = Service(tname, tid)
                elif(tnode == 'communicationpattern'):
                    # logger.debug("Created Communication Pattern {}".format(tname))
                    el = CommunicationPattern(tname, 'messagebroker',tid)
                elif(tnode == 'database'):
                    # logger.debug("Created Database {}".format(tname))
                    el = Database(tname, tid)
                else:
                    raise Exception("NOde type is not recognized")
                micro_model.add_node(el)
                # logger.debug("Loaded node {}".format(tname))
            for link in data['links']:
                ltype =  link['type']
                source = micro_model[link['source']]
                target = micro_model[link['target']]
                if(ltype == 'runtime'):
                    source.add_run_time(target)
                    # logger.debug("Added runtime link {} -> {}".format(source, target))
                elif (ltype == 'deploymenttime'):
                    # logger.debug("Added runtime link {} -> {}".format(source, target))
                    source.add_deployment_time(target)
                else:
                    raise Exception("Link type {} is not recognized".format(ltype))
            return micro_model