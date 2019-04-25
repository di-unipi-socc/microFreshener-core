import ruamel.yaml
from pathlib import Path
from ..model.template import MicroModel
from ..model.nodes import Service, Database, CommunicationPattern
from ..model.groups import Squad, Edge
from .iloader import Loader
from .type import SERVICE, COMMUNICATION_PATTERN,DATABASE, API_GATEWAY, MESSAGE_BROKER,CIRCUIT_BREAKER, SQUAD, EDGE, INTERACT_WITH, RUN_TIME, DEPLOYMENT_TIME

from ..logging import MyLogger

logger = MyLogger().get_logger()
class YMLLoader(Loader):

    def __init__(self):
        self.micro_model = None
    
    def load(self, path_to_yml)->MicroModel:
        self.micro_model = MicroModel('micro.tosca')
        yaml = ruamel.yaml.YAML() # default  type='rt' 
        logger.info("Loading YML file {}".format(path_to_yml))
        self.micro_yml = yaml.load(Path(path_to_yml))

        self.relationship_templates = self._parse_relationship_templates()
        self._add_nodes()
        self._add_relationships()
        self._add_groups()
        return self.micro_model
    
    def _parse_relationship_templates(self):
        return  self.micro_yml.get('topology_template').get('relationship_templates')
  
    def _get_relationship_by_name(self, name):
        if name in self.relationship_templates:
            return self.relationship_templates[name]
        else:
            raise ValueError("{} relationship template does not exist".format(name))
    
    def _get_relationship_property_value(self, relationship, property_name):
        if property_name in relationship['properties']:
            return relationship['properties'][property_name]
        else:
            raise ValueError("{} property does not exist on relationshp {}".format(property_name, relationship))

    def _add_nodes(self):
        nodes_ruamel = self.micro_yml.get('topology_template').get('node_templates')
        for node_name, commented_map in nodes_ruamel.items():
            node_type = self.get_type(commented_map)
            if node_type == SERVICE:
                el = Service(node_name)
            elif node_type == DATABASE:
                el = Database(node_name)
            elif node_type == MESSAGE_BROKER:    #TODO: derived from CommunicationPattern
                el = CommunicationPattern(node_name, node_type)
            elif node_type == API_GATEWAY:
                el = CommunicationPattern(node_name, node_type)
            elif node_type == CIRCUIT_BREAKER:
                el = CommunicationPattern(node_name, node_type)
            else:
                raise ValueError("Node type {} not recognized ".format(node_type))
            self.micro_model.add_node(el) 
    
    def _add_relationships(self):
        nodes_ruamel = self.micro_yml.get('topology_template').get('node_templates')
        for node_name, commented_map in nodes_ruamel.items():
            source_node = self.micro_model[node_name]
            for req in self.get_requirements(commented_map):
                for interaction_type, target_type in req.items():
                    # [('run_time', ordereddict([('node', 'shipping'), ('relationship', 'timedout')]))]
                    is_timedout_interaction = False
                    if(isinstance(target_type, str)):
                        target_node = self.micro_model[target_type]
                        is_timedout_interaction = False
                        logger.debug("Adding relationship from {} to {}".format(source_node, target_node))
                    elif isinstance(target_type, ruamel.yaml.comments.CommentedMap):
                        for key, value in target_type.items():
                            if(key =="relationship"):
                                rel = self._get_relationship_by_name(value)
                                is_timedout_interaction = self._get_relationship_property_value(rel,"timeout")
                            elif key=="node":
                                target_node = self.micro_model[value]
                        logger.debug("Adding Timeout relationship from {} to {}".format(source_node, target_node))
                    if(interaction_type == RUN_TIME):  
                        source_node.add_run_time(target_node, with_timeout=is_timedout_interaction)
                    if(interaction_type == DEPLOYMENT_TIME):
                        source_node.add_deployment_time(target_node, with_timeout=is_timedout_interaction)
    
    def _add_groups(self):
        groups_ruamel = self.micro_yml.get('topology_template').get('groups')
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