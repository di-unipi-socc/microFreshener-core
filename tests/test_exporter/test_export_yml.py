from unittest import TestCase

from microanalyser.importer import YMLImporter
from microanalyser.exporter import YMLExporter


class TestYMLTranformer(TestCase):

    @classmethod
    def setUpClass(self):
        file = 'data/examples/helloworld.yml' 
        loader = YMLImporter()
        self.microtosca = loader.Import(file)
        self.tranformer = YMLExporter()
    
    def test_relationship_format(self):
        pass

    # def test_timedout_relationship(self):
    #     order = self.microtosca["order"]
    #     shipping = self.microtosca["shipping"]
    #     link_to_shipping = [link for link in order.run_time if link.target == shipping] 
    #     rel_dict = self.tranformer._transform_relationship(link_to_shipping[0])
    #     self.assertEqual("run_time" in rel_dict, True)
    #     self.assertEqual(rel_dict["run_time"]["node"], "shipping")


        



