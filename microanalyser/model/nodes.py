'''
nodes module
'''

from .relationships import DeploymentTimeInteraction, RunTimeInteraction
from .helper import get_requirements

# from .antipatterns import WRONG_CUT, SHARED_PERSISTENCY, DEPLOYMENT_INTERACTION, DIRECT_INTERACTION, CASCADING_FAILURE
# from .antipatterns import DirectInteraction, SharedPersistency, CascadingFailure, DeploymentInteraction
# from ..analyser.principles import BoundedContextPrinciple, DecentralizedDataPrinciple, IndependentlyDeployablePrinciple, HorizzontallyScalablePrinciple, FaultResiliencePrinciple

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

        
        self.antipatterns = [] # list of antipatterns afflicting a node 
        # self.principles = []   # list of principles associated with a node 
    
    # def addPrinciples(self, principle):
    #     self.principles.append(principle)

    def getPrinciples(self):
        return self.principles

    def addAntipattern(self, antipattern):
        if(not antipattern.isEmpty()):
            self.antipatterns.append(antipattern)
    
    def getAntipatterns(self):
        return [ a.to_dict() for a in self.antipatterns]

    def remove_incoming_relationship(self, relationship):
        if isinstance(relationship, RunTimeInteraction) and relationship in self.up_run_time_requirements:
            self.up_run_time_requirements.remove(relationship)
        if isinstance(relationship, DeploymentTimeInteraction) and relationship in self.up_deployment_time_requirements:
            self.up_deployment_time_requirements.remove(relationship)

    @property
    def neighbors(self):
        return set()

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
    def neighbors(self):
        return set(rel.target for rel in self.relationships)

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
        if not isinstance(item, RunTimeInteraction):
            item = RunTimeInteraction(self, item)
        self._run_time.append(item)
        if not isinstance(item.target, str):
            item.target.up_run_time_requirements.append(item)

    def add_deployment_time(self, item, alias=None):
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

        # principles associated with a Service node
        # self.addPrinciples(IndependentlyDeployablePrinciple())
        # self.addPrinciples(HorizzontallyScalablePrinciple())
        # self.addPrinciples(FaultResiliencePrinciple())
    
    # TODO: add options to the method to persalised the analysis
    def analyse(self, options=None):
        for principle in self.getPrinciples():
            # if principle not in options.principles_to_discard
            print("\n" + str(principle))
            for antipattern in principle.getAntipatterns():
                # if antipattern not in options.principles_to_discard
                antipattern.check(self)

    # TODO remove 
    def check_antipatterns(self, antipatterns_tobe_discarded=[]):
        if DEPLOYMENT_INTERACTION not in antipatterns_tobe_discarded:
            self.addAntipattern(self._deployment_interations())
        if DIRECT_INTERACTION  not in antipatterns_tobe_discarded:
            self.addAntipattern(self._direct_interactions())
        if CASCADING_FAILURE  not in antipatterns_tobe_discarded:
            self.addAntipattern(self._cascading_failures())
        return self.getAntipatterns()

    # TODO remove this method put the into antipattern class
    # def _deployment_interations(self):
    #     print("Checking deployment imte interactions for antiapattere")
    #     deployment_interactions = [dt_interaction for dt_interaction in self.deployment_time 
    #                         if (isinstance(dt_interaction.target, Service)
    #                         # TODO: cehck if the targer is derived from teh  Communication Pattern class
    #                         or isinstance(dt_interaction.target, CommunicationPattern))]
    #     return DeploymentInteraction(deployment_interactions)

    # def _direct_interactions(self):
    #     interactions = [up_rt for up_rt in self.up_run_time_requirements if (isinstance(up_rt.source, Service))]
    #     return DirectInteraction(interactions)

    # def _cascading_failures(self):
    #     interactions = [rt_int for rt_int in self.run_time if isinstance(rt_int.target, Service)]
    #     # TODO: guardare se esiste un path che arriva a un'altro servizio in cui non c'è un CircuiBreaker
    #     # nodes_patterns = [req.target for req in node.run_time if (isinstance(req.target, CommunicationPattern) and
    #     #                    renq.target.concrete_type !=  CIRCUIT_BREAKER)
    #     #             ]
    #     # vs_patterns = [node for node in nodes_patterns if node.]
    #     return CascadingFailure(interactions)

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
    
    def get_str_obj(self):
        return '{}, {}'.format(super(CommunicationPattern, self), _str_obj(self))

    def __str__(self):
        return '{} ({})'.format(self.name, self.concrete_type)

    # def __eq__(self, other):
    #     return super(CommunicationPattern, self).__eq__(other) and  self.concrete_type == other.type

    # def __hash__(self):
    #     return hash(self.name)

class Database(Root):

    def __init__(self, name):
        super(Database, self).__init__(name)
        # self.addPrinciples(DecentralizedDataPrinciple)

    @property
    def relationships(self):
         return []

    @property
    def run_time(self):
         return []

    @property
    def deployment_time(self):
         return []

    # TODO; maybe to be moved inside the Principle Class
    def check_antipatterns(self, antipatterns_tobe_discarded=[]):
        if SHARED_PERSISTENCY not in antipatterns_tobe_discarded:
            self.addAntipattern(self._shared_persitency())
        return self.getAntipatterns()

    def count_antipatterns(self):
        return len(self.check_antipatterns)

    def _shared_persitency(self):
       return SharedPersistency(self.incoming)

    def __str__(self):
        return '{} ({})'.format(self.name, 'database')

    def get_str_obj(self):
        return '{}, {}'.format(super(Database, self), _str_obj(self))