from unittest import TestCase

from microfreshener.core.model.type import MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_TIMEOUT_PROPERTY, MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_DYNAMIC_DISCOVEY_PROPERTY, MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_CIRCUIT_BREAKER_PROPERTY
from microfreshener.core.model.microtosca import MicroToscaModel
from microfreshener.core.model.nodes import Service, Database, MessageBroker, MessageRouter
from microfreshener.core.errors import MicroToscaModelError


class TestMicroTosca(TestCase):

    @classmethod
    def setUpClass(self):
        self.name = "prova-model"
        self.microtosca = MicroToscaModel(self.name)
    
    def test_get_node_error(self):
        with self.assertRaises(MicroToscaModelError):        
            self.microtosca['gerNotExistingNode']

    def test_add_service_node(self):
        self.service_name = "s1"
        s = Service(self.service_name)
        self.microtosca.add_node(s)
        self.assertEqual(s, self.microtosca[self.service_name])
    
    def test_add_database_node(self):
        self.db_name = "db"
        db = Service(self.db_name)
        self.microtosca.add_node(db)
        self.assertEqual(db, self.microtosca[self.db_name])