from unittest import TestCase

from microanalyser.loader import YMLLoader
from microanalyser.trasformer import YMLTransformer



class TestYMLTranformer(TestCase):

    @classmethod
    def setUpClass(self):
        file = 'data/examples/helloworld.yml' 
        loader = YMLLoader()
        self.microtosca_template = loader.load(file)
        self.tranformer = YMLTransformer()
        

    def test_dictionary_created(self):
        yml_string = self.tranformer.transform(self.microtosca_template)
        



