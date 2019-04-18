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

    def to_dict(self):
        return {'source': str(self.source), 'target': str(self.target)}


class InteractsWith(Relationship):

    def __init__(self, source, target, is_timedout=False, alias=None,
                 requirement=CONNECTION, capability=ENDPOINT):
        super(InteractsWith, self).__init__(
            source, target, requirement, capability)
        self.alias = alias
        self.is_timedout = is_timedout

    @property
    def timedout(self):
        return self.is_timedout

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

    def to_dict(self):
        return {'source': str(self.source), 'target': str(self.target)}


class DeploymentTimeInteraction(InteractsWith):

    def __init__(self, source, target, is_timedout=False, alias=None,
                 requirement=CONNECTION, capability=ENDPOINT):
        super(DeploymentTimeInteraction, self).__init__(
            source, target, is_timedout, alias, requirement, capability)

    def __str__(self):
        return 'DeploymentTimeInteraction({})'.format(super(InteractsWith, self).__str__())

    def __repr__(self):
        return 'DeploymentTimeInteraction({})'.format(super(InteractsWith, self).__repr__())

    def to_dict(self):
        # return {'source': str(self.source), 'target': str(self.target), "type":"deploymenttime"}
        return {'source': self.source.name, 'target': self.target.name, "type": "deploymenttime"}



class RunTimeInteraction(InteractsWith):

    def __init__(self, source, target, is_timedout=False, alias=None,
                 requirement=CONNECTION, capability=ENDPOINT):
        super(RunTimeInteraction, self).__init__(
            source, target, is_timedout, alias, requirement, capability)

    def __str__(self):
        return 'RunTimeInteraction({})'.format(super(RunTimeInteraction, self).__str__())

    def __repr__(self):
        return 'RunTimeInteraction({})'.format(super(RunTimeInteraction, self).__repr__())

    def to_dict(self):
        # return {'source': str(self.source), 'target': str(self.target), "type":"runtime"}
        return {'source': self.source.name, 'target': self.target.name, "type": "runtime"}
