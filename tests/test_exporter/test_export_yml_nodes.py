from unittest import TestCase

from microfreshener.core.importer import YMLImporter
from microfreshener.core.exporter import YMLExporter
from microfreshener.core.model.type import MICROTOSCA_NODES_SERVICE, MICROTOSCA_NODES_DATABASE, MICROTOSCA_NODES_MESSAGE_BROKER, MICROTOSCA_NODES_MESSAGE_ROUTER


class TestYMLTranformer(TestCase):

    @classmethod
    def setUpClass(self):
        file = 'data/tests/test_nodes.yml'
        loader = YMLImporter()
        self.microtosca = loader.Import(file)
        self.tranformer = YMLExporter()

    def test_transform_service(self):
        service = self.microtosca["my_service"]
        dict_service = self.tranformer._transform_node_template(service)
        self.assertEqual(dict_service["type"], MICROTOSCA_NODES_SERVICE)

    def test_transform_database(self):
        db = self.microtosca['my_database']
        dict_db = self.tranformer._transform_node_template(db)
        self.assertEqual(dict_db["type"], MICROTOSCA_NODES_DATABASE)

    def test_transform_messagebroker(self):
        mb = self.microtosca['my_messagebroker']
        dict_mb = self.tranformer._transform_node_template(mb)
        self.assertEqual(dict_mb["type"], MICROTOSCA_NODES_MESSAGE_BROKER)

    def test_transform_router(self):
        mr = self.microtosca['my_messagerouter']
        dict_mr = self.tranformer._transform_node_template(mr)
        self.assertEqual(dict_mr["type"], MICROTOSCA_NODES_MESSAGE_ROUTER)
