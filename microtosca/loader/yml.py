import ruamel.yaml
from pathlib import Path
from ..model import MicroToscaModel
from ..model import Service, Database, CommunicationPattern
from ..model.groups import Team
from ..model.helper import get_type


from ..model.type import SERVICE, COMMUNICATION_PATTERN,DATABASE,MESSAGE_BROKER,CIRCUIT_BREAKER, TEAM

class YMLImporter(object):

    def __init__(self):
        pass # self.microtosca_template = micro_tosca_template
    
    def Import(self, path_to_yml):
        yaml = ruamel.yaml.YAML() # default  type='rt' 
    
        microtosca_template = MicroToscaModel('micro.tosca')
        micro_yml = yaml.Import(Path(path_to_yml))
        nodes_ruamel = micro_yml.get('topology_template').get('node_templates')

        for node_name, commented_map in nodes_ruamel.items():
            node_type = get_type(commented_map)
            if node_type == SERVICE:
                el = Service.from_yaml(node_name,commented_map)
            if node_type == MESSAGE_BROKER: #TODO: derived from CommunicationPattern
                el = CommunicationPattern.from_yaml(node_name,node_type,commented_map)
            if node_type == DATABASE:
                el = Database.from_yaml(node_name,commented_map)
            microtosca_template.add_node(el)
            
        groups_ruamel = micro_yml.get('topology_template').get('groups')

        for (group_name, ordered_dict) in groups_ruamel.items():
            group_type = get_type(ordered_dict)
            if group_type == TEAM:
                squad = Team.from_yaml(group_name, ordered_dict)
            microtosca_template.add_group(squad)
        return microtosca_template
