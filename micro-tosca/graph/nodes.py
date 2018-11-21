'''
Nodes module
'''

from .relationships import InteractsWith


def _add_to_map(d, k, v):
    if d is None:
        d = {}
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
        self.tpl = None

        self._ATTRIBUTE = {}

        # reverse requirements
        self.up_requirements = []

    @property
    def full_name(self):
        return '{}.{}'.format(self.tpl.name, self.name)

    @property
    def depend(self):
        return (i.format for i in self._depend)

    def __str__(self):
        return self.name

    def __getitem__(self, item):
        return self._ATTRIBUTE.get(item, lambda: None)()

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def get_str_obj(self):
        _str_obj(self)


class Service(Root):

    def __init__(self, name):
        super(Service, self).__init__(name)

        # attributes
        self.id = None

        self._ATTRIBUTE = {
            'id': lambda: self.id,
        }

        # requirements
        self._run_time = []
        self._deployment_time = []

    def add_run_time(self, item):
        if not isinstance(item, InteractsWith):
            item = InteractsWith(self, item)
        self._run_time.append(item)
        if not isinstance(item.target, str):
            item.target.up_requirements.append(item)

    def add_deployment_time(self, item, alias=None):
        if not isinstance(item, InteractsWith):
            item = InteractsWith(self, item, alias)
        self._deployment_time.append(item)
        if not isinstance(item.target, str):
            item.target.up_requirements.append(item)

    @property
    def full_name(self):
        return 'tosker_{}.{}'.format(self.tpl.name, self.name)

    @property
    def run_time(self):
         return (i.format for i in self._run_time)

    @property
    def deployment_time(self):
         return (i.format for i in self._deployment_time)

    @property
    def relationships(self):
         return self._run_time + self._deployment_time

    def get_str_obj(self):
        return '{}, {}'.format(
            super(Container, self).__str__(), _str_obj(self)
        )

    def __str__(self):
        return '{} ({})'.format(self.name, 'container')


class Database(Root):

    def __init__(self, name):
        super(Database, self).__init__(name)
        # attributes
        self.id = None

        self._ATTRIBUTE = {
            'id': lambda: self.id,
        }

    @property
    def full_name(self):
        return 'tosker_{}.{}'.format(self.tpl.name, self.name)

    def __str__(self):
        return '{} ({})'.format(self.name, 'database')

    def get_str_obj(self):
        return '{}, {}'.format(super(Database, self), _str_obj(self))


class CommunicationPattern(Root):

    def __init__(self, name):
        super(CommunicationPattern, self).__init__(name)

        # requirements
        self._run_time = []
        self._deployment_time = None


    @property
    def run_time(self):
         return (i.format for i in self._run_time)

    @property
    def deployment_time(self):
         return (i.format for i in self._deployment_time)

    @property
    def relationships(self):
         return self._run_time + self._deployment_time


    def get_str_obj(self):
        return '{}, {}'.format(super(CommunicationPattern, self), _str_obj(self))

    def __str__(self):
        return '{} ({})'.format(self.name, 'software')

class CircuitBreaker(Root):

    def __init__(self, name):
        super(CircuitBreaker, self).__init__(name)
