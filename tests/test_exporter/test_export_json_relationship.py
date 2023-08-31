from unittest import TestCase

from microfreshener.core.importer import JSONImporter, YMLImporter
from microfreshener.core.exporter import JSONExporter
from microfreshener.core.model.type import MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_TIMEOUT_PROPERTY, \
    MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_DYNAMIC_DISCOVEY_PROPERTY, \
    MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_CIRCUIT_BREAKER_PROPERTY


class TestJSONTranformerRelationship(TestCase):

    @classmethod
    def setUpClass(self):
        file = 'data/tests/test_relationships.yml'
        self.importer = YMLImporter()
        self.microtosca = self.importer.Import(file)
        self.tranformer = JSONExporter()

    def test_relationship(self):
        rel_dict = self._export_link_to_json_from_source_to_target("my-svc", "my-compute")
        pass

    def _export_link_to_json_from_source_to_target(self, source_name, target_name):
        source = self.microtosca[source_name]
        target = self.microtosca[target_name]
        link_to_target = [
            link for link in source.deployed_on if link.target == target]
        self.assertEqual(len(link_to_target), 1)
        rel_dict = self.tranformer.export_link_to_json(link_to_target[0])
        return rel_dict



