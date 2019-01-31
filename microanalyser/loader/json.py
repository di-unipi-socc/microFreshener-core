
import json
from pprint import pprint
from ..model.template import MicroModel
from ..model.relationships import RunTimeInteraction, DeploymentTimeInteraction
from ..model.nodes import Service, Database, CommunicationPattern


class JSONLoader(object):

    def __init__(self):
        pass # self.micro_model = micro_tosca_template
    

    def load(self, path_to_json):
        print("loading json file ", path_to_json)
        with open(path_to_json) as f:
            data = json.load(f)
            micro_model = MicroModel(data['name'])
            for n in data['nodes']:
                if( n['type'] == 'service'):
                    print("found servie", n['name'])
                    el = Service(n['name'])
                    for runtime_links in n['run_time_links']:
                        target = runtime_links['target']
                        print("\t addind run time to" + target)
                        el.add_run_time(target)
                    for deploymentime_links in n['deployment_time_links']:
                        target = deploymentime_links['target']
                        print("\t adding deployment time to" + target)
                        el.add_deployment_time(target)
                if( n['type'] == 'communicationpattern'):
                    el = CommunicationPattern(n['name'], 'messagebroker')
                    print("found cp", n['name'])
                    for runtime_links in n['run_time_links']:
                        target = runtime_links['target']
                        print("\t addind run time to" + target)
                        el.add_run_time(target)
                    for deploymentime_links in n['deployment_time_links']:
                        target = deploymentime_links['target']
                        print("\t adding deployment time to" + target)
                        el.add_deployment_time(target)
                if( n['type'] == 'database'):
                    el = Database(n['name'])
                    print("found db", n['name'])
                micro_model.add_node(el) 
                print("Added node {}".format(el))
        micro_model.update()
        return micro_model


    
    # TODO: load() usr read from jaon file and return a MicroModel object
    def load_from_dict(self, model_as_dict):
        micro_model = MicroModel('micro.tosca')
        for n in model_as_dict['nodes']:
            if(n['type'] == 'service'):
                print("found servie", n['name'])
                el = Service(n['name'])
                for runtime_links in n['run_time_links']:
                    target = runtime_links['target']
                    print("\t addind run time to" + target)
                    el.add_run_time(target)
                for deploymentime_links in n['deployment_time_links']:
                    target = deploymentime_links['target']
                    print("\t adding deployment time to" + target)
                    el.add_deployment_time(target)
            if( n['type'] == 'communicationpattern'):
                el = CommunicationPattern(n['name'], 'messagebroker')
                print("found cp", n['name'])
                for runtime_links in n['run_time_links']:
                    target = runtime_links['target']
                    print("\t addind run time to" + target)
                    el.add_run_time(target)
                for deploymentime_links in n['deployment_time_links']:
                    target = deploymentime_links['target']
                    print("\t adding deployment time to" + target)
                    el.add_deployment_time(target)
            if( n['type'] == 'database'):
                el = Database(n['name'])
                print("found db", n['name'])
        
            micro_model.add_node(el) 
            print("Added node {}".format(el))
        return micro_model
        
