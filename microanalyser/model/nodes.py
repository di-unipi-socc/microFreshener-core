'''
nodes module
'''

from .relationships import DeploymentTimeInteraction, RunTimeInteraction
from ..logging import MyLogger

logger = MyLogger().get_logger()

def _add_to_map(d, k, v):
    if d is None:
        d[k] = v
    return d


def _add_to_list(l_name, i):
    if l_name is None:
        l_name = []
    l_name.append(i)
    return l_name


def _str_obj(o):
    return ', '.join(["{}: {}".format(k, v) for k, v in vars(o).items()])


class Root(object):

    def __init__(self, name):
        self.name = name

        # reverse requirements
        self.up_deployment_time_requirements = []
        self.up_run_time_requirements = []

    def remove_incoming_relationship(self, relationship):
        if isinstance(relationship, RunTimeInteraction) and relationship in self.up_run_time_requirements:
            self.up_run_time_requirements.remove(relationship)
        if isinstance(relationship, DeploymentTimeInteraction) and relationship in self.up_deployment_time_requirements:
            self.up_deployment_time_requirements.remove(relationship)

    @property
    def incoming(self):
        return self.up_deployment_time_requirements + self.up_run_time_requirements

    @property
    def incoming_run_time(self):
        return self.up_run_time_requirements

    @property
    def incoming_deployment_time(self):
        return self.up_deployment_time_requirements
    

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == self.name

    def __hash__(self):
        return hash(self.name)

    def get_str_obj(self):
        _str_obj(self)

    def to_dict(self):
        return {'name': self.name}

class Software(Root):

    def __init__(self, name):
        super(Software, self).__init__(name)

        # requirements
        self._run_time = []
        self._deployment_time = []

    @property
    def relationships(self):
        return self._run_time + self._deployment_time

    @property
    def run_time(self):
        return (i.format for i in self._run_time)

    @property
    def deployment_time(self):
        return (i.format for i in self._deployment_time)

    def add_run_time(self, item):
        logger.debug("{}: adding runtime link to {}".format(self, item))
        if not isinstance(item, RunTimeInteraction):
            item = RunTimeInteraction(self, item)
        self._run_time.append(item)
        if not isinstance(item.target, str):
            item.target.up_run_time_requirements.append(item)

    def add_deployment_time(self, item, alias=None):
        logger.debug("{}: adding deployment link to {}".format(self, item))
        if not isinstance(item, DeploymentTimeInteraction):
            item = DeploymentTimeInteraction(self, item, alias)
        self._deployment_time.append(item)
        if not isinstance(item.target, str):
            item.target.up_deployment_time_requirements.append(item)


class Service(Software):

    def __init__(self, name):
        super(Service, self).__init__(name)

        # requirements
        self._run_time = []
        self._deployment_time = []

    @property
    def relationships(self):
        return self._run_time + self._deployment_time

    @property
    def run_time(self):
        return self._run_time

    @property
    def deployment_time(self):
        return self._deployment_time

    def get_str_obj(self):
        return '{}, {}'.format(
            super(Service, self).__str__(), _str_obj(self)
        )

    def __str__(self):
        return '{} ({})'.format(self.name, 'service')


class CommunicationPattern(Software):

    def __init__(self, name, ctype):
        super(CommunicationPattern, self).__init__(name)

        self.concretetype = ctype  # 'MessageBrocker, CircuitBreaker', 'ApiGateway'

        # requirements
        self._run_time = []
        self._deployment_time = []

    @property
    def relationships(self):
        return self._run_time + self._deployment_time

    @property
    def run_time(self):
        return self._run_time

    @property
    def deployment_time(self):
        return self._deployment_time

    @property
    def concrete_type(self):
        return self.concretetype

    # @property
    # def run_time(self):
    #      return (i.format for i in self._run_time)

    # @property
    # def deployment_time(self):
    #      return (i.format for i in self._deployment_time)

    def get_str_obj(self):
        return '{}, {}'.format(super(CommunicationPattern, self), _str_obj(self))

    def __str__(self):
        return '{} ({})'.format(self.name, self.concrete_type)

class Database(Root):

    def __init__(self, name):
        super(Database, self).__init__(name)
        # self.addPrinciples(DecentraliseEverythingPrinciple)

    @property
    def relationships(self):
        return []

    @property
    def run_time(self):
        return []

    @property
    def deployment_time(self):
        return []

    def __str__(self):
        return '{} ({})'.format(self.name, 'database')

    def get_str_obj(self):
        return '{}, {}'.format(super(Database, self), _str_obj(self))
