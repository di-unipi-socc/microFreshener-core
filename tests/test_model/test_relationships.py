from unittest import TestCase

import uuid
from microfreshener.core.model.type import MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_TIMEOUT_PROPERTY, MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_DYNAMIC_DISCOVEY_PROPERTY, MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_CIRCUIT_BREAKER_PROPERTY
from microfreshener.core.model.microtosca import MicroToscaModel
from microfreshener.core.model.nodes import Service, Datastore, MessageBroker, MessageRouter
from microfreshener.core.errors import MicroToscaModelError, SelfLoopMicroToscaModelError, RelationshipNotFoundError
from microfreshener.core.model.relationships import InteractsWith


class TestModelRelationships(TestCase):

    @classmethod
    def setUpClass(self):
        self.name = "prova-model"
        self.microtosca = MicroToscaModel(self.name)
        self.service_name = "s1"
        self.database_name = "db1"
        self.messagerouter_name = "mr1"
        self.messagebroker_name = "mb1"

        self.microtosca.add_node(Service(self.service_name))
        self.microtosca.add_node(Datastore(self.database_name))
        self.microtosca.add_node(MessageBroker(self.messagebroker_name))
        self.microtosca.add_node(MessageRouter(self.messagerouter_name))

    def test_create_interactWith(self):
        source_node = self.microtosca[self.service_name]
        rel = InteractsWith(source_node, self.microtosca[self.database_name])
        self.assertIsInstance(rel.id, str)
        self.assertEqual(rel.source, source_node)
        self.assertIsInstance(rel.source, Service)
        self.assertIsInstance(rel.target, Datastore)
        self.assertEqual(rel.target, self.microtosca[self.database_name])

    def test_add_interaction_with_interactwith(self):
        source_node = self.microtosca[self.service_name]
        target_node = self.microtosca[self.messagerouter_name]
        interaction = InteractsWith(source_node, target_node)
        source_node.add_interaction(interaction)
        self.assertIn(interaction, source_node.interactions)
        self.assertIn(interaction, target_node.incoming_interactions)

    def test_add_interaction_from_service(self):
        source = self.microtosca[self.service_name]
        target = self.microtosca[self.database_name]
        rel = source.add_interaction(target)
        self.assertEqual(len(source.interactions), 1)
        self.assertIn(rel, source.interactions)
        self.assertIn(rel, target.incoming_interactions)

    def test_add_interaction_from_messagerouter(self):
        source = self.microtosca[self.messagerouter_name]
        target = self.microtosca[self.service_name]
        rel = source.add_interaction(target)
        self.assertEqual(len(source.interactions), 1)
        self.assertIn(rel, source.interactions)
        self.assertIn(rel, target.incoming_interactions)

    def test_get_relationship(self):
        source = self.microtosca[self.messagerouter_name]
        target = self.microtosca[self.database_name]
        rel = source.add_interaction(target)
        expected = self.microtosca.get_relationship(rel.id)
        self.assertEqual(rel, expected)
        self.assertIn(expected, source.interactions)
        self.assertIn(expected, target.incoming_interactions)

    def test_get_relationship_errors(self):
        with self.assertRaises(RelationshipNotFoundError):
            self.microtosca.get_relationship("notexistinglink")

    def test_remove_interacion_from_node(self):
        source = self.microtosca[self.service_name]
        target = self.microtosca[self.messagebroker_name]
        rel = source.add_interaction(target)
        self.assertIn(rel, source.interactions)
        self.assertIn(rel, target.incoming_interactions)
        source.remove_interaction(rel)
        self.assertNotIn(rel, source.interactions)
        self.assertNotIn(rel, target.incoming_interactions)

    def test_remove_incoming_interacion_from_node(self):
        source = self.microtosca[self.service_name]
        target = self.microtosca[self.messagebroker_name]
        rel = source.add_interaction(target)
        self.assertIn(rel, source.interactions)
        self.assertIn(rel, target.incoming_interactions)
        target.remove_incoming_interaction(rel)
        self.assertNotIn(rel, target.incoming_interactions)
        self.assertIn(rel, source.interactions)

    def test_add_interaction_database_error(self):
        # test that Datastore cannot be a source of the interactiwth interaction
        source = self.microtosca[self.database_name]
        with self.assertRaises(MicroToscaModelError):
            target = self.microtosca[self.service_name]
            source.add_interaction(target)
        with self.assertRaises(MicroToscaModelError):
            target = self.microtosca[self.messagebroker_name]
            source.add_interaction(target)
        with self.assertRaises(MicroToscaModelError):
            target = self.microtosca[self.messagerouter_name]
            source.add_interaction(target)

    def test_add_interaction_messagebroker_error(self):
        source = self.microtosca[self.messagebroker_name]
        with self.assertRaises(MicroToscaModelError):
            target = self.microtosca[self.service_name]
            source.add_interaction(target)
        with self.assertRaises(MicroToscaModelError):
            target = self.microtosca[self.messagerouter_name]
            source.add_interaction(target)
        with self.assertRaises(MicroToscaModelError):
            target = self.microtosca[self.database_name]
            source.add_interaction(target)

    def test_add_interaction_selfloop_error(self):
        with self.assertRaises(SelfLoopMicroToscaModelError):
            source = self.microtosca[self.service_name]
            target = self.microtosca[self.service_name]
            source.add_interaction(target)

    def test_change_properties(self):
        s = self.microtosca.add_node(Service("s"))
        t = self.microtosca.add_node(Service("t"))
        link = self.microtosca.add_interaction(s, t)
        self.assertFalse(link.timeout)
        self.assertFalse(link.circuit_breaker)
        self.assertFalse(link.dynamic_discovery)

        link.set_timeout(True)
        link.set_circuit_breaker(True)
        link.set_dynamic_discovery(True)

        self.assertTrue(link.timeout)
        self.assertTrue(link.circuit_breaker)
        self.assertTrue(link.dynamic_discovery)

