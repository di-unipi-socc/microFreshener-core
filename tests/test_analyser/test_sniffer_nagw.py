from unittest import TestCase

from microanalyser.importer import YMLImporter
from microanalyser.analyser.sniffer import NoApiGatewaySmellSniffer
from microanalyser.analyser.smell import NoApiGatewaySmell
from microanalyser.model.groups import Edge


class TestNoApiGatewaySmell(TestCase):

    @classmethod
    def setUpClass(self):
        file = 'data/tests/test_sniffer_nagw.yml'
        loader = YMLImporter()
        self.micro_model = loader.Import(file)
        self.apgwSniffer = NoApiGatewaySmellSniffer(self.micro_model)

    def test_yes_apgw(self):
        edge = self.micro_model.get_group("edgenodes")
        self.assertIsInstance(edge, Edge)
        self.assertEqual(len(edge.members), 3)
        smells = self.apgwSniffer.snif(edge)
        for smell in smells: 
            self.assertIsInstance(smell,NoApiGatewaySmell)
        self.assertEqual(len(smells), 2)

    def test_no_apgw(self):
        edge = self.micro_model.get_group("edgenodes1")
        self.assertIsInstance(edge, Edge)
        self.assertEqual(len(edge.members), 2)
        smells = self.apgwSniffer.snif(edge)
        self.assertEqual(len(smells), 0)
