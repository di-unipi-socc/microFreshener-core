'''
Relationships module
'''
import six

REQUIREMENTS = STORAGE, CONNECTION, DEPENDENCY, HOST =\
               'storage', 'connection', 'dependency', 'host'

CAPABILITIES = ENDPOINT, FEATURE, HOST, ATTACHMENT =\
               'endpoint', 'feature', 'host', 'attachement'

def _get_str_name(obj):
    return obj if isinstance(obj, six.string_types) else obj.name

def _get_str_full_name(obj):
    return obj if isinstance(obj, six.string_types) else obj.full_name

class Relationship(object):

    def __init__(self, source, target, requirement=None, capability=None):
        self.source = source
        self.target = target
        self.requirement = requirement
        self.capability = capability
    
    def __repr__(self):
        return 's={0.source},t={0.target},req={0.requirement},cap={0.capability}'.format(self)
    
    def __eq__(self, other):
        return self.source == other.source and self.target == other.target 
    
    def __hash__(self):
        return hash(self.source)+hash(self.target)

class InteractsWith(Relationship):

    def __init__(self, source, target, alias=None,
                 requirement=CONNECTION, capability=ENDPOINT):
        super(InteractsWith, self).__init__(source, target, requirement, capability)
        self.alias = alias

    @property
    def format(self):
        full_name = _get_str_full_name(self.target)
        if self.alias is not None:
            return (full_name, self.alias)
        else:
            return (full_name, _get_str_name(self.target))

    def __str__(self):
        return 'InteractsWith({})'.format(super(InteractsWith, self).__str__())
    
    def __repr__(self):
        return 'InteractsWith({})'.format(super(InteractsWith, self).__repr__())

    
