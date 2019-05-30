'''
nodes module
'''

from .relationships import DeploymentTimeInteraction, RunTimeInteraction
from ..logging import MyLogger

logger = MyLogger().get_logger()


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
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

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

    def add_run_time(self, item, with_timeout=False, with_circuit_breaker=False, with_dynamic_discovery=False):
        logger.debug("{}: adding runtime link to {}".format(self, item))
        if not isinstance(item, RunTimeInteraction):
            item = RunTimeInteraction(self, item, with_timeout=with_timeout,
                                      with_circuit_breaker=with_circuit_breaker, 
                                      with_dynamic_discovery=with_dynamic_discovery)
        self._run_time.append(item)
        if not isinstance(item.target, str):
            item.target.up_run_time_requirements.append(item)

    def add_deployment_time(self, item, with_timeout=False, with_circuit_breaker=False, with_dynamic_discovery=False):
        logger.debug("{}: adding deployment link to {}".format(self, item))
        if not isinstance(item, DeploymentTimeInteraction):
            item = DeploymentTimeInteraction(self, item, with_timeout=with_timeout,
                                      with_circuit_breaker=with_circuit_breaker, 
                                      with_dynamic_discovery=with_dynamic_discovery)
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


    def __str__(self):
        return '{} ({})'.format(self.name, 'service')

class CommunicationPattern(Software):

    def __init__(self, name, short_name="CP"):
        super(CommunicationPattern, self).__init__(name)

        self.short_name = short_name
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

    def __str__(self):
        return '{} ({})'.format(self.name, self.short_name)

class MessageBroker(CommunicationPattern):

    def __init__(self, name):
          super(MessageBroker, self).__init__(name, "MB")
    
    def __str__(self):
        return '{} ({})'.format(self.name, self.short_name)

class MessageRouter(CommunicationPattern):

    def __init__(self, name):
          super(MessageRouter, self).__init__(name, "MR")

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

