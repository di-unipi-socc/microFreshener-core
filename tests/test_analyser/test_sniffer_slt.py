from unittest import TestCase

from microfreshener.core.importer import YMLImporter
from microfreshener.core.analyser.sniffer import SingleLayerTeamsSmellSniffer
from microfreshener.core.analyser.smell import SingleLayerTeamsSmell

import os

class TestSingleLayerTeamsSmell(TestCase):

    @classmethod
    def setUpClass(self):
        file = os.getcwd() + '/data/tests/test_sniffer_slt.yml'
        loader = YMLImporter()
        self.micro_model = loader.Import(file)
        self.sltSniffer = SingleLayerTeamsSmellSniffer(self.micro_model)

    def test_yes_slt_with_db(self):
        team1 = self.micro_model.get_group("t1t1")
        smell1 = self.sltSniffer.snif(team1)
        self.assertIsInstance(smell1, SingleLayerTeamsSmell)
        self.assertFalse(smell1.isEmpty())
        team2 = self.micro_model.get_group("t2t1")
        smell2 = self.sltSniffer.snif(team2)
        self.assertTrue(smell2.isEmpty())

    def test_yes_slt_with_db_used_by_dbteam(self):
        team1 = self.micro_model.get_group("t1t2")
        smell1 = self.sltSniffer.snif(team1)
        self.assertIsInstance(smell1, SingleLayerTeamsSmell)
        self.assertFalse(smell1.isEmpty())
        team2 = self.micro_model.get_group("t2t2")
        smell2 = self.sltSniffer.snif(team2)
        self.assertTrue(smell2.isEmpty())

    def test_no_slt_with_db_not_in_team(self):
        team = self.micro_model.get_group("tt3")
        smell = self.sltSniffer.snif(team)
        self.assertTrue(smell.isEmpty())

    def test_yes_slt_with_mr_not_internally_linked(self):
        team1 = self.micro_model.get_group("t1t4")
        smell1 = self.sltSniffer.snif(team1)
        self.assertIsInstance(smell1, SingleLayerTeamsSmell)
        self.assertFalse(smell1.isEmpty())
        team2 = self.micro_model.get_group("t2t4")
        smell2 = self.sltSniffer.snif(team2)
        self.assertTrue(smell2.isEmpty())

    def test_yes_slt_with_mb_not_internally_linked(self):
        team1 = self.micro_model.get_group("t1t5")
        smell1 = self.sltSniffer.snif(team1)
        self.assertIsInstance(smell1, SingleLayerTeamsSmell)
        self.assertFalse(smell1.isEmpty())
        team2 = self.micro_model.get_group("t2t5")
        smell2 = self.sltSniffer.snif(team2)
        self.assertTrue(smell2.isEmpty())

    def test_no_slt_with_mr_internally_linked(self):
        team1 = self.micro_model.get_group("t1t6")
        smell1 = self.sltSniffer.snif(team1)
        self.assertTrue(smell1.isEmpty())
        team2 = self.micro_model.get_group("t2t6")
        smell2 = self.sltSniffer.snif(team2)
        self.assertTrue(smell2.isEmpty())

    def test_no_slt_with_mb_internally_linked(self):
        team1 = self.micro_model.get_group("t1t7")
        smell1 = self.sltSniffer.snif(team1)
        self.assertTrue(smell1.isEmpty())
        team2 = self.micro_model.get_group("t2t7")
        smell2 = self.sltSniffer.snif(team2)
        self.assertTrue(smell2.isEmpty())

    def test_yes_slt_with_mr_internally_linked_to_mr(self):
        team1 = self.micro_model.get_group("t1t8")
        smell1 = self.sltSniffer.snif(team1)
        self.assertIsInstance(smell1, SingleLayerTeamsSmell)
        self.assertFalse(smell1.isEmpty())
        team2 = self.micro_model.get_group("t2t8")
        smell2 = self.sltSniffer.snif(team2)
        self.assertTrue(smell2.isEmpty())

    def test_no_slt_with_owned_db(self):
        team1 = self.micro_model.get_group("t1t9")
        smell1 = self.sltSniffer.snif(team1)
        self.assertTrue(smell1.isEmpty())

    def test_no_slt_with_owned_mr(self):
        team1 = self.micro_model.get_group("t1t10")
        smell1 = self.sltSniffer.snif(team1)
        self.assertTrue(smell1.isEmpty())

    def test_no_slt_with_owned_mb(self):
        team1 = self.micro_model.get_group("t1t11")
        smell1 = self.sltSniffer.snif(team1)
        self.assertTrue(smell1.isEmpty())