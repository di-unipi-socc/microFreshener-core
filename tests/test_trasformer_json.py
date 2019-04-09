from unittest import TestCase

from microanalyser.loader import JSONLoader
from microanalyser.trasformer import JSONTransformer



class TestJSONTranformer(TestCase):

    @classmethod
    def setUpClass(self):
        file = 'data/examples/helloworld.json' 
        loader = JSONLoader()
        self.microtosca_template = loader.load(file)
        self.tranformer = JSONTransformer()
        

    def test_dictionary_groups(self):
        edgeGroup = self.microtosca_template.get_group('edgenodes')
        group_dict = self.tranformer._transform_group(edgeGroup)
        self.assertEqual("name" in group_dict, True)
        self.assertEqual("type" in group_dict, True)
        self.assertEqual("members" in group_dict, True)




