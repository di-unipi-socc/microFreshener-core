'''
Relationships module
'''
import six

REQUIREMENTS = STORAGE, CONNECTION, DEPENDENCY, HOST =\
               'storage', 'connection', 'dependency', 'host'

CAPABILITIES = ENDPOINT, FEATURE, HOST, ATTACHMENT =\
               'endpoint', 'feature', 'host', 'attachement'


class Relationship(object):

    def __init__(self, source, target, requirement=None, capability=None):
        self.source = source
        self.target = target
        self.requirement = requirement
        self.capability = capability

    def __str__(self):
        return 'o={0.source},t={0.target},req={0.requirement},cap={0.capability}'.format(self)


def _get_str_name(obj):
    return obj if isinstance(obj, six.string_types) else obj.name


def _get_str_full_name(obj):
    return obj if isinstance(obj, six.string_types) else obj.full_name


class InteractsWith(Relationship):

    def __init__(self, source, node, alias=None,
                 requirement=CONNECTION, capability=ENDPOINT):
        super(InteractsWith, self).__init__(source, node, requirement, capability)
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
