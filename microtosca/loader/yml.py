import ruamel.yaml
from pathlib import Path
from ..graph.template import MicroToscaTemplate
from ..graph.nodes import Service, Database, CommunicationPattern
from ..graph.groups import Squad
from ..graph.helper import get_type


from ..type import SERVICE, COMMUNICATION_PATTERN,DATABASE,MESSAGE_BROKER,CIRCUIT_BREAKER, SQUAD


class YmlLoader(object):

    def __init__(self):
        pass # self.microtosca_template = micro_tosca_template
    
    def parse(self, path_to_yml):
        yaml = ruamel.yaml.YAML() # default  type='rt' 
    
        microtosca_template = MicroToscaTemplate('micro.tosca')
        micro_yml = yaml.load(Path(path_to_yml))
        nodes_ruamel = micro_yml.get('topology_template').get('node_templates')

        for node_name, commented_map in nodes_ruamel.items():
            node_type = get_type(commented_map)
            if node_type == SERVICE:
                el = Service.from_yaml(node_name,commented_map)
            if node_type == MESSAGE_BROKER: #TODO: derived from CommunicationPattern
                el = CommunicationPattern.from_yaml(node_name,node_type,commented_map)
            if node_type == DATABASE:
                el = Database.from_yaml(node_name,commented_map)
            microtosca_template.push(el)
            
        groups_ruamel = micro_yml.get('topology_template').get('groups')

        for (group_name, ordered_dict) in groups_ruamel.items():
            group_type = get_type(ordered_dict)
            if group_type == SQUAD:
                squad = Squad.from_yaml(group_name, ordered_dict)
            microtosca_template.add_group(squad)
        return microtosca_template
