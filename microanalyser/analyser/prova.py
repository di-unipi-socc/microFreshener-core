from ..helper.decorator import visitor
from ..model.nodes import Service, Database, CommunicationPattern
from ..model.template import MicroModel
from .antipatterns import WrongCutAntipattern, DirectInteractionAntipattern, SharedPersistencyAntipattern,  DeploymentInteractionAntipattern, CascadingFailureAntipattern


class Prova(object):
    name = "Horizzontally scalable"

    def __init__(self, name):
        self.antipatterns = [DirectInteractionAntipattern()] #, DeploymentInteractionAntipattern(), CascadingFailureAntipattern()]  # list of the antipatterns that violates a principle

    @visitor(Service)
    def visit(self, node):
        res = {'name' : self.name, 'id': node.id}
        antipatterns = []
        for antipattern in self.antipatterns:
            antipatterns.append(antipattern.check(node))
        res['antipatterns'] =  antipatterns
        return res 

    @visitor(Database)
    def visit(self, node):
        res = {'name' : node.name, 'id': node.id}
        res['principles'] =  []
        return res 

    @visitor(CommunicationPattern)
    def visit(self, node):
        res = {'name' : node.name, 'id': node.id}
        res['principles'] =  []
        return res 

class Prova2(object):
    name = "PRINCIPLE"

    def __init__(self, name):
        self.name = name

    @visitor(Service)
    def visit(self, node):
        res = {'name' : node.name, 'id': node.id}
        res['principles'] =  []
        return res 
    
    # @visitor(Database)
    # def visit(self, node):
    #     print("Prova2: Databse")

    # @visitor(CommunicationPattern)
    # def visit(self, node):
    #     print("prova2: Communication pattern")

class GraphProva(object):

    @visitor(MicroModel)
    def visit(self, graph):
        print("Visiting the micro model")
        print("nodes {}".format(len(list(graph.nodes))))

    
