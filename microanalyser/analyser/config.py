
class AnalyserConfig(object):

    def __init__(self):
        self.smells = []
        self.ignore_smells_for_node = {}

    def addSmells(self, smell):
        self.smells.appens(smell)

    def getSmells(self):
        return self.smells

    def addIgnoreSmellForNode(self, node, smell):
        if node.name not in self.ignore_smells_for_node.keys:
            self.ignore_smells_for_node[node.name] = [smell]
        else
            self.ignore_smells_for_node[node.name].append(smell)

    def getIgnoreSmellsForNode(self, node):
        return self.ignore_smells_for_node.get(node.name, None)