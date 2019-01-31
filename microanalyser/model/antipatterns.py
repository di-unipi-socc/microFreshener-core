from .relationships import InteractsWith

ANTIPATTERNS = WRONG_CUT, SHARED_PERSISTENCY, DEPLOYMENT_INTERACTION, DIRECT_INTERACTION, CASCADING_FAILURE =\
             'wrong_cut', 'shared_persitency', 'deployment_interaction', 'direct_Interaction', 'cascading_failure'

class Antipattern(object):
    def __init__(self, interactions):
        self.refactorings = []
        self.interactions = interactions # list of the interactions that cause the antipatterns

    def isEmpty(self): # check if the antipatterns has some "bad" interactions that cause the antipattern
        return len(self.interactions) == 0
    
    def getInteractions(self):
        return  [i.to_dict() for i in self.interactions]

class WrongCut(Antipattern):
    name = WRONG_CUT

    def __init__(self, squada, squadb, interaction):
        super(Antipattern, self).__init__(interactions)       
        self.squada = squada
        self.squadb = squadb
    
    def to_dict(self):
        return {'name': self.name, 'cause':self.getInteractions()}
    
    def refactorings(self):
        return [ {'id':1, 'name': 'prova1'},{'id': 2, 'name': 'prova2'}]

class SharedPersistency(Antipattern):
    name = SHARED_PERSISTENCY

    # interactions is a list of interations that cause the shared persistence antipattern
    def __init__(self, interactions):
        super(SharedPersistency, self).__init__(interactions)       
        # self.interactions = interactions 
    
    def to_dict(self):
        return {'name': self.name, 'cause': self.getInteractions()}

class DeploymentInteraction(Antipattern):
    
    name = DEPLOYMENT_INTERACTION

    def __init__(self, interactions):
        super(DeploymentInteraction, self).__init__(interactions)   

    def to_dict(self):
        return {'name': self.name, 'cause': self.getInteractions()}

    def refactorings(self):
        return [ {'id':1, 'name': 'splitdatabase'}, {'id':1, 'name': 'merge services'}]
    
class DirectInteraction(Antipattern):
    
    name = DIRECT_INTERACTION

    def __init__(self, interactions):
        super(DirectInteraction, self).__init__(interactions)       
        # self.interactions = interactions  #  list of interactions that cause the antipattern

    def to_dict(self):
        return {'name': self.name, 
                'cause': self.getInteractions(),
        }
                # 'refactorings': self.refactorings()}

    def refactorings(self):
        return [ {'id':1, 'name': 'splitdatabase'}, {'id':1, 'name': 'merge services'}]
    
class CascadingFailure(Antipattern):
    
    name = CASCADING_FAILURE

    def __init__(self, interactions):
        super(CascadingFailure, self).__init__(interactions)       
        # self.interactions = interactions

    def __str__(self):
        return 'CascadingFailure({})'.format(super(Antipattern, self).__str__())

    def to_dict(self):
        return {'name': self.name, 'cause': self.getInteractions()}

    def refactorings(self):
        return [ {'id':1, 'name': 'splitdatabase'}, {'id':1, 'name': 'merge services'}]
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