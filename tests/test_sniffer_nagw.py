from unittest import TestCase

from microanalyser.loader import YMLLoader
from microanalyser.analyser.sniffer import NoApiGatewaySmellSniffer
from microanalyser.model.groups import Edge


class TestEBSE(TestCase):

    @classmethod
    def setUpClass(self):
        file = 'data/examples/test_sniffer_nagw.yml'
        loader = YMLLoader()
        self.micro_model = loader.load(file)
        self.apgwSniffer = NoApiGatewaySmellSniffer(self.micro_model)

    def test_yes_apgw(self):
        edge = self.micro_model.get_group("edgenodes")
        self.assertIsInstance(edge, Edge)
        self.assertEqual(len(edge.members), 3)
        smells = self.apgwSniffer.snif(edge)
        self.assertEqual(len(smells), 2)
    
    def test_no_apgw(self):
        edge = self.micro_model.get_group("edgenodes1")
        self.assertIsInstance(edge, Edge)
        self.assertEqual(len(edge.members), 2)
        smells = self.apgwSniffer.snif(edge)
        self.assertEqual(len(smells), 0)
    

   
