'''
MicroToscaTemplate module
'''
import six
from .nodes import Root, Service, Database, CommunicationPattern
from .groups import Squad


class MicroToscaTemplate:

    def __init__(self, name):
        self._nodes = {}
        self._groups = {}
        self.name = name

    @property
    def nodes(self):
        return (v for k, v in self._nodes.items())

    @property
    def services(self):
        return (v for k, v in self._nodes.items() if isinstance(v, Service))

    @property
    def databases(self):
        return (v for k, v in self._nodes.items() if isinstance(v, Database))

    @property
    def communicationPatterns(self):
        return (v for k, v in self._nodes.items() if isinstance(v, CommunicationPattern))

    @property
    def groups(self):
         return (v for k, v in self._groups.items())

    @property
    def squads(self):
        return (v for k, v in self._groups.items() if isinstance(v, Squad))

    def squad_of(self, node):
        for squad in self.squads:
            for member in squad.members:
                if(member == node):
                    return squad
        return None
        
    def update(self):
        self._add_pointer()
        self._add_back_links()
        self._add_groups_pointers()

    def _add_groups_pointers(self):
        for g in self.groups:
            for member in g.members:
                g[member] = self[member]

    def _add_pointer(self):
        for node in self.nodes:
            for rel in node.relationships:
                rel.target = self[rel.target]

    def _add_back_links(self):
        for node in self.nodes:
            for rel in node.run_time:
                rel.target.up_run_time_requirements.append(rel)
            for rel in node.deployment_time:
                rel.target.up_deployment_time_requirements.append(rel)

    def push(self, node):
        self._nodes[node.name] = node

    def add_group(self, group):
        self._groups[group.name] = group

    def __getitem__(self, name):
        return self._nodes.get(name, None)
 
    def __contains__(self, item):
        if isinstance(item, six.string_types):
            return self[item] is not None
        if isinstance(item, Root):
            return self[item.name] is not None
        return False

    def __str__(self):
        return ', '.join((i.name for i in self.nodes))

    # def __dict__(self):
    #      graph = dict()
    #      graph['services'] = [{"mcm":34}]
    #      return graph

    # def __setstate__(self):
    #     self.__dict__ = {"ciao":45}
