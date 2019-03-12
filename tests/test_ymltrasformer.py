from unittest import TestCase

from microanalyser.loader import JSONLoader
from microanalyser.trasformer import YMLTransformer



class TestYMLTranformer(TestCase):

    @classmethod
    def setUpClass(self):
        file = 'data/examples/hello-world-ok.json'
        self.tranformer = YMLTransformer()
        loader = JSONLoader()
        self.microtosca_template = loader.load(file)
        self.microtosca_template.update() 

    def test_number_nodes(self):
        self.tranformer.transform(self.microtosca_template)


