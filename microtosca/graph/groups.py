import six
from .helper import get_members

class Root(object):

    def __init__(self,name):
        self.name = name

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

class Squad(Root):

    def __init__(self, name):
        super(Squad, self).__init__(name)
        self._members = {}
        self._yml = None 

    @property
    def members(self):
        return [v for k, v in self._members.items()]

    @classmethod
    def from_yaml(cls, group_name, yaml):
        g = cls(group_name)
        g._yaml = yaml
        for member in get_members(yaml):
            g.push(member)
        return g

    def push(self, member):
        # membere is a string
        # TODO: maybe _members can be an array insted of a dictionary
        self._members[member] = member 

    def __str__(self):
        return '{} ({})'.format(self.name, 'squad')

    def __getitem__(self, name):
        return self._members.get(name, None)
    
    def __setitem__(self, key, value):
        self._members[key] = value

    def __contains__(self, item):
        if isinstance(item, six.string_types):
            return self[item] is not None
        if isinstance(item, Root):
            return self[item.name] is not None
        return False