from unittest import TestCase

from microfreshener.core.importer import YMLImporter
from microfreshener.core.analyser.sniffer import SingleLayerTeamsSmellSniffer
from microfreshener.core.analyser.smell import SingleLayerTeamsSmell
from microfreshener.core.model.groups import Edge


class TestSingleLayerTeamsSmell(TestCase):

    @classmethod
    def setUpClass(self):
        file = 'data/tests/test_sniffer_ctdm.yml'
        loader = YMLImporter()
        self.micro_model = loader.Import(file)
        self.ctdmSniffer = SingleLayerTeamsSmellSniffer(
            self.micro_model)

    def test_ctdm(self):
        team1 = self.micro_model.get_group("team1")
        smell = self.ctdmSniffer.snif(team1)
        self.assertIsInstance(smell, SingleLayerTeamsSmellSmell)
        self.assertFalse(smell.isEmpty())
        self.assertEqual(len(smell.getLinkCause()),  2)

    def test_(self):
        team3 = self.micro_model.get_group("team3")
        smell = self.ctdmSniffer.snif(team3)
        self.assertTrue(smell.isEmpty())
