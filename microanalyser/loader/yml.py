import ruamel.yaml
from pathlib import Path
from ..model.template import MicroModel
from ..model.nodes import Service, Database, CommunicationPattern
from ..model.groups import Squad, Edge
from .iloader import Loader
from .type import SERVICE, COMMUNICATION_PATTERN,DATABASE, API_GATEWAY, MESSAGE_BROKER,CIRCUIT_BREAKER, SQUAD, EDGE, INTERACT_WITH, RUN_TIME, DEPLOYMENT_TIME


class YMLLoader(Loader):

    def __init__(self):
        self.micro_model = None
    
    def load(self, path_to_yml)->MicroModel:
        self.micro_model = MicroModel('micro.tosca')
        yaml = ruamel.yaml.YAML() # default  type='rt' 
        micro_yml = yaml.load(Path(path_to_yml))
        self._add_nodes(micro_yml)
        self._add_relationships(micro_yml)
        self._add_groups(micro_yml)
        return self.micro_model

    def _add_nodes(self, micro_yml):
        nodes_ruamel = micro_yml.get('topology_template').get('node_templates')
        for node_name, commented_map in nodes_ruamel.items():
            node_type = self.get_type(commented_map)
            if node_type == SERVICE:
                el = Service(node_name)
            if node_type == MESSAGE_BROKER: #TODO: derived from CommunicationPattern
                el = CommunicationPattern(node_name, node_type)
            if node_type == API_GATEWAY:
                el = CommunicationPattern(node_name, node_type)
            if node_type == DATABASE:
                el = Database(node_name)
            self.micro_model.add_node(el) 
    
    def _add_relationships(self, micro_yml):
        nodes_ruamel = micro_yml.get('topology_template').get('node_templates')
        for node_name, commented_map in nodes_ruamel.items():
            source_node = self.micro_model[node_name]
            for req in self.get_requirements(commented_map):
                for interaction_type, target_name in req.items(): # [('run_time', 'order_db')]
                    target_node = self.micro_model[target_name]
                    if(interaction_type == RUN_TIME):  
                        source_node.add_run_time(target_node)
                    if(interaction_type == DEPLOYMENT_TIME):
                        source_node.add_deployment_time(target_node)
    
    def _add_groups(self, micro_yml):
        groups_ruamel = micro_yml.get('topology_template').get('groups')
        for (group_name, ordered_dict) in groups_ruamel.items():
            group_type = self.get_type(ordered_dict)
            if group_type == SQUAD:
                group = Squad(group_name)
                for member in self.get_members(ordered_dict):
                    group.add_member(self.micro_model[member])
            if group_type == EDGE:
                group = Edge(group_name)
                for member in self.get_members(ordered_dict):
                    group.add_member(self.micro_model[member])
            self.micro_model.add_group(group)

    def get_requirements(self,ruamel_commented_map):
        return ruamel_commented_map['requirements'] if 'requirements' in ruamel_commented_map else []

    def get_type(self,ruamel_commented_map):
        return ruamel_commented_map['type'] if 'type' in ruamel_commented_map else ''

    def get_members(self,ruamel_commented_map):
        return ruamel_commented_map['members'] if 'members' in ruamel_commented_map else []