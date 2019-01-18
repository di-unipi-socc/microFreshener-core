import ruamel.yaml
from pathlib import Path
from ..model.template import MicroModel
from ..model.nodes import Service, Database, CommunicationPattern
from ..model.groups import Squad

from .type import SERVICE, COMMUNICATION_PATTERN,DATABASE,MESSAGE_BROKER,CIRCUIT_BREAKER, SQUAD, INTERACT_WITH, RUN_TIME, DEPLOYMENT_TIME


class MicroToscaLoader(object):

    def __init__(self):
        pass # self.micro_model = micro_tosca_template
    
    def load(self, path_to_yml):
        yaml = ruamel.yaml.YAML() # default  type='rt' 
    
        micro_model = MicroModel('micro.tosca')

        micro_yml = yaml.load(Path(path_to_yml))
        nodes_ruamel = micro_yml.get('topology_template').get('node_templates')

        for node_name, commented_map in nodes_ruamel.items():
            node_type = self.get_type(commented_map)
            if node_type == SERVICE:
                el = Service(node_name)
                for req in self.get_requirements(commented_map):
                    for name, value in req.items(): # [('run_time', 'order_db')]
                        if(name == RUN_TIME):  
                            el.add_run_time(value)
                        if(name == DEPLOYMENT_TIME):
                            el.add_deployment_time(value)
                # el = self.from_yaml(node_name, commented_map)
            if node_type == MESSAGE_BROKER: #TODO: derived from CommunicationPattern
                # el = CommunicationPattern.from_yaml(node_name, node_type, commented_map)
                el = CommunicationPattern(node_name, node_type)
                for req in  self.get_requirements(commented_map):
                    for name, value in req.items(): # [('run_time', 'order_db')]
                        if(name == RUN_TIME):  
                            el.add_run_time(value)
                        if(name == DEPLOYMENT_TIME):
                            el.add_deployment_time(value)
            if node_type == DATABASE:
                el = Database(node_name)
            micro_model.add_node(el) 
            
        groups_ruamel = micro_yml.get('topology_template').get('groups')

        for (group_name, ordered_dict) in groups_ruamel.items():
            group_type = self.get_type(ordered_dict)
            if group_type == SQUAD:
                squad = Squad(group_name)
                for member in self.get_members(ordered_dict):
                    squad.add_node(member)
                    # squad.add_node(micro_model[member])

            micro_model.add_group(squad)
        return micro_model

    def get_requirements(self,ruamel_commented_map):
        return ruamel_commented_map['requirements'] if 'requirements' in ruamel_commented_map else []

    def get_type(self,ruamel_commented_map):
        return ruamel_commented_map['type'] if 'type' in ruamel_commented_map else ''

    def get_members(self,ruamel_commented_map):
        return ruamel_commented_map['members'] if 'members' in ruamel_commented_map else []