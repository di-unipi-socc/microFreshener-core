from .model.relationships import InteractsWith

class Antipattern(object):

    def _init__(self, name):
        self.name = name 
        self.refactorings = []

class WrongCut(Antipattern):

    def _init__(self, name, squada, squadb, interaction):
        super(Antipattern, self).__init__(name)       
        self.interaction = interaction
        self.squada = squada
        self.squadb = squadb
    
    def refactorings():
        return [ {'id':1, 'name': 'prova1'}{'id': 'name': 'prova2'}]


class SharedPersistency(Antipattern):

    def _init__(self, name, database, nodea, nodeb):
        super(Antipattern, self).__init__(name)       
        self.database = database
        self.nodea = nodea
        self.nodeb = nodeb
    
    def refactorings():
        return [ {'id':1, 'name': 'splitdatabase'}, {'id':1, 'name': 'merge services'}]
    

