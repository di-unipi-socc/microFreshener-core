from unittest import TestCase

from microfreshener.core.importer import YMLImporter
from microfreshener.core.analyser.sniffer import SharedBoundedContextSmellSniffer
from microfreshener.core.analyser.smell import SharedBoundedContextSmell

import os

class TestSharedBoundedContextSmell(TestCase):

    @classmethod
    def setUpClass(self):
        file = os.getcwd() + '/data/tests/test_sniffer_sbc.yml'
        loader = YMLImporter()
        self.micro_model = loader.Import(file)
        self.sbcSniffer = SharedBoundedContextSmellSniffer(self.micro_model)

    def test_yes_sbc(self):
        team1 = self.micro_model.get_group("t1t1")
        smell1 = self.sbcSniffer.snif(team1)
        self.assertIsInstance(smell1, SharedBoundedContextSmell)
        self.assertFalse(smell1.isEmpty())
        team2 = self.micro_model.get_group("t2t1")
        smell2 = self.sbcSniffer.snif(team2)
        self.assertIsInstance(smell2, SharedBoundedContextSmell)
        self.assertFalse(smell2.isEmpty())

    def test_yes_sbc_with_external_service(self):
        team1 = self.micro_model.get_group("t1t2")
        smell1 = self.sbcSniffer.snif(team1)
        self.assertIsInstance(smell1, SharedBoundedContextSmell)
        self.assertFalse(smell1.isEmpty())
        team2 = self.micro_model.get_group("t2t2")
        smell2 = self.sbcSniffer.snif(team2)
        self.assertIsInstance(smell2, SharedBoundedContextSmell)
        self.assertFalse(smell2.isEmpty())

    def test_yes_sbc_if_no_other_db_user(self):
        team1 = self.micro_model.get_group("t1t3")
        smell1 = self.sbcSniffer.snif(team1)
        self.assertIsInstance(smell1, SharedBoundedContextSmell)
        self.assertFalse(smell1.isEmpty())
        team2 = self.micro_model.get_group("t2t3")
        smell2 = self.sbcSniffer.snif(team2)
        self.assertIsInstance(smell2, SharedBoundedContextSmell)
        self.assertFalse(smell2.isEmpty())

    def test_yes_sbc_db_without_team(self):
        team1 = self.micro_model.get_group("t1t4")
        smell1 = self.sbcSniffer.snif(team1)
        self.assertIsInstance(smell1, SharedBoundedContextSmell)
        self.assertFalse(smell1.isEmpty())
        team2 = self.micro_model.get_group("t2t4")
        smell2 = self.sbcSniffer.snif(team2)
        self.assertIsInstance(smell2, SharedBoundedContextSmell)
        self.assertFalse(smell2.isEmpty())

    def test_no_sbc_same_team(self):
        team1 = self.micro_model.get_group("tt5")
        smell1 = self.sbcSniffer.snif(team1)
        self.assertTrue(smell1.isEmpty())
