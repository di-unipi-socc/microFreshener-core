from .model.nodes import Root, Database, Service, CommunicationPattern

class NodeAp():

    def __init__(self, node)
        self._node = node:
        self.antipatterns = {}

    @property
    def wrongCuts():
        if(isinstance(self._node, Service):
            for relationship in self.relationships:
                if(self.is_wrong_cut(relationship)):
                    self.antipatterns['wrongcuts'].append(str(relationship)