from unittest import TestCase

from microanalyser.importer import JSONImporter, YMLImporter
from microanalyser.exporter import JSONExporter
from microanalyser.model.type import INTERACT_WITH_TIMEOUT_PROPERTY, INTERACT_WITH_DYNAMIC_DISCOVEY_PROPERTY,INTERACT_WITH_CIRCUIT_BREAKER_PROPERTY


class TestJSONTranformer(TestCase):

    @classmethod
    def setUpClass(self):
        file = 'data/examples/test_nodes.json'
        self.importer = JSONImporter()
        self.microtosca = self.importer.Import(file)
        self.tranformer = JSONExporter()

    def test_transform_service(self):
        s1 = self.microtosca['my_service']
        dict_s1 = self.tranformer._transform_node(s1)
        self.assertEqual(dict_s1["type"],"service")
        self.assertEqual(dict_s1["name"], "my_service")
    
    def test_transform_database(self):
        db = self.microtosca['my_database']
        dict_db = self.tranformer._transform_node(db)
        self.assertEqual(dict_db["type"],"database")
        self.assertEqual(dict_db["name"], "my_database")
    
    def test_transform_messagebroker(self):
        mb = self.microtosca['my_messagebroker']
        dict_mb = self.tranformer._transform_node(mb)
        self.assertEqual(dict_mb["type"],"messagebroker")
        self.assertEqual(dict_mb["name"], "my_messagebroker")
    
    def test_transform_router(self):
        mr = self.microtosca['my_messagerouter']
        dict_mr = self.tranformer._transform_node(mr)
        self.assertEqual(dict_mr["type"],"messagerouter")
        self.assertEqual(dict_mr["name"], "my_messagerouter")