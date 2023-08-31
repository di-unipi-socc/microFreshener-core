from unittest import TestCase

from microfreshener.core.importer import JSONImporter
from microfreshener.core.errors import ImporterError
from microfreshener.core.model.relationships import InteractsWith
from microfreshener.core.model.nodes import Service, Datastore


class TestJSONImporterRelationships(TestCase):

    @classmethod
    def setUpClass(self):
        self.file = 'data/tests/test_relationships.json'
        self.importer = JSONImporter()
        self.json_data = self.importer.load_json(self.file)
        self.importer._load_microtosca(self.json_data)
        self.importer._load_nodes(self.json_data)
       
    # def test_load_node_id_from_json(self):
    #     link = self.json_data['links'][0]
    #     id = load_node_id_from_json(link)

    def test_load_source_node_from_json(self):
        link = self.json_data['links'][0]
        source = self.importer.load_source_node_from_json(link)
        self.assertEqual(source.name, 's1')
        self.assertIsInstance(source, Service)

    def test_load_source_node_from_json_error(self):
        link = self.json_data['links'][1]
        with self.assertRaises(ImporterError):
            self.importer.load_source_node_from_json(link)

    def test_load_target_node_from_json(self):
        json_data = self.importer.load_json(self.file)
        link  =  json_data['links'][0]
        target = self.importer.load_target_node_from_json(link)
        self.assertEqual(target.name, 's2')
        self.assertIsInstance(target, Service)

    def test_load_target_node_from_json_error(self):
        link = self.json_data['links'][1]
        with self.assertRaises(ImporterError):
            self.importer.load_target_node_from_json(link)

    def test_load_interaction_from_json(self):
        link  =  self.json_data['links'][2]
        interaction = self.importer.load_interaction_from_json(link)
        self.assertIsInstance(interaction, InteractsWith)
        self.assertIsInstance(interaction.source, Service)
        self.assertIsInstance(interaction.target, Datastore)

    def test_import_link_from_json(self):
        link  =  self.json_data['links'][3]
        interaction = self.importer.import_link_from_json(link)
        self.assertIsInstance(interaction, InteractsWith)
        self.assertIn(interaction, interaction.source.interactions)
        self.assertIn(interaction, interaction.target.incoming_interactions)