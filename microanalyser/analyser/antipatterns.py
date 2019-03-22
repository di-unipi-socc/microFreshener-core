
ANTIPATTERNS = WRONG_CUT, SHARED_PERSISTENCY, DEPLOYMENT_INTERACTION, DIRECT_INTERACTION, CASCADING_FAILURE =\
        'Wrong Cut', 'Shared Persistency', 'Deployment Interaction', 'Direct Interaction', 'Cascading Failure'

from ..model.nodes import Service, Database, CommunicationPattern
from ..logging import MyLogger
from ..model.template import MicroModel
from ..helper.decorator import visitor
from ..model.nodes import Root


logger = MyLogger().get_logger()

class Antipattern(object):

    def __init__(self):
        self.refactorings = []  # list of the refactorings to resolve the antipattern
        self.interactions = []  # list of the Interactions that cause the antipatterns

    def isEmpty(self):  # check if the antipatterns has some "bad" interactions that cause the antipattern
        return len(self.interactions) == 0

    def getInteractions(self):
        return [interaction.to_dict() for interaction in self.interactions]

    def addRefactoring(self, refactoring):
        self.refactorings.append(refactoring)

    def getRefactorings(self):
        return [refactoring for refactoring in self.refactorings]

    def to_dict(self):
        return {'name': self.name, 'cause': self.getInteractions(), 'refactorings': self.getRefactorings()}

    def visit(self, node):
        pass


class SharedPersistencyAntipattern(Antipattern):
    name = SHARED_PERSISTENCY

    # interactions is a list of interations that cause the shared persistence antipattern
    def __init__(self):
        super(SharedPersistencyAntipattern, self).__init__()
        self.addRefactoring({'name': "merge services"})
        self.addRefactoring({'name': "split database"})
        self.addRefactoring({'name': 'add database manager'})

    @visitor(Database)
    def visit(self, node):
        self.interactions = list(set(node.incoming)) 
        return self.interactions
    
    def isEmpty(self):  # check if the antipatterns has some "bad" interactions that cause the antipattern
        print(self.interactions)
        return len(self.interactions) <= 1

class DeploymentInteractionAntipattern(Antipattern):

    name = DEPLOYMENT_INTERACTION

    def __init__(self):
        super(DeploymentInteractionAntipattern, self).__init__()
        self.addRefactoring({'name': "promote interactions"})
        self.addRefactoring({'name': "remove interaction"})

    def refactorings(self):
        return [{'id': 1, 'name': 'splitdatabase'}, {'id': 1, 'name': 'merge services'}]

    @visitor(Service)
    def visit(self, node):
        logger.debug("{} antipattern on node {}".format(self.name, node))
        self.interactions = [dt_interaction for dt_interaction in node.deployment_time
                                   if (isinstance(dt_interaction.target, Service)
                                       # TODO: check if the targer is derived from the Communication Pattern class
                                       or isinstance(dt_interaction.target, CommunicationPattern))]
        #return  self.interactions if self.interactions else None
        return self.to_dict() if not self.isEmpty() else None

class DirectInteractionAntipattern(Antipattern):

    name = DIRECT_INTERACTION

    def __init__(self):
        super(DirectInteractionAntipattern, self).__init__()
        self.addRefactoring({'name': "add messagge broker"})
        self.addRefactoring({'name': "add circuit braker"})
    
    @visitor(Service)
    def visit(self, node):
        logger.debug("{} antipattern on node {}".format(self.name, node))
        
        self.interactions = [up_rt for up_rt in node.up_run_time_requirements if (
            isinstance(up_rt.source, Service))]
        #return  self.interactions if self.interactions else None
        return self.to_dict() if not self.isEmpty() else None

class CascadingFailureAntipattern(Antipattern):

    name = CASCADING_FAILURE

    def __init__(self):
        super(CascadingFailureAntipattern, self).__init__()
        self.addRefactoring({'name': "Add circuit breaker"})
        self.addRefactoring({'name': "Add message broker"})

    def __str__(self):
        return 'CascadingFailure({})'.format(super(Antipattern, self).__str__())
    
    @visitor(Service)
    def visit(self, node):
        logger.debug("{} antipattern on node {}".format(self.name, node))        
        # TODO: check also if there is a path from the node to a service node without a circuit breaker
        self.interactions = [rt for rt in node.run_time if (isinstance(rt.target, Service))]
        #return self.interactions 
        #return self.to_dict() if not self.isEmpty() else None


class NoApiGatewayAntipattern(Antipattern):
    name = "NoApiGateway"
    
    def __init__(self):
        super(NoApiGatewayAntipattern, self).__init__()
    
    def __str__(self):
        return 'NoApiGateway({})'.format(super(Antipattern, self).__str__())
    
    @visitor(MicroModel)
    def visit(self, micromodel):
        """
        Check if the model has at leat one gateway.
        """
        print("Searching api gateway")
        api_gateways = []
        for cp in micromodel.communicationPatterns:
            if cp.concrete_type == "ApiGateway":
                api_gateways.append(cp)
        # return None if there is some gateways in the architecture (the list of gateways is not empty) 
        # TODO: else return all the Exteranl components that shold be attached by the api gateway.
        #      up to now return all the communication patterns
        return  None if api_gateways else list(micromodel.communicationPatterns)


# Not used antipatterns
class WrongCutAntipattern(Antipattern):
    name = WRONG_CUT

    def __init__(self, squada, squadb, interactions):
        super(WrongCutAntipattern, self).__init__()
        self.squada = squada
        self.squadb = squadb

        self.addRefactoring({'name': "move database"})
        self.addRefactoring({'name': "add database manager"})
        self.addRefactoring({'name': 'move communication'})

    # def wrong_cut(self, node):
    #     interactions = []
    #     for relationship in node.relationships:
    #         source_node = relationship.source
    #         target_node = relationship.target
    #         source_squad = self.micro_model.squad_of(source_node)
    #         target_squad = self.micro_model.squad_of(target_node)
    #         if (isinstance(source_node, Service) and isinstance(target_node, Database)
    #             and source_squad != target_squad):
    #             interactions.append(relationship)    
    #     return interactions
