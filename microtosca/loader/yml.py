import ruamel.yaml
from pathlib import Path
from graph.template import MicroToscaTemplate
from graph.nodes import Service, Database, CommunicationPattern

# CUSTOM NODE TYPEs
SERVICE = 'micro.nodes.Service'
COMMUNICATION_PATTERN = 'micro.nodes.CommunicationPattern'
DATABASE = 'micro.nodes.Database'

MESSAGE_BROKER = 'micro.nodes.MessageBroker'
CIRCUIT_BREAKER = 'micro.nodes.CircuitBreaker'

class YmlLoader(object):

    def __init__(self):
        pass # self.microtosca_template = micro_tosca_template
    
    def parse(self, path_to_yml):
        yaml = ruamel.yaml.YAML()#typ='safe') #typ='rt') 
    
        microtosca_template = MicroToscaTemplate('micro.tosca')
        micro_yml = yaml.load(Path(path_to_yml))
        nodes_ruamel = micro_yml.get('topology_template').get('node_templates')

        for node_name, commented_map in nodes_ruamel.items():
            node_type = self.get_node_type(commented_map)
            if node_type == SERVICE:
                el = Service.from_yaml(node_name,commented_map)
            if node_type == MESSAGE_BROKER: # TODO: derived from CommunicationPattern
                el = CommunicationPattern.from_yaml(node_name,node_type,commented_map)
            if node_type == DATABASE:
                el = Database.from_yaml(node_name,commented_map)
            el.name = node_name
            microtosca_template.push(el)
        return microtosca_template

    def get_node_type(self, ruamel_commented_map):
        return ruamel_commented_map['type'] 

    def get_requirements(self,ruamel_commented_map):
        return ruamel_commented_map['requirements'] 