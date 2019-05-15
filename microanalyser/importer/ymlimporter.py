import ruamel.yaml
from pathlib import Path
from ..model import MicroToscaModel
from ..model import Service, Database, CommunicationPattern, MessageBroker, MessageRouter
from ..model.groups import Team, Edge
from .iimporter import Importer
from ..model.type import MICROTOSCA_NODES_SERVICE, MICROTOSCA_NODES_COMMUNICATIONPATTERN, MICROTOSCA_NODES_DATABASE, MICROTOSCA_NODES_MESSAGE_BROKER, MICROTOSCA_NODES_MESSAGE_ROUTER
from ..model.type import MICROTOSCA_GROUPS_TEAM, MICROTOSCA_GROUPS_EDGE
from ..model.type import MICROTOSCA_RELATIONSHIPS_INTERACT_WITH
from ..model.type import MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_TIMEOUT_PROPERTY, MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_DYNAMIC_DISCOVEY_PROPERTY, MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_CIRCUIT_BREAKER_PROPERTY
from .ymltype import YML_RUN_TIME, YML_DEPLOYMENT_TIME
from .ymltype import YML_RELATIONSHIP_T, YML_RELATIONSHIP_D, YML_RELATIONSHIP_C, YML_RELATIONSHIP_CD, YML_RELATIONSHIP_TC, YML_RELATIONSHIP_TD, YML_RELATIONSHIP_TCD
from .ymltype import YML_RELATIONSHIP_TEMPLATE
from ..errors import ImporterError
from ..logging import MyLogger

logger = MyLogger().get_logger()


class YMLImporter(Importer):

    def __init__(self):
        self.micro_model = None

    def Import(self, path_to_yml)->MicroToscaModel:
        self.micro_model = MicroToscaModel('micro.tosca')
        yaml = ruamel.yaml.YAML()  # default  type='rt'
        logger.info("Loading YML file: {}".format(path_to_yml))
        self.micro_yml = yaml.load(Path(path_to_yml))

        self.relationship_templates = self._parse_relationship_templates()
        self._add_nodes()
        self._add_relationships()
        self._add_groups()
        return self.micro_model

    def _parse_relationship_templates(self):
        return self.micro_yml.get('topology_template').get('relationship_templates')

    def _get_relationship_template_by_name(self, name):
        if name in YML_RELATIONSHIP_TEMPLATE:
            if name in self.relationship_templates:
                return self.relationship_templates[name]
            else:
                raise ImporterError(f"Relationship template  {name} does not exist")
        else:
            raise ImporterError(f"Relationship template {name} is not a valid relationship template.")

    def _get_relationship_property_values(self, relationship):
        is_timeout = False
        is_circuit_breaker = False
        is_dynamic_discovery = False
        if MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_TIMEOUT_PROPERTY in relationship['properties']:
            is_timeout = relationship['properties'][MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_TIMEOUT_PROPERTY]
        if MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_CIRCUIT_BREAKER_PROPERTY in relationship['properties']:
            is_circuit_breaker = relationship['properties'][MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_CIRCUIT_BREAKER_PROPERTY]
        if MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_DYNAMIC_DISCOVEY_PROPERTY in relationship['properties']:
            is_dynamic_discovery = relationship['properties'][MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_DYNAMIC_DISCOVEY_PROPERTY]
        return (is_timeout, is_circuit_breaker, is_dynamic_discovery)

    def _add_nodes(self):
        nodes_ruamel = self.micro_yml.get(
            'topology_template').get('node_templates')
        for node_name, commented_map in nodes_ruamel.items():
            node_type = self.get_type(commented_map)
            if node_type == MICROTOSCA_NODES_SERVICE:
                el = Service(node_name)
            elif node_type == MICROTOSCA_NODES_DATABASE:
                el = Database(node_name)
            elif node_type == MICROTOSCA_NODES_MESSAGE_BROKER:
                el = MessageBroker(node_name)
            elif node_type == MICROTOSCA_NODES_MESSAGE_ROUTER:
                el = MessageRouter(node_name)
            elif node_type == MICROTOSCA_NODES_COMMUNICATIONPATTERN:
                raise ImporterError(f"The node type {MICROTOSCA_NODES_COMMUNICATIONPATTERN} cannot be istantiated.")
            else:
                raise ImporterError(f"The node type {node_type} not recognized.")
            self.micro_model.add_node(el)

    def _add_relationships(self):
        nodes_ruamel = self.micro_yml.get(
            'topology_template').get('node_templates')
        for node_name, commented_map in nodes_ruamel.items():
            source_node = self.micro_model[node_name]
            for req in self.get_requirements(commented_map):
                for interaction_type, target_type in req.items():
                    # [('run_time', ordereddict([('node', 'shipping'), ('relationship', 't'| 'c'| 'd')]))]
                    is_timeout = False
                    is_circuit_breaker = False
                    is_dynamic_discovery = False
                    if(isinstance(target_type, str)):
                        target_node = self.micro_model[target_type]
                    elif isinstance(target_type, ruamel.yaml.comments.CommentedMap):
                        for key, value in target_type.items():
                            if(key == "relationship"):
                                rel = self._get_relationship_template_by_name(value)
                                (is_timeout, is_circuit_breaker,
                                 is_dynamic_discovery) = self._get_relationship_property_values(rel)
                            elif key == "node":
                                target_node = self.micro_model[value]
                            else:
                                raise ImporterError(
                                    "Relationship {} not recognized ".format(key))
                    else:
                        raise ImporterError(
                            "Target type {} of relatinoship {} not recognized ".format(target_type, req))
                    if(interaction_type == YML_RUN_TIME):
                        source_node.add_run_time(
                            target_node, is_timeout, is_circuit_breaker, is_dynamic_discovery)
                    if(interaction_type == YML_DEPLOYMENT_TIME):
                        source_node.add_deployment_time(
                            target_node, with_timeout=is_timeout)

    def _add_groups(self):
        if 'groups' in self.micro_yml.get('topology_template'):
            groups_ruamel = self.micro_yml.get('topology_template').get('groups')
            for (group_name, ordered_dict) in groups_ruamel.items():
                group_type = self.get_type(ordered_dict)
                if group_type == MICROTOSCA_GROUPS_TEAM:
                    group = Team(group_name)
                    for member in self.get_members(ordered_dict):
                        group.add_member(self.micro_model[member])
                if group_type == MICROTOSCA_GROUPS_EDGE:
                    group = Edge(group_name)
                    for member in self.get_members(ordered_dict):
                        group.add_member(self.micro_model[member])
                self.micro_model.add_group(group)

    def get_requirements(self, ruamel_commented_map):
        return ruamel_commented_map['requirements'] if 'requirements' in ruamel_commented_map else []

    def get_type(self, ruamel_commented_map):
        return ruamel_commented_map['type'] if 'type' in ruamel_commented_map else ''

    def get_members(self, ruamel_commented_map):
        return ruamel_commented_map['members'] if 'members' in ruamel_commented_map else []
