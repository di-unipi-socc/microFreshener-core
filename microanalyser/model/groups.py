import six
from .nodes import Root

class RootGroup(object):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

class Squad(RootGroup):

    def __init__(self, name):
        super(Squad, self).__init__(name)
        self._members = {}
        self._yml = None 

    @property
    def members(self):
        return [v for k, v in self._members.items()]


    def add_node(self, member):
        # member is a string, with the methods update() the object are inserted 
        self._members[member] = member 

    def __str__(self):
        return '{} ({})'.format(self.name, 'squad')

    def __getitem__(self, name):
        return self._members.get(name, None)
    
    def __setitem__(self, key, value):
        self._members[key] = value

    def __contains__(self, member):
        if isinstance(member, six.string_types):
            return self[member] is not None
        if isinstance(item, Root):
            return self[member.name] is not None
        return False

class Edge(RootGroup):

    def __init__(self, name):
        super(Edge, self).__init__(name)
        self._members = {}
    
    @property
    def members(self):
        return [v for k, v in self._members.items()]
    
    def add_node(self, member):
        # member is a string, with the methods update() the object are inserted 
        self._members[member.name] = member 
        # self._members[member.name] = member 
        # if isinstance(member, six.string_types):
        #     self._members[member] = member 
        # if isinstance(member, Root):
        #     self._members[member.name] = member 
    
    def __str__(self):
        return '{} ({})'.format(self.name, 'edge')

    def __getitem__(self, name:str):
        return self._members.get(name, None)
    
    def __setitem__(self, key, value):
        self._members[key] = value

    def __contains__(self, member):
        if isinstance(member, six.string_types):
            return self[member] is not None
        if isinstance(member, Root):
            return self[member.name] is not None
        return False
