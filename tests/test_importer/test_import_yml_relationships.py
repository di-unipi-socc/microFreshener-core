from unittest import TestCase

from microfreshener.core.importer import YMLImporter
from microfreshener.core.importer.ymltype import YML_RELATIONSHIP_T, YML_RELATIONSHIP_D, YML_RELATIONSHIP_C, YML_RELATIONSHIP_CD, YML_RELATIONSHIP_TC, YML_RELATIONSHIP_TD, YML_RELATIONSHIP_TCD
from microfreshener.core.model.type import MICROTOSCA_RELATIONSHIPS_INTERACT_WITH
from microfreshener.core.model.type import MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_TIMEOUT_PROPERTY, MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_DYNAMIC_DISCOVEY_PROPERTY, MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_CIRCUIT_BREAKER_PROPERTY
from microfreshener.core.errors import ImporterError
class TestYMLLoaderRelationship(TestCase):

    @classmethod
    def setUpClass(self):
        file = 'data/tests/test_relationship.yml'
        self.importer = YMLImporter()
        self.microtosca = self.importer.Import(file)

    def test_relationship_empty(self):
        link = self._load_relationship_from_source_to_target("source", "target")
        self.assertFalse(link.timeout)
        self.assertFalse(link.circuit_breaker)
        self.assertFalse(link.dynamic_discovery)
    
    def test_relationship_t(self):
        link = self._load_relationship_from_source_to_target("source", "target_t")
        self.assertTrue(link.timeout)
        self.assertFalse(link.circuit_breaker)
        self.assertFalse(link.dynamic_discovery)
        
    def test_relationship_c(self):
        link = self._load_relationship_from_source_to_target("source", "target_c")
        self.assertFalse(link.timeout)
        self.assertTrue(link.circuit_breaker)
        self.assertFalse(link.dynamic_discovery)
    
    def test_relationship_d(self):
        link = self._load_relationship_from_source_to_target("source", "target_d")
        self.assertFalse(link.timeout)
        self.assertFalse(link.circuit_breaker)
        self.assertTrue(link.dynamic_discovery)
    
    def test_relationship_tc(self):
        link = self._load_relationship_from_source_to_target("source", "target_tc")
        self.assertTrue(link.timeout)
        self.assertTrue(link.circuit_breaker)
        self.assertFalse(link.dynamic_discovery)
    
    def test_relationship_td(self):
        link = self._load_relationship_from_source_to_target("source", "target_td")
        self.assertTrue(link.timeout)
        self.assertFalse(link.circuit_breaker)
        self.assertTrue(link.dynamic_discovery)
    
    def test_relationship_cd(self):
        link = self._load_relationship_from_source_to_target("source", "target_cd")
        self.assertFalse(link.timeout)
        self.assertTrue(link.circuit_breaker)
        self.assertTrue(link.dynamic_discovery)
    
    def test_relationship_tcd(self):
        link = self._load_relationship_from_source_to_target("source", "target_tcd")
        self.assertTrue(link.timeout)
        self.assertTrue(link.circuit_breaker)
        self.assertTrue(link.dynamic_discovery)

    def test_multiple_relatsionship(self):
        source = self.microtosca["source_same"]
        target = self.microtosca["target_same"]
        links_to_target = [link for link in source.run_time if link.target == target]
        self.assertEqual(len(links_to_target), 8)
        self.assertFalse(links_to_target[0] == links_to_target[1])
        self.assertTrue(links_to_target[0] == links_to_target[0])

    def test_get_relationship_template_t(self):
        rel = self.importer._get_relationship_template_by_name(YML_RELATIONSHIP_T)
        self.assertDictEqual(rel, {"type": MICROTOSCA_RELATIONSHIPS_INTERACT_WITH, "properties": {MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_TIMEOUT_PROPERTY: True}})
 
    def test_get_relationship_template_c(self):
            rel = self.importer._get_relationship_template_by_name(YML_RELATIONSHIP_C)
            self.assertDictEqual(rel, {"type": MICROTOSCA_RELATIONSHIPS_INTERACT_WITH, "properties": {MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_CIRCUIT_BREAKER_PROPERTY: True}})
    
    def test_get_relationship_template_d(self):
            rel = self.importer._get_relationship_template_by_name(YML_RELATIONSHIP_D)
            self.assertDictEqual(rel, {"type": MICROTOSCA_RELATIONSHIPS_INTERACT_WITH, "properties": {MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_DYNAMIC_DISCOVEY_PROPERTY: True}})
    
    def test_get_relationship_template_tc(self):
            rel = self.importer._get_relationship_template_by_name(YML_RELATIONSHIP_TC)
            self.assertDictEqual(rel, {"type": MICROTOSCA_RELATIONSHIPS_INTERACT_WITH, "properties": {MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_TIMEOUT_PROPERTY: True, MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_CIRCUIT_BREAKER_PROPERTY:True}})
    
    def test_get_relationship_template_td(self):
            rel = self.importer._get_relationship_template_by_name(YML_RELATIONSHIP_TD)
            self.assertDictEqual(rel, {"type": MICROTOSCA_RELATIONSHIPS_INTERACT_WITH, "properties": {MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_TIMEOUT_PROPERTY: True, MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_DYNAMIC_DISCOVEY_PROPERTY:True}})
    
    def test_get_relationship_template_cd(self):
            rel = self.importer._get_relationship_template_by_name(YML_RELATIONSHIP_CD)
            self.assertDictEqual(rel, {"type": MICROTOSCA_RELATIONSHIPS_INTERACT_WITH, "properties": {MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_CIRCUIT_BREAKER_PROPERTY: True, MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_DYNAMIC_DISCOVEY_PROPERTY:True}})
    
    def test_get_relationship_template_tcd(self):
            rel = self.importer._get_relationship_template_by_name(YML_RELATIONSHIP_TCD)
            self.assertDictEqual(rel, {"type": MICROTOSCA_RELATIONSHIPS_INTERACT_WITH, "properties": {MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_TIMEOUT_PROPERTY: True, MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_CIRCUIT_BREAKER_PROPERTY: True, MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_DYNAMIC_DISCOVEY_PROPERTY:True}})
    
    def test_get_relationship_template_raise(self):
        with self.assertRaises(ImporterError):
            self.importer._get_relationship_template_by_name("notexist")
 
    def _load_relationship_from_source_to_target(self, source_name, target_name):
        source = self.microtosca[source_name]
        target = self.microtosca[target_name]
        links_to_target = [link for link in source.run_time if link.target == target]
        self.assertEqual(len(links_to_target), 1)
        return links_to_target[0]

    

