from .antipatterns import WrongCutAntipattern, DirectInteractionAntipattern, SharedPersistencyAntipattern,  DeploymentInteractionAntipattern, CascadingFailureAntipattern
from ..model.nodes import Root, Service, Database, CommunicationPattern

PRINCIPLES = INDEPENDENT_DEPLOYABILITY,  HORIZONTAL_SCALABILITY, ISOLATE_FAILURE, DECENTRALISE_EVERYTHING= \
             'IndependentDeployability', 'HorizontalScalability', 'IsolateFailure', 'DecentraliseEverything'

class Principle(object):
    name = "PRINCIPLE"

    def __init__(self, id, name):
        self.name = name
        self.id = id
        self.antipatterns = [ ]  # list of the antipatterns that violates an principle

    def getAntipatterns(self):
        return  self.antipatterns

    def getOccurredAntipatterns(self):
        return [ant for ant in self.antipatterns if not ant.isEmpty()]
    
    def addAntipattern(self,antipattern):
        self.antipatterns.append(antipattern)

    def isEmpty(self):
        return all(antipattern.isEmpty() for antipattern in self.antipatterns)
    
    # def to_dict(self):
    #     return {'name': self.name, 'antipatterns':[i.to_dict() for i in self.getOccurredAntipatterns()]}
        
    # def apply_to(self, node):
    #     # check all the antiappaterrns associated with the principles
    #     for antipattern in self.getAntipatterns():
    #         antipattern.check(node)

    #     return  self

    def __str__(self):
        return self.name
    
    def apply_to(self, node):
        pass

class IndependentDeployabilityPrinciple(Principle):
    name = INDEPENDENT_DEPLOYABILITY

    def __init__(self):
        super(IndependentDeployabilityPrinciple, self).__init__(3, INDEPENDENT_DEPLOYABILITY)
        self.addAntipattern(DeploymentInteractionAntipattern())
    
    def to_dict(self):
        return {'name': self.name, 'antipatterns':[i.to_dict() for i in self.getOccurredAntipatterns()]}

    def apply_to(self, node):
        if (isinstance(node, Service)):
            for antipattern in self.getAntipatterns():
                antipattern.check(node)
                # print(antipattern.getInteractions())
        return self

class HorizontalScalabilityPrinciple(Principle):
    name = HORIZONTAL_SCALABILITY

    def __init__(self):
        super(HorizontalScalabilityPrinciple, self).__init__(4, HORIZONTAL_SCALABILITY)
        self.addAntipattern(DirectInteractionAntipattern(incoming=True))
    
    def to_dict(self):
        return {'name': self.name, 'antipatterns':[i.to_dict() for i in self.getOccurredAntipatterns()]}
        
    def apply_to(self, node):
        if (isinstance(node, Service)):
            for antipattern in self.getAntipatterns():
                antipattern.check(node)
                # print(antipattern.getInteractions())
        return self

class IsolateFailurePrinciple(Principle):
    name = ISOLATE_FAILURE

    def __init__(self):
        super(IsolateFailurePrinciple, self).__init__(5, ISOLATE_FAILURE)
        self.addAntipattern(DirectInteractionAntipattern())

    def to_dict(self):
        return {'name': self.name, 'antipatterns':[i.to_dict() for i in self.getOccurredAntipatterns()]}
        
    def apply_to(self, node):
        if (isinstance(node, Service)):
            for antipattern in self.getAntipatterns():
                antipattern.check(node)
        return self

class DecentraliseEverythingPrinciple(Principle):
    name = DECENTRALISE_EVERYTHING

    def __init__(self):
        super(DecentraliseEverythingPrinciple, self).__init__(2, DECENTRALISE_EVERYTHING)
        self.addAntipattern(SharedPersistencyAntipattern())
    
    def to_dict(self):
        return {'name': self.name, 'antipatterns':[i.to_dict() for i in self.getOccurredAntipatterns()]}

    def apply_to(self, node):
        if (isinstance(node, Database)):
            for antipattern in self.getAntipatterns():
                antipattern.check(node)
                # print(antipattern.getInteractions())
        return self
