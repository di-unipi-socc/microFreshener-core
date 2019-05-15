from unittest import TestCase

from microanalyser.importer import YMLImporter
from microanalyser.analyser.sniffer import CrossTeamDataManagementSmellSniffer
from microanalyser.model.groups import Edge


class TestCrossTeamDataManagementSmell(TestCase):

    @classmethod
    def setUpClass(self):
        file = 'data/examples/test_sniffer_ctdm.yml'
        loader = YMLImporter()
        self.micro_model = loader.Import(file)
        self.ctdmSniffer = CrossTeamDataManagementSmellSniffer(
            self.micro_model)

    def test_ctdm(self):
        team1 = self.micro_model.get_group("team1")
        smell = self.ctdmSniffer.snif(team1)
        self.assertFalse(smell.isEmpty())
        self.assertEqual(len(smell.getLinkCause()),  2)

    def test_(self):
        team3 = self.micro_model.get_group("team3")
        smell = self.ctdmSniffer.snif(team3)
        self.assertTrue(smell.isEmpty())
