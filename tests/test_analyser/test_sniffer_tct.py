from unittest import TestCase

from microfreshener.core.importer import YMLImporter
from microfreshener.core.analyser.sniffer import TightlyCoupledTeamsSmellSniffer
from microfreshener.core.analyser.smell import TightlyCoupledTeamsSmell

import os

class TestTightlyCoupledTeamsSmell(TestCase):

    @classmethod
    def setUpClass(self):
        file = os.getcwd() + '/data/tests/test_sniffer_tct.yml'
        loader = YMLImporter()
        self.micro_model = loader.Import(file)
        self.tctSniffer = TightlyCoupledTeamsSmellSniffer(self.micro_model)

    def test_tct_simple(self):
        team1 = self.micro_model.get_group("t1t1")
        smell1 = self.tctSniffer.snif(team1)
        self.assertIsInstance(smell1, TightlyCoupledTeamsSmell)
        self.assertFalse(smell1.isEmpty())
        team2 = self.micro_model.get_group("t2t1")
        smell2 = self.tctSniffer.snif(team2)
        self.assertTrue(smell2.isEmpty())

    def test_tct_service_with_db(self):
        team1 = self.micro_model.get_group("t1t2")
        smell1 = self.tctSniffer.snif(team1)
        self.assertIsInstance(smell1, TightlyCoupledTeamsSmell)
        self.assertFalse(smell1.isEmpty())
        team2 = self.micro_model.get_group("t2t2")
        smell2 = self.tctSniffer.snif(team2)
        self.assertTrue(smell2.isEmpty())

    def test_tct_with_mr(self):
        team1 = self.micro_model.get_group("t1t3")
        smell1 = self.tctSniffer.snif(team1)
        self.assertIsInstance(smell1, TightlyCoupledTeamsSmell)
        self.assertFalse(smell1.isEmpty())
        team2 = self.micro_model.get_group("t2t3")
        smell2 = self.tctSniffer.snif(team2)
        self.assertTrue(smell2.isEmpty())

    def test_tct_both(self):
        team1 = self.micro_model.get_group("t1t4")
        smell1 = self.tctSniffer.snif(team1)
        self.assertIsInstance(smell1, TightlyCoupledTeamsSmell)
        self.assertFalse(smell1.isEmpty())
        team2 = self.micro_model.get_group("t2t4")
        smell2 = self.tctSniffer.snif(team2)
        self.assertIsInstance(smell2, TightlyCoupledTeamsSmell)
        self.assertFalse(smell2.isEmpty())

    def test_tct_with_mb_both(self):
        team1 = self.micro_model.get_group("t1t5")
        smell1 = self.tctSniffer.snif(team1)
        self.assertIsInstance(smell1, TightlyCoupledTeamsSmell)
        self.assertFalse(smell1.isEmpty())
        team2 = self.micro_model.get_group("t2t5")
        smell2 = self.tctSniffer.snif(team2)
        self.assertIsInstance(smell2, TightlyCoupledTeamsSmell)
        self.assertFalse(smell2.isEmpty())

    def test_tct_with_mr_both(self):
        team1 = self.micro_model.get_group("t1t6")
        smell1 = self.tctSniffer.snif(team1)
        self.assertIsInstance(smell1, TightlyCoupledTeamsSmell)
        self.assertFalse(smell1.isEmpty())
        team2 = self.micro_model.get_group("t2t6")
        smell2 = self.tctSniffer.snif(team2)
        self.assertIsInstance(smell2, TightlyCoupledTeamsSmell)
        self.assertFalse(smell2.isEmpty())

    def test_tct_with_db_both(self):
        team1 = self.micro_model.get_group("t1t7")
        smell1 = self.tctSniffer.snif(team1)
        self.assertIsInstance(smell1, TightlyCoupledTeamsSmell)
        self.assertFalse(smell1.isEmpty())
        team2 = self.micro_model.get_group("t2t7")
        smell2 = self.tctSniffer.snif(team2)
        self.assertIsInstance(smell2, TightlyCoupledTeamsSmell)
        self.assertFalse(smell2.isEmpty())

    def test_tct_with_db_both(self):
        team1 = self.micro_model.get_group("t1t7")
        smell1 = self.tctSniffer.snif(team1)
        self.assertIsInstance(smell1, TightlyCoupledTeamsSmell)
        self.assertFalse(smell1.isEmpty())
        team2 = self.micro_model.get_group("t2t7")
        smell2 = self.tctSniffer.snif(team2)
        self.assertIsInstance(smell2, TightlyCoupledTeamsSmell)
        self.assertFalse(smell2.isEmpty())

    def test_tct_with_db_both(self):
        team1 = self.micro_model.get_group("tt8")
        smell1 = self.tctSniffer.snif(team1)
        self.assertTrue(smell1.isEmpty())