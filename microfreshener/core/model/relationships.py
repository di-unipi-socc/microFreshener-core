'''
Relationships module
'''
import six
import uuid


from ..errors import MicroToscaModelError, SelfLoopMicroToscaModelError


def _get_str_name(obj):
    return obj if isinstance(obj, six.string_types) else obj.name


def _get_str_full_name(obj):
    return obj if isinstance(obj, six.string_types) else obj.full_name


class Relationship(object):

    def __init__(self, source, target, id=None):
        if(source != target):
            self.source = source
            self.target = target
            self.uuid = str(uuid.uuid4()) if id is None else id
        else:
            raise SelfLoopMicroToscaModelError(
                f"Self loop relationship are not allowed in MicroTosca. Trying to add relationship from {source} to {target}")

    @property
    def id(self):
        return str(self.uuid)

    def __repr__(self):
        return 's={0.source},t={0.target}'.format(self)

    def __eq__(self, other):
        # return self.source == other.source and self.target == other.target
        return self.uuid == other.uuid

    def __hash__(self):
        return hash(self.source)+hash(self.target)

    def to_dict(self):
        # return {'source': str(self.source), 'target': str(self.target)}
        return {'source': self.source.name, 'target': self.target.name}


class InteractsWith(Relationship):

    def __init__(self, source, target, with_timeout=False,
                 with_circuit_breaker=False,
                 with_dynamic_discovery=False,
                 alias=None,
                 id=None):
        from .nodes import Service, Datastore, CommunicationPattern, MessageRouter
        if(isinstance(source, Service) or isinstance(source, MessageRouter)):
            super(InteractsWith, self).__init__(source, target, id)
            self.alias = alias
            self.property_timeout = with_timeout
            self.property_circuit_breaker = with_circuit_breaker
            self.property_dynamic_discovery = with_dynamic_discovery
        else:
            raise MicroToscaModelError(
                f"InteractWith relationship cannot be created from {source} to {target}. {type(source).__name__}")

    def set_timeout(self, value):
        self.property_timeout = value
    
    def set_circuit_breaker(self, value):
        self.property_circuit_breaker = value
    
    def set_dynamic_discovery(self, value):
        self.property_dynamic_discovery = value

    @property
    def timeout(self):
        return self.property_timeout

    @property
    def circuit_breaker(self):
        return self.property_circuit_breaker

    @property
    def dynamic_discovery(self):
        return self.property_dynamic_discovery

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

    # def __eq__(self, other):
    #     return super(InteractsWith, self).__eq__(other) and self.timeout == other.timeout and self.circuit_breaker == other.circuit_breaker and self.dynamic_discovery == other.dynamic_discovery

    def to_dict(self):
        # return {'source': str(self.source), 'target': str(self.target)}
        return {'source': self.source.name, 'target': self.target.name, "type": "interaction"}


class DeploymentTimeInteraction(InteractsWith):

    def __init__(self, source, target, with_timeout=False, with_circuit_breaker=False, with_dynamic_discovery=False, alias=None):
        super(DeploymentTimeInteraction, self).__init__(
            source, target,  with_timeout, with_circuit_breaker, with_dynamic_discovery, alias)

    def __str__(self):
        return 'DeploymentTimeInteraction({})'.format(super(InteractsWith, self).__str__())

    def __repr__(self):
        return 'DeploymentTimeInteraction({})'.format(super(InteractsWith, self).__repr__())

    def to_dict(self):
        return {'source': self.source.name, 'target': self.target.name, "type": "deploymenttime"}


class RunTimeInteraction(InteractsWith):

    def __init__(self, source, target, with_timeout=False, with_circuit_breaker=False, with_dynamic_discovery=False, alias=None):
        super(RunTimeInteraction, self).__init__(
            source, target, with_timeout, with_circuit_breaker, with_dynamic_discovery, alias)

    def __str__(self):
        return 'RunTimeInteraction({})'.format(super(RunTimeInteraction, self).__str__())

    def __repr__(self):
        return 'RunTimeInteraction({})'.format(super(RunTimeInteraction, self).__repr__())

    def to_dict(self):
        return {'source': self.source.name, 'target': self.target.name, "type": "runtime"}
