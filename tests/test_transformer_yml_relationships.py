from unittest import TestCase

from microanalyser.loader import YMLLoader
from microanalyser.trasformer import YMLTransformer
from microanalyser.model.type import INTERACT_WITH, RUN_TIME, DEPLOYMENT_TIME
from microanalyser.model.type import INTERACT_WITH_TIMEOUT_PROPERTY, INTERACT_WITH_DYNAMIC_DISCOVEY_PROPERTY,INTERACT_WITH_CIRCUIT_BREAKER_PROPERTY


class TestJSONTranformer(TestCase):

    @classmethod
    def setUpClass(self):
        file = 'data/examples/test_relationship.yml'
        loader = YMLLoader()
        self.microtosca = loader.load(file)
        self.tranformer = YMLTransformer()

    def test_relationship(self):
        rel_dict = self._transform_relationship_from_source_to_target("source", "target")
        self.assertEqual(rel_dict[RUN_TIME], "target")

    def test_relationship_t(self):
        rel_dict = self._transform_relationship_from_source_to_target("source", "target_t")
        self.assertEqual(rel_dict[RUN_TIME]['node'], "target_t")
        self.assertEqual(rel_dict[RUN_TIME]["relationship"], "t")
    
    def test_relationship_c(self):
        rel_dict = self._transform_relationship_from_source_to_target("source", "target_c")
        self.assertEqual(rel_dict[RUN_TIME]['node'], "target_c")
        self.assertEqual(rel_dict[RUN_TIME]["relationship"], "c")
    
    def test_relationship_d(self):
        rel_dict = self._transform_relationship_from_source_to_target("source", "target_d")
        self.assertEqual(rel_dict[RUN_TIME]['node'], "target_d")
        self.assertEqual(rel_dict[RUN_TIME]["relationship"], "d")
    
    def test_relationship_tc(self):
        rel_dict = self._transform_relationship_from_source_to_target("source", "target_tc")
        self.assertEqual(rel_dict[RUN_TIME]['node'], "target_tc")
        self.assertEqual(rel_dict[RUN_TIME]["relationship"], "tc")
    
    def test_relationship_td(self):
        rel_dict = self._transform_relationship_from_source_to_target("source", "target_td")
        self.assertEqual(rel_dict[RUN_TIME]['node'], "target_td")
        self.assertEqual(rel_dict[RUN_TIME]["relationship"], "td")
    
    def test_relationship_cd(self):
        rel_dict = self._transform_relationship_from_source_to_target("source", "target_cd")
        self.assertEqual(rel_dict[RUN_TIME]['node'], "target_cd")
        self.assertEqual(rel_dict[RUN_TIME]["relationship"], "cd")

    
    def test_relationship_tcd(self):
        rel_dict = self._transform_relationship_from_source_to_target("source", "target_tcd")
        self.assertEqual(rel_dict[RUN_TIME]['node'], "target_tcd")
        self.assertEqual(rel_dict[RUN_TIME]["relationship"], "tcd")
    
    def _transform_relationship_from_source_to_target(self, source_name, target_name):
        source = self.microtosca[source_name]
        target = self.microtosca[target_name]
        link_to_target = [
            link for link in source.run_time if link.target == target]
        self.assertEqual(len(link_to_target), 1)
        rel_dict = self.tranformer._transform_relationship(link_to_target[0])
        return rel_dict




