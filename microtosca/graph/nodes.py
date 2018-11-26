'''
Nodes module
'''

from .relationships import InteractsWith
from .helper import get_requirements, get_node_type

# CUSTOM RELATIONSHIP TYPES
INTERACT_WITH = 'micro.relationships.InteractsWith'
RUN_TIME = "run_time"
DEPLOYMENT_TIME = "deployment_time"

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
        # self.tpl = None 
        # reverse requirements
        self.up_deployment_time_requirements = []
        self.up_run_time_requirements = []

    @property
    def incoming(self):
        return  self.up_deployment_time_requirements  +  self.up_run_time_requirements 

    @property
    def incoming_run_time(self):
        return  self.up_deployment_time_requirements

    @property
    def incoming_deployment_time(self):
        return  self.up_deployment_time_requirements

    @property
    def full_name(self):
        #return '{}.{}'.format(self.tpl.name, self.name)
        return '{}'.format(self.name)

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def get_str_obj(self):
        _str_obj(self)

class Software(Root):

    def __init__(self, name):
        super(Software, self).__init__(name)

        # requirements
        self._run_time = []
        self._deployment_time = []
    
    @property
    def run_time(self):
         return (i.format for i in self._run_time)

    @property
    def deployment_time(self):
         return (i.format for i in self._deployment_time)
    
    def add_run_time(self, item):
        if not isinstance(item, InteractsWith):
            item = InteractsWith(self, item)
        self._run_time.append(item)
        if not isinstance(item.target, str):
            item.target.up_run_time_requirements.append(item)

    def add_deployment_time(self, item, alias=None):
        if not isinstance(item, InteractsWith):
            item = InteractsWith(self, item, alias)
        self._deployment_time.append(item)
        if not isinstance(item.target, str):
            item.target.up_deployment_time_requirements.append(item)
    
class Service(Root):

    def __init__(self, name):
        super(Service, self).__init__(name)
        
        self._yaml = None 

        # requirements
        self._run_time = []
        self._deployment_time = []

    #@property
    #def full_name(self):
    #    return 'tosker_{}.{}'.format(self.tpl.name, self.name)

    @property
    def relationships(self):
         return self._run_time + self._deployment_time

    @property
    def run_time(self):
         return self._run_time

    @property
    def deployment_time(self):
         return self._deployment_time
    
    @staticmethod
    def from_yaml(node_name, yaml):
        s = Service(node_name)
        s._yaml = yaml
        for req in get_requirements(yaml):
            for name, value in req.items(): # [('run_time', 'order_db')]
                if(name == RUN_TIME):  
                    s.add_run_time(value)
                if(name == DEPLOYMENT_TIME):
                    s.add_deployment_time(value)
        return s

    def update_yaml(self):
        # Update the self._yaml dictionary with the property of
        # the Service object.
        # You can also maintain updated the _yaml dictionary at
        # every change of the Service object,  but in Python you do
        # not have privacy on the property so objects can be modified
        # without you know.
        pass

    def add_run_time(self, item):
        if not isinstance(item, InteractsWith):
            item = InteractsWith(self, item)
        self._run_time.append(item)
        if not isinstance(item.target, str):
            item.target.up_run_time_requirements.append(item)

    def add_deployment_time(self, item, alias=None):
        if not isinstance(item, InteractsWith):
            item = InteractsWith(self, item, alias)
        self._deployment_time.append(item)
        if not isinstance(item.target, str):
            item.target.up_deployment_time_requirements.append(item)


    def get_str_obj(self):
        return '{}, {}'.format(
            super(Service, self).__str__(), _str_obj(self)
        )

    def __str__(self):
        return '{} ({})'.format(self.name, 'service')

class CommunicationPattern(Root):

    def __init__(self, name, ctype):
        super(CommunicationPattern, self).__init__(name)
       
        self._yaml = None # yaml object reference

        self.concrete_type = ctype # 'MessageBrocker, CircuitBRaker'

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
    def type(self):
        return self.concrete_type

    # @property
    # def run_time(self):
    #      return (i.format for i in self._run_time)

    # @property
    # def deployment_time(self):
    #      return (i.format for i in self._deployment_time)
    
    @staticmethod
    def from_yaml(node_name, node_type, yaml):
        c = CommunicationPattern(node_name, node_type)
        c._yaml = yaml
        for req in get_requirements(yaml):
            for name, value in req.items(): # [('run_time', 'order_db')]
                if(name == RUN_TIME):  
                    c.add_run_time(value)
                if(name == DEPLOYMENT_TIME):
                    c.add_deployment_time(value)
        return c

    def add_run_time(self, item):
        if not isinstance(item, InteractsWith):
            item = InteractsWith(self, item)
        self._run_time.append(item)
        if not isinstance(item.target, str):
            item.target.up_run_time_requirements.append(item)

    def add_deployment_time(self, item, alias=None):
        if not isinstance(item, InteractsWith):
            item = InteractsWith(self, item, alias)
        self._deployment_time.append(item)
        if not isinstance(item.target, str):
            item.target.up_deployment_time_requirements.append(item)

    def get_str_obj(self):
        return '{}, {}'.format(super(CommunicationPattern, self), _str_obj(self))

    def __str__(self):
        return '{} ({})'.format(self.name, self.concrete_type)

class Database(Root):

    def __init__(self, name):
        super(Database, self).__init__(name)

        self._yaml = None # yaml object reference

    #@property
    #def full_name(self):
    #    return 'tosker_{}.{}'.format(self.tpl.name, self.name)
    
    @property
    def relationships(self):
         return []

    @property
    def run_time(self):
         return []

    @property
    def deployment_time(self):
         return []

    @staticmethod
    def from_yaml(node_name, yaml):
        d = Database(node_name)
        d._yaml = yaml
        return d

    def __str__(self):
        return '{} ({})'.format(self.name, 'database')

    def get_str_obj(self):
        return '{}, {}'.format(super(Database, self), _str_obj(self))
