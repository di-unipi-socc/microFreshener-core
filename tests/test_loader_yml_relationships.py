from unittest import TestCase

from microanalyser.loader import YMLLoader

class TestYMLLoaderRelationship(TestCase):

    @classmethod
    def setUpClass(self):
        file = 'data/examples/test_relationship.yml'
        self.loader = YMLLoader()
        self.microtosca = self.loader.load(file)

    def test_relationship_empty_(self):
        source = self.microtosca["source"]
        target = self.microtosca["target"]
        links_to_target = [link for link in source.run_time if link.target == target]
        self.assertEqual(len(links_to_target), 1)
        self.assertFalse(links_to_target[0].timeout)
        self.assertFalse(links_to_target[0].circuit_breaker)
        self.assertFalse(links_to_target[0].dynamic_discovery)
    
    def test_relationship_t(self):
        source = self.microtosca["source"]
        target = self.microtosca["target_t"]
        links_to_target = [link for link in source.run_time if link.target == target]
        self.assertEqual(len(links_to_target), 1)
        self.assertTrue(links_to_target[0].timeout)
        self.assertFalse(links_to_target[0].circuit_breaker)
        self.assertFalse(links_to_target[0].dynamic_discovery)
        
    def test_relationship_c(self):
        source = self.microtosca["source"]
        target = self.microtosca["target_c"]
        links_to_target = [link for link in source.run_time if link.target == target]
        self.assertEqual(len(links_to_target), 1)
        self.assertFalse(links_to_target[0].timeout)
        self.assertTrue(links_to_target[0].circuit_breaker)
        self.assertFalse(links_to_target[0].dynamic_discovery)
    
    def test_relationship_d(self):
        source = self.microtosca["source"]
        target = self.microtosca["target_d"]
        links_to_target = [link for link in source.run_time if link.target == target]
        self.assertEqual(len(links_to_target), 1)
        self.assertFalse(links_to_target[0].timeout)
        self.assertFalse(links_to_target[0].circuit_breaker)
        self.assertTrue(links_to_target[0].dynamic_discovery)
    
    def test_relationship_tc(self):
        source = self.microtosca["source"]
        target = self.microtosca["target_tc"]
        links_to_target = [link for link in source.run_time if link.target == target]
        self.assertEqual(len(links_to_target), 1)
        self.assertTrue(links_to_target[0].timeout)
        self.assertTrue(links_to_target[0].circuit_breaker)
        self.assertFalse(links_to_target[0].dynamic_discovery)
    
    def test_relationship_td(self):
        source = self.microtosca["source"]
        target = self.microtosca["target_td"]
        links_to_target = [link for link in source.run_time if link.target == target]
        self.assertEqual(len(links_to_target), 1)
        self.assertTrue(links_to_target[0].timeout)
        self.assertFalse(links_to_target[0].circuit_breaker)
        self.assertTrue(links_to_target[0].dynamic_discovery)
    
    def test_relationship_cd(self):
        source = self.microtosca["source"]
        target = self.microtosca["target_cd"]
        links_to_target = [link for link in source.run_time if link.target == target]
        self.assertEqual(len(links_to_target), 1)
        self.assertFalse(links_to_target[0].timeout)
        self.assertTrue(links_to_target[0].circuit_breaker)
        self.assertTrue(links_to_target[0].dynamic_discovery)
    
    def test_relationship_tcd(self):
        source = self.microtosca["source"]
        target = self.microtosca["target_tcd"]
        links_to_target = [link for link in source.run_time if link.target == target]
        self.assertEqual(len(links_to_target), 1)
        self.assertTrue(links_to_target[0].timeout)
        self.assertTrue(links_to_target[0].circuit_breaker)
        self.assertTrue(links_to_target[0].dynamic_discovery)
    


