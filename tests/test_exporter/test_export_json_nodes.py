from unittest import TestCase

from microfreshener.core.importer import JSONImporter, YMLImporter
from microfreshener.core.exporter import JSONExporter
from microfreshener.core.model.type import MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_TIMEOUT_PROPERTY, MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_DYNAMIC_DISCOVEY_PROPERTY,MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_CIRCUIT_BREAKER_PROPERTY

from microfreshener.core.importer.jsontype import JSON_NODE_DATABASE, JSON_NODE_MESSAGE_BROKER, JSON_NODE_MESSAGE_ROUTER, JSON_NODE_SERVICE

class TestJSONTranformer(TestCase):

    @classmethod
    def setUpClass(self):
        file = 'data/tests/test_nodes.json'
        self.importer = JSONImporter()
        self.microtosca = self.importer.Import(file)
        self.tranformer = JSONExporter()

    def test_transform_service(self):
        s1 = self.microtosca['my_service']
        dict_s1 = self.tranformer._transform_node(s1)
        self.assertEqual(dict_s1["type"],JSON_NODE_SERVICE)
        self.assertEqual(dict_s1["name"], "my_service")
    
    def test_transform_database(self):
        db = self.microtosca['my_database']
        dict_db = self.tranformer._transform_node(db)
        self.assertEqual(dict_db["type"],JSON_NODE_DATABASE)
        self.assertEqual(dict_db["name"], "my_database")
    
    def test_transform_messagebroker(self):
        mb = self.microtosca['my_messagebroker']
        dict_mb = self.tranformer._transform_node(mb)
        self.assertEqual(dict_mb["type"],JSON_NODE_MESSAGE_BROKER)
        self.assertEqual(dict_mb["name"], "my_messagebroker")
    
    def test_transform_router(self):
        mr = self.microtosca['my_messagerouter']
        dict_mr = self.tranformer._transform_node(mr)
        self.assertEqual(dict_mr["type"],JSON_NODE_MESSAGE_ROUTER)
        self.assertEqual(dict_mr["name"], "my_messagerouter")