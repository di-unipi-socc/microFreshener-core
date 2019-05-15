from unittest import TestCase

from microanalyser.importer import YMLImporter
from microanalyser.analyser.sniffer import SharedPersistencySmellSniffer
from microanalyser.model.groups import Edge


class TestWobblyserviceInteractionSmell(TestCase):

    @classmethod
    def setUpClass(self):
        file = 'data/examples/test_sniffer_shpr.yml'
        loader = YMLImporter()
        self.micro_model = loader.Import(file)
        self.shprSniffer = SharedPersistencySmellSniffer()

    def test_shpr(self):
        database = self.micro_model["db"]
        smell = self.shprSniffer.snif(database)
        self.assertFalse(smell.isEmpty())
        self.assertEqual(len(smell.getLinkCause()), 3)
        self.assertEqual(len(smell.getNodeCause()), 0)
    
    def test_shpr_database(self):
        database = self.micro_model["db1"]
        smell = self.shprSniffer.snif(database)
        self.assertTrue(smell.isEmpty())
        self.assertEqual(len(smell.getLinkCause()), 0)
        self.assertEqual(len(smell.getNodeCause()), 0)


        