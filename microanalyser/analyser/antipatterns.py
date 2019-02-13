

ANTIPATTERNS = WRONG_CUT, SHARED_PERSISTENCY, DEPLOYMENT_INTERACTION, DIRECT_INTERACTION, CASCADING_FAILURE =\
             'wrong_cut', 'shared_persitency', 'deployment_interaction', 'direct_Interaction', 'cascading_failure'

from ..model.relationships import InteractsWith
from ..model.nodes import Service, Database, CommunicationPattern

class Antipattern(object):

    def __init__(self):
        self.refactorings = [] # list of the refactorings to resolve the antipattern
        self.interactions = [] # list of the Interactions that cause the antipatterns

    def isEmpty(self): # check if the antipatterns has some "bad" interactions that cause the antipattern
        return len(self.interactions) == 0
    
    def getInteractions(self):
        print(self.interactions)
        return [interaction.to_dict() for interaction in self.interactions]
    
    def addRefactoring(self,refactoring):
        self.refactorings.append(refactoring)
    
    def getRefactorings(self):
        return  [refactoring for refactoring in self.refactorings]

    def to_dict(self):
        return {'name': self.name, 'cause': self.getInteractions(), 'refactorings': self.getRefactorings()}

    def check(self, node):
        pass

class WrongCutAntipattern(Antipattern):
    name = WRONG_CUT

    def __init__(self, squada, squadb, interactions):
        super(WrongCutAntipattern, self).__init__()     
        self.squada = squada
        self.squadb = squadb

        self.addRefactoring({'name':"move database"})
        self.addRefactoring({'name': "add database manager"})
        self.addRefactoring({'name': 'move communication'})
    
    # def to_dict(self):
    #     return {'name': self.name, 'cause': self.getInteractions(), 'refactorings': self.getRefactorings()}

class SharedPersistencyAntipattern(Antipattern):
    name = SHARED_PERSISTENCY

    # interactions is a list of interations that cause the shared persistence antipattern
    def __init__(self):
        super(SharedPersistencyAntipattern, self).__init__()     
        self.addRefactoring({'name':"merge services"})
        self.addRefactoring({'name': "split database"})
        self.addRefactoring({'name': 'add database manager'})
    
    # def to_dict(self):
    #     return {'name': self.name, 'cause': self.getInteractions(), 'refactorings': self.getRefactorings()}
    
    def check(self, node):
        self.interactions = node.incoming

class DeploymentInteractionAntipattern(Antipattern):
    
    name = DEPLOYMENT_INTERACTION

    def __init__(self):
        super(DeploymentInteractionAntipattern, self).__init__()
        self.addRefactoring({'name':"promote interactions"})
        self.addRefactoring({'name': "remove interaction"})

    # def to_dict(self):
    #     return {'name': self.name, 'cause': self.getInteractions(),'refactorings': self.getRefactorings()}

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

    def __init__(self, incoming=False):
        super(DirectInteractionAntipattern, self).__init__()     
        self.addRefactoring({'name':"add messagge broker"})
        self.addRefactoring({'name':"add circuit braker"})
        self.incoming = incoming # check incoming direct interactions, else check outgoing interactions

    # def to_dict(self):
    #     return {'name': self.name, 'cause': self.getInteractions(),'refactorings': self.getRefactorings()}

    def check(self, node):
        print("checking direct interaction", node.name)
        if(self.incoming):
            self.interactions = [up_rt for up_rt in node.up_run_time_requirements if (isinstance(up_rt.source, Service))]
        else:
            self.interactions = [rt for rt in node.run_time if (isinstance(rt.source, Service))]

# TODO: delete cascading failure (it is a direct interaction) --> maybe note because the same antipattenrs may have differnt refactorings
# and add the "NotResilientPath" antipatterns: 
# occurs when the path do not contains a circuitbracker communicatio npatterns.
class CascadingFailureAntipattern(Antipattern):
    
    name = CASCADING_FAILURE

    def __init__(self):
        super(CascadingFailureAntipattern, self).__init__()     
        self.addRefactoring({'name':"add circuit braker"})
        self.addRefactoring({'name':"add message broker"})

    def __str__(self):
        return 'CascadingFailure({})'.format(super(Antipattern, self).__str__())

    # def to_dict(self):
    #     return {'name': self.name, 'cause': self.getInteractions(), 'refactorings': self.getRefactorings()}
    
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