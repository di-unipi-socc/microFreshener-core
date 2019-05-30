from unittest import TestCase

from microfreshener.core.importer import JSONImporter, YMLImporter
from microfreshener.core.exporter import JSONExporter

from microfreshener.core.importer.jsontype import JSON_GROUPS_EDGE, JSON_GROUPS_TEAM


class TestJSONTranformer(TestCase):

    @classmethod
    def setUpClass(self):
        file = 'data/examples/hello-world/helloworld.yml'
        self.importer = YMLImporter()
        self.microtosca = self.importer.Import(file)
        self.tranformer = JSONExporter()

    def test_dictionary_groups(self):
        edgeGroup = self.microtosca.get_group('edgenodes')
        group_dict = self.tranformer._transform_group(edgeGroup)
        self.assertEqual("name" in group_dict, True)
        self.assertEqual("type" in group_dict, True)
        self.assertEqual("members" in group_dict, True)

    def test_team1(self): 
        squad =  self.microtosca.get_group("team1")
        squad_dict = self.tranformer._transform_group(squad)
        self.assertEqual(squad_dict['name'], "team1")
        self.assertEqual("type" in squad_dict, True)
        self.assertEqual(squad_dict['type'], JSON_GROUPS_TEAM)

    def test_team2(self):
        squad2 =  self.microtosca.get_group("team2")
        squad_dict = self.tranformer._transform_group(squad2)
        self.assertEqual('name' in squad_dict, True)
        self.assertEqual(squad_dict['name'], "team2")
        self.assertEqual("type" in squad_dict, True)
        self.assertEqual(squad_dict['type'], JSON_GROUPS_TEAM)
      





