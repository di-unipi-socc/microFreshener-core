
REFACTORINGS = WRONG_CUT, SHARED_PERSISTENCY, DEPLOYMENT_INTERACTION, DIRECT_INTERACTION, CASCADING_FAILURE =\
             'wrong_cut', 'shared_persitency', 'deployment_interaction', 'direct_Interaction', 'cascading_failure'

from antipatterns import SharedPersistency

class Refactoring(object):

    def __init__(self,):
        pass

class MergeMicroservice(Refactoring):

    def __init__(sharedpersistency):
        self.shared_persitency = sharedpersistency
    
    def solution(self):
        