from unittest import TestCase

from microanalyser.loader import JSONLoader
from microanalyser.trasformer import YMLTransformer



class TestYMLTranformer(TestCase):

    @classmethod
    def setUpClass(self):
        pass
        # file = 'data/examples/helloworld.json' 
        # loader = JSONLoader()
        # microtosca_template = loader.load(file)
        # self.tranformer = YMLTransformer()
        # self.dict_model = self.tranformer.transform(microtosca_template)

    # def test_dictionary_created(self):
    #     self.assertDictEqual(self.dict_model, ntemplate)



