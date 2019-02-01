from .antipatterns import WrongCutAntipattern, DirectInteractionAntipattern, SharedPersistencyAntipattern,  DeploymentInteractionAntipattern, CascadingFailureAntipattern
from ..model.nodes import Root, Service, Database, CommunicationPattern
PROPERTIES = BOUNDED_CONTEXT, DECENTRALIZED_DATA, INDEPENDENTLY_DEPLOYABLE, HORIZZONTALLY_SCALABLE, FAULT_RESILIENCE=\
             'boundedContext', 'decentralizedData', 'independentlyDeployable', 'horizzontallyScalable', 'faultResilience'


class Principle(object):

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
    
class BoundedContextPrinciple(Principle):

    def __init__(self):
        super(BoundedContextPrinciple, self).__init__(1, BOUNDED_CONTEXT)
        self.addAntipattern(WrongCutAntipattern("pepe", "dooa",[]))
    
    def to_dict(self):
        return {'name': self.name, 'antipatterns':[i.to_dict() for i in self.getOccurredAntipatterns()]}

    def occurs(self):
        return self

    def apply_to(self, node):
        if (isinstance(node, Database)):
            for antipattern in self.getAntipatterns():
                antipattern.check(node)
                # print(antipattern.getInteractions())
        return self

class DecentralizedDataPrinciple(Principle):

    def __init__(self):
        super(DecentralizedDataPrinciple, self).__init__(2, DECENTRALIZED_DATA)
        self.addAntipattern(SharedPersistencyAntipattern())
    
    def to_dict(self):
        return {'name': self.name, 'antipatterns':[i.to_dict() for i in self.getOccurredAntipatterns()]}

    def apply_to(self, node):
        if (isinstance(node, Database)):
            for antipattern in self.getAntipatterns():
                antipattern.check(node)
                # print(antipattern.getInteractions())
        return self

class IndependentlyDeployablePrinciple(Principle):

    def __init__(self):
        super(IndependentlyDeployablePrinciple, self).__init__(3, INDEPENDENTLY_DEPLOYABLE)
        self.addAntipattern(DeploymentInteractionAntipattern())
    
    def to_dict(self):
        return {'name': self.name, 'antipatterns':[i.to_dict() for i in self.getOccurredAntipatterns()]}

    def apply_to(self, node):
        if (isinstance(node, Service)):
            for antipattern in self.getAntipatterns():
                antipattern.check(node)
                # print(antipattern.getInteractions())
        return self

class HorizzontallyScalablePrinciple(Principle):

    def __init__(self):
        super(HorizzontallyScalablePrinciple, self).__init__(4, HORIZZONTALLY_SCALABLE)
        self.addAntipattern(DirectInteractionAntipattern())
    
    def to_dict(self):
        return {'name': self.name, 'antipatterns':[i.to_dict() for i in self.getOccurredAntipatterns()]}
        
    def apply_to(self, node):
        if (isinstance(node, Service)):
            for antipattern in self.getAntipatterns():
                antipattern.check(node)
                # print(antipattern.getInteractions())
        return self

class FaultResiliencePrinciple(Principle):

    def __init__(self):
        super(FaultResiliencePrinciple, self).__init__(5, FAULT_RESILIENCE)
        self.addAntipattern(DirectInteractionAntipattern())

    def to_dict(self):
        return {'name': self.name, 'antipatterns':[i.to_dict() for i in self.getOccurredAntipatterns()]}
        
    def apply_to(self, node):
        if (isinstance(node, Service)):
            for antipattern in self.getAntipatterns():
                antipattern.check(node)
        return self

