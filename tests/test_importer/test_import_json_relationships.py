from unittest import TestCase

from microfreshener.core.importer import JSONImporter

class TestJSONLoaderRelationship(TestCase):

    @classmethod
    def setUpClass(self):
        file = 'data/tests/test_relationship.json'
        self.importer = JSONImporter()
        self.microtosca = self.importer.Import(file)

    def test_relationship_empty_(self):
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
    

    def _load_relationship_from_source_to_target(self, source_name, target_name):
        source = self.microtosca[source_name]
        target = self.microtosca[target_name]
        links_to_target = [link for link in source.run_time if link.target == target]
        self.assertEqual(len(links_to_target), 1)
        return links_to_target[0]

