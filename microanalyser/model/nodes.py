'''
nodes module
'''

from .relationships import InteractsWith
from .helper import get_requirements

from .antipatterns import WRONG_CUT, SHARED_PERSISTENCY, DEPLOYMENT_INTERACTION, DIRECT_INTERACTION, CASCADING_FAILURE
from .antipatterns import DirectInteraction, SharedPersistency, CascadingFailure, DeploymentInteraction

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

        # reverse requirements
        self.up_deployment_time_requirements = []
        self.up_run_time_requirements = []
        self.antipatterns = {}

    def add_antipattern_function(self, funct):
        self.antipatterns[funct.__name__, funct ]

    @property
    def incoming(self):
        return  self.up_deployment_time_requirements  +  self.up_run_time_requirements 

    @property
    def incoming_run_time(self):
        return  self.up_deployment_time_requirements

    @property
    def incoming_deployment_time(self):
        return  self.up_deployment_time_requirements

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

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
    
class Service(Software):

    def __init__(self, name):
        super(Service, self).__init__(name)
        
        # requirements
        self._run_time = []
        self._deployment_time = []

    def check_antipatterns(self, config_analysis={}):
        # config_analysis  = {
        #      'antipatterns' :['ap1, ap2, apn]
        #      'refactorings'. [r1, r2, rn]
        # }
        antipatterns =[]
        antipatterns_to_discard = config_analysis.get('antipatterns',[])
        refactorings = config_analysis.get('refactorings',[])
        if DEPLOYMENT_INTERACTION not in antipatterns_to_discard:
            antipatterns.append(self._deployment_interations().to_dict())
        if DIRECT_INTERACTION  not in antipatterns_to_discard:
            antipatterns.append(self._direct_interactions().to_dict())
        if CASCADING_FAILURE  not in antipatterns_to_discard:
            antipatterns.append(self._cascading_failures().to_dict())
        return antipatterns

    def _deployment_interations(self):
        deployment_interactions = [dt_interaction for dt_interaction in self.deployment_time 
                            if (isinstance(dt_interaction.target, Service)
                            # TODO: cehck if the targer is derived from teh  Communication Pattern class
                            or isinstance(dt_interaction.target, CommunicationPattern))]
        return DeploymentInteraction(deployment_interactions)

    def _direct_interactions(self):
        interactions = [up_rt for up_rt in self.up_run_time_requirements if (isinstance(up_rt.source, Service))]
        return DirectInteraction(interactions)

    def _cascading_failures(self):
        interactions = [rt_int for rt_int in self.run_time if isinstance(rt_int.target, Service)]
        # TODO: guardare se esiste un path che arriva a un'altro servizio in cui non c'è un CircuiBreaker
        # nodes_patterns = [req.target for req in node.run_time if (isinstance(req.target, CommunicationPattern) and
        #                    renq.target.concrete_type !=  CIRCUIT_BREAKER)
        #             ]
        # vs_patterns = [node for node in nodes_patterns if node.]
        return CascadingFailure(interactions)

    @property
    def relationships(self):
         return self._run_time + self._deployment_time

    @property
    def run_time(self):
         return self._run_time

    @property
    def deployment_time(self):
         return self._deployment_time

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

class CommunicationPattern(Software):

    def __init__(self, name, ctype):
        super(CommunicationPattern, self).__init__(name)
       
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
    
    def check_antipatterns(self, constraints):
        return []

    # @property
    # def run_time(self):
    #      return (i.format for i in self._run_time)

    # @property
    # def deployment_time(self):
    #      return (i.format for i in self._deployment_time)
    

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

    @property
    def relationships(self):
         return []

    @property
    def run_time(self):
         return []

    @property
    def deployment_time(self):
         return []

    def check_antipatterns(self, config_analysis={}):
        antipatterns = []
        antipatterns_to_discard = config_analysis.get('antipatterns',[])
        # refactorings = config_analysis.get('refactorings',[])
        if SHARED_PERSISTENCY not in antipatterns_to_discard:
            antipatterns.append(self._shared_persitency().to_dict())
        return antipatterns
    
    def _shared_persitency(self):
       return SharedPersistency(self.incoming) if len(self.incoming) > 1 else None

    def __str__(self):
        return '{} ({})'.format(self.name, 'database')

    def get_str_obj(self):
        return '{}, {}'.format(super(Database, self), _str_obj(self))