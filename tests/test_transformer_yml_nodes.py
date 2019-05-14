from unittest import TestCase

from microanalyser.loader import YMLLoader
from microanalyser.trasformer import YMLTransformer
from microanalyser.model.type import SERVICE, DATABASE, MESSAGE_BROKER, MESSAGE_ROUTER


class TestYMLTranformer(TestCase):

    @classmethod
    def setUpClass(self):
        file = 'data/examples/test_nodes.yml'
        loader = YMLLoader()
        self.microtosca = loader.load(file)
        self.tranformer = YMLTransformer()

    def test_transform_service(self):
        service = self.microtosca["my_service"]
        dict_service = self.tranformer._transform_node_template(service)
        self.assertEqual(dict_service["type"], SERVICE)

    def test_transform_database(self):
        db = self.microtosca['my_database']
        dict_db = self.tranformer._transform_node_template(db)
        self.assertEqual(dict_db["type"], DATABASE)

    def test_transform_messagebroker(self):
        mb = self.microtosca['my_messagebroker']
        dict_mb = self.tranformer._transform_node_template(mb)
        self.assertEqual(dict_mb["type"], MESSAGE_BROKER)

    def test_transform_router(self):
        mr = self.microtosca['my_messagerouter']
        dict_mr = self.tranformer._transform_node_template(mr)
        self.assertEqual(dict_mr["type"], MESSAGE_ROUTER)
