

ANTIPATTERNS = WRONG_CUT, SHARED_PERSISTENCY, DEPLOYMENT_INTERACTION, DIRECT_INTERACTION, CASCADING_FAILURE =\
             'wrong_cut', 'shared_persitency', 'deployment_interaction', 'direct_Interaction', 'cascading_failure'

from  ..model.relationships import InteractsWith
from ..model.nodes import Service, Database, CommunicationPattern

class Antipattern(object):
    def __init__(self):
        self.refactorings = []
        self.interactions = [] # list of the interactions that cause the antipatterns

    def isEmpty(self): # check if the antipatterns has some "bad" interactions that cause the antipattern
        return len(self.interactions) == 0
    
    def getInteractions(self):
        return  self.interactions
    
    def check(self, node):
        print("chcking antipatterns", node.name)

class WrongCutAntipattern(Antipattern):
    name = WRONG_CUT

    def __init__(self, squada, squadb, interactions):
        super(WrongCutAntipattern, self).__init__()     
        self.squada = squada
        self.squadb = squadb
    
    def to_dict(self):
        return {'name': self.name, 'cause':self.getInteractions()}
    
    def refactorings(self):
        return [ {'id':1, 'name': 'prova1'},{'id': 2, 'name': 'prova2'}]

class SharedPersistencyAntipattern(Antipattern):
    name = SHARED_PERSISTENCY

    # interactions is a list of interations that cause the shared persistence antipattern
    def __init__(self):
        super(SharedPersistencyAntipattern, self).__init__()     
        # self.interactions = interactions 
    
    def to_dict(self):
        return {'name': self.name, 'cause': self.getInteractions()}
    
    def check(self, node):
        self.interactions = node.incoming

class DeploymentInteractionAntipattern(Antipattern):
    
    name = DEPLOYMENT_INTERACTION

    def __init__(self):
        super(DeploymentInteractionAntipattern, self).__init__() 

    def to_dict(self):
        return {'name': self.name, 'cause': self.getInteractions()}

    def refactorings(self):
        return [ {'id':1, 'name': 'splitdatabase'}, {'id':1, 'name': 'merge services'}]
    
    def check(self, node):
        print("checking deployment interactions", node.name)
        deployment_interactions = [dt_interaction for dt_interaction in node.deployment_time 
                            if (isinstance(dt_interaction.target, Service)
                            # TODO: check if the targer is derived from the Communication Pattern class
                            or isinstance(dt_interaction.target, CommunicationPattern))]
        self.interactions = deployment_interactions
    
class DirectInteractionAntipattern(Antipattern):
    
    name = DIRECT_INTERACTION

    def __init__(self):
        super(DirectInteractionAntipattern, self).__init__()     
        # self.interactions = interactions  #  list of interactions that cause the antipattern

    def to_dict(self):
        return {'name': self.name, 
                'cause': self.getInteractions(),
        }
                # 'refactorings': self.refactorings()}

    def refactorings(self):
        return [ {'id':1, 'name': 'splitdatabase'}, {'id':1, 'name': 'merge services'}]
    
    def check(self, node):
        print("chcking direct interactions", node.name)
        self.interactions = [up_rt for up_rt in node.up_run_time_requirements if (isinstance(up_rt.source, Service))]
        

# TODO: delete cascading failure ( it is a direct interaction) 
# and add the "NotResilientPath"  antipatterns: occurs when the path do not contains a circuitbracker communicatio npatterns.
class CascadingFailureAntipattern(Antipattern):
    
    name = CASCADING_FAILURE

    def __init__(self):
        super(CascadingFailureAntipattern, self).__init__()     
        # self.interactions = interactions

    def __str__(self):
        return 'CascadingFailure({})'.format(super(Antipattern, self).__str__())

    def to_dict(self):
        return {'name': self.name, 'cause': self.getInteractions()}

    def refactorings(self):
        return [ {'id':1, 'name': 'splitdatabase'}, {'id':1, 'name': 'merge services'}]
    
    def check(self, node):
        print("chcking cascading failure antipatterns", node.name)

    # antipatterns : [
    #                 {   id: 1,
    #                     name: cascading_failure 
    #                     cause: [Interaction(1),..., Interaction(n)]
    #                     refactorings: [
    #                         {   id: 1,
    #                             name: movedbT1,
    #                             solution: 
    #                         },
    #                         {   id: 2,
    #                             name: movedbT2:
    #                             solution:  
    #                         },
    #                         {   id: 3
    #                             name: addManager: 
    #                             solution; 
    #                         }
    #                 ]
    #             ]
    #]