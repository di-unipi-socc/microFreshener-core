import six
from .nodes import Root, Database
from ..logging import MyLogger

logger = MyLogger().get_logger()


class RootGroup(object):

    def __init__(self, name):
        self.name = name
        self._members = {}

    @property
    def members(self):
        return [v for k, v in self._members.items()]

    def to_dict(self):
        return {"name": self.name, "nodes": [node.name in self.members]}

    def add_member(self, member):
        self._members[member.name] = member

    def __contains__(self, member):
        if isinstance(member, six.string_types):
            return self[member] is not None
        if isinstance(member, Root):
            return self[member.name] is not None
        return False

    def __getitem__(self, name):
        return self._members.get(name, None)

    def __setitem__(self, key, value):
        self._members[key] = value

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)


class Team(RootGroup):

    def __init__(self, name):
        super(Team, self).__init__(name)

    def __str__(self):
        return '{} ({})'.format(self.name, 'squad')


class Edge(RootGroup):

    def __init__(self, name):
        super(Edge, self).__init__(name)

    def add_member(self, member):
        if(not isinstance(member, Database)):
            super(Edge, self).add_member(member)

    def __str__(self):
        return '{} ({})'.format(self.name, 'edge')
