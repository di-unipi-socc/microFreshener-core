from unittest import TestCase

from microfreshener.core.importer import YMLImporter
from microfreshener.core.exporter import YMLExporter
from microfreshener.core.model.type import MICROTOSCA_GROUPS_TEAM, MICROTOSCA_GROUPS_EDGE

class TestYMLTranformer(TestCase):

    @classmethod
    def setUpClass(self):
        file = 'data/tests/test_groups.yml'
        importer = YMLImporter()
        self.microtosca = importer.Import(file)
        self.exporter = YMLExporter()

    def test_export_team1(self):
        t1 = self.microtosca.get_group("team1")
        dteam = self.exporter._transform_group(t1)
        self.assertEqual(dteam["type"], MICROTOSCA_GROUPS_TEAM)
        self.assertEqual(dteam["members"], [ "s1", "mb1"])
    
    def test_export_team2(self):
        t2 = self.microtosca.get_group("team2")
        dteam = self.exporter._transform_group(t2)
        self.assertEqual(dteam["type"], MICROTOSCA_GROUPS_TEAM)
        self.assertEqual(dteam["members"], [ "s2", "mr2", "db2"])

    def test_export_team3(self):
        t3 = self.microtosca.get_group("team3")
        dteam = self.exporter._transform_group(t3)
        self.assertEqual(dteam["type"], MICROTOSCA_GROUPS_TEAM)
        self.assertEqual(dteam["members"], [ "s3", "db3"])

    def test_export_edge(self):
        edge = self.microtosca.get_group("edgenodes")
        dedge = self.exporter._transform_group(edge)
        self.assertEqual(dedge["type"], MICROTOSCA_GROUPS_EDGE)
        self.assertEqual(dedge["members"], [ "s1", "mr2", "s3"])
