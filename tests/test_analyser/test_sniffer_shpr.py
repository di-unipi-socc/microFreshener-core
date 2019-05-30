from unittest import TestCase

from microfreshener.core.importer import YMLImporter
from microfreshener.core.analyser.sniffer import SharedPersistencySmellSniffer
from microfreshener.core.analyser.smell import SharedPersistencySmell
from microfreshener.core.model.groups import Edge


class TestWobblyserviceInteractionSmell(TestCase):

    @classmethod
    def setUpClass(self):
        file = 'data/tests/test_sniffer_shpr.yml'
        loader = YMLImporter()
        self.micro_model = loader.Import(file)
        self.shprSniffer = SharedPersistencySmellSniffer()

    def test_shpr(self):
        database = self.micro_model["db"]
        smell = self.shprSniffer.snif(database)
        self.assertIsInstance(smell, SharedPersistencySmell)
        self.assertFalse(smell.isEmpty())
        self.assertEqual(len(smell.getLinkCause()), 3)
        self.assertEqual(len(smell.getNodeCause()), 0)
    
    def test_shpr_database(self):
        database = self.micro_model["db1"]
        smell = self.shprSniffer.snif(database)
        self.assertTrue(smell.isEmpty())
        self.assertEqual(len(smell.getLinkCause()), 0)
        self.assertEqual(len(smell.getNodeCause()), 0)

    def test_shpr_service_to_database(self):
        database = self.micro_model["db2"]
        smell = self.shprSniffer.snif(database)
        self.assertTrue(smell.isEmpty())
