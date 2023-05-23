from unittest import TestCase

from microfreshener.core.importer import YMLImporter
from microfreshener.core.model import Compute


class TestYMLImporterRelationships(TestCase):

    @classmethod
    def setUpClass(self):
        file = 'data/tests/test_relationships.yml'
        self.importer = YMLImporter()
        self.microtosca = self.importer.Import(file)

    def test_number_nodes(self):
        self.assertEqual(len(list(self.microtosca.nodes)), 2)

    def test_deployed_on_present(self):
        self.assertTrue(len(self.microtosca["my-svc"].deployed_on), 1)

    def test_compute_source(self):
        self.assertTrue(isinstance(self.microtosca["my-svc"].deployed_on[0].target, Compute))

