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
        

    def test_timedout_relationship(self):
        order = self.microtosca["order"]
        shipping = self.microtosca["shipping"]
        link_to_shipping = [link for link in order.run_time if link.target == shipping] 
        rel_dict = self.tranformer._transform_relationship(link_to_shipping[0])
        self.assertEqual("target" in rel_dict, True)
        self.assertEqual("source" in rel_dict, True)
        self.assertEqual("timeout" in rel_dict, True)
        self.assertEqual(rel_dict["timeout"], True)


        



