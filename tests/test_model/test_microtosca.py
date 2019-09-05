from unittest import TestCase

from microfreshener.core.model.type import MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_TIMEOUT_PROPERTY, MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_DYNAMIC_DISCOVEY_PROPERTY, MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_CIRCUIT_BREAKER_PROPERTY
from microfreshener.core.model.microtosca import MicroToscaModel
from microfreshener.core.model.nodes import Service, Datastore, MessageBroker, MessageRouter
from microfreshener.core.errors import MicroToscaModelError, GroupNotFoundError
from microfreshener.core.model import Team


class TestMicroTosca(TestCase):

    @classmethod
    def setUpClass(self):
        self.name = "prova-model"
        self.microtosca = MicroToscaModel(self.name)
        self.service_name = "s1"
        self.db_name = "db"
        self.mr_name = "message_router"
        self.mb_name = "message_broker"

    def test_add_service_node(self):
        s = Service(self.service_name)
        self.microtosca.add_node(s)
        self.assertTrue(s in self.microtosca)
        self.assertEqual(s, self.microtosca[self.service_name])
        self.assertIsInstance(self.microtosca[self.service_name], Service)
        self.assertIn(s, self.microtosca.services)

    def test_add_database_node(self):
        db = Datastore(self.db_name)
        self.microtosca.add_node(db)
        self.assertTrue(db in self.microtosca)
        self.assertEqual(db, self.microtosca[self.db_name])
        self.assertIsInstance(self.microtosca[self.db_name], Datastore)
        self.assertIn(db, self.microtosca.datastores)

    def test_add_mb_node(self):
        mb = MessageBroker(self.mb_name)
        self.microtosca.add_node(mb)
        self.assertTrue(mb in self.microtosca)
        self.assertEqual(mb, self.microtosca[self.mb_name])
        self.assertIsInstance(self.microtosca[self.mb_name], MessageBroker)
        self.assertIn(mb, self.microtosca.communication_patterns)
        self.assertIn(mb, self.microtosca.message_brokers)

    def test_add_mr_node(self):
        mr = MessageRouter(self.mr_name)
        self.microtosca.add_node(mr)
        self.assertTrue(mr in self.microtosca)
        self.assertEqual(mr, self.microtosca[self.mr_name])
        self.assertIsInstance(self.microtosca[self.mr_name], MessageRouter)
        self.assertIn(mr, self.microtosca.communication_patterns)
        self.assertIn(mr, self.microtosca.message_routers)

    def test_get_node(self):
        self.assertEqual(
            self.microtosca[self.service_name].name, self.service_name)
        self.assertIsInstance(self.microtosca[self.service_name], Service)
        self.assertEqual(self.microtosca[self.db_name].name, self.db_name)
        self.assertIsInstance(self.microtosca[self.db_name], Datastore)
        self.assertEqual(self.microtosca[self.mb_name].name, self.mb_name)
        self.assertIsInstance(self.microtosca[self.mb_name], MessageBroker)
        self.assertEqual(self.microtosca[self.mr_name].name, self.mr_name)
        self.assertIsInstance(self.microtosca[self.mr_name], MessageRouter)

    def test_get_node_error(self):
        with self.assertRaises(MicroToscaModelError):
            self.microtosca['getNotExistingNode']

    def test_add_interaction(self):
        nodo1 = self.microtosca.add_node(Service("inter1"))
        nodo2 = self.microtosca.add_node(Service("inter2"))
        rel = self.microtosca.add_interaction(nodo1, nodo2)
        self.assertIn(rel, nodo1.interactions)
        self.assertIn(rel, nodo2.incoming_interactions)

    def test_add_relationship(self):
        rel = self._add_relationship("servizio1", "servizio2")
        self.assertIsInstance(rel.source, Service)
        self.assertIsInstance(rel.target, Service)
        self.assertIn(rel, self.microtosca["servizio1"].interactions)
        self.assertIn(rel, self.microtosca["servizio2"].incoming_interactions)

    def test_get_relationship(self):
        rel = self._add_relationship("servizio3", "servizio4")
        exp_rel = self.microtosca.get_relationship(rel.id)
        self.assertEqual(rel, exp_rel)
        self.assertEqual(rel.source, exp_rel.source)
        self.assertEqual(rel.target, exp_rel.target)

    def test_remove_relationship(self):
        rel = self._add_relationship("servizio5", "servizio6")
        self.microtosca.delete_relationship(rel)
        self.assertNotIn(rel, self.microtosca["servizio5"].interactions)
        self.assertNotIn(
            rel, self.microtosca["servizio6"].incoming_interactions)

    def _add_relationship(self, source_name, target_name):
        s = self.microtosca.add_node(Service(source_name))
        t = self.microtosca.add_node(Service(target_name))
        return s.add_interaction(t)

    def test_delete_node(self):
        nodo = self.microtosca.add_node(Service("prova"))
        self.assertIn(nodo, self.microtosca.services)
        self.microtosca.delete_node(nodo)
        self.assertNotIn(nodo, self.microtosca.services)

    def test_delete_node_remove_interactions(self):
        first = self.microtosca.add_node(Service("first"))
        second = self.microtosca.add_node(Service("second"))
        third = self.microtosca.add_node(Service("third"))
        first_second = first.add_interaction(second)
        second_third = second.add_interaction(third)
        first_third = first.add_interaction(third)
        self.microtosca.delete_node(second)
        self.assertNotIn(second, self.microtosca.nodes)
        self.assertNotIn(first_second, second.incoming_interactions)
        self.assertNotIn(second_third, third.incoming_interactions)
        self.assertIn(first_third, third.incoming_interactions)
        self.assertIn(first_third, first.interactions)

    def test_get_subgraph_from_nodes(self):
        first = self.microtosca.add_node(Service("one"))
        second = self.microtosca.add_node(Service("two"))
        third = self.microtosca.add_node(Service("third"))
        team_name = "prova-subgraph"
        team = Team(team_name)
        team.add_member(first)
        self.microtosca.add_group(team)

        first = self.microtosca.add_node(first)
        second = self.microtosca.add_node(second)
        third = self.microtosca.add_node(third)

        first_to_second = first.add_interaction(second)
        third_to_second = third.add_interaction(second)

        subgraph = self.microtosca.get_subgraph([first, second, third])

        self.assertEqual(len(list(subgraph.nodes)), 3)
        self.assertCountEqual(list(subgraph.nodes), [first, second, third])

        self.assertIn(first_to_second, subgraph['one'].interactions)
        self.assertIn(first_to_second, subgraph['two'].incoming_interactions)
        self.assertEqual(2, len(subgraph['two'].incoming_interactions))

        self.assertIn(first, subgraph.get_group(team_name).members)
        self.assertEqual(len(list(subgraph.get_group(team_name).members)), 1)

    def test_relink_incoming(self):
        s1 = self.microtosca.add_node(Service("s1"))
        s2 = self.microtosca.add_node(Service("s2"))
        s3 = self.microtosca.add_node(Service("s3"))

        current = self.microtosca.add_node(Service("current"))
        new = self.microtosca.add_node(Service("new_node"))

        s1.add_interaction(current)
        s2.add_interaction(current)
        s3.add_interaction(current)

        self.assertEqual(len(list(current.incoming_interactions)), 3)

        self.microtosca.relink_incoming(current, new)

        self.assertEqual(len(list(current.incoming_interactions)), 0)
        self.assertEqual(len(list(new.incoming_interactions)), 3)
        self.assertCountEqual(
            [rel.source for rel in new.incoming_interactions], [s1, s2, s3])

    def test_relink_incoming_with_discard(self):
        s1 = self.microtosca.add_node(Service("s1"))
        s2 = self.microtosca.add_node(Service("s2"))
        s3 = self.microtosca.add_node(Service("s3"))
        discard = self.microtosca.add_node(Service("discard"))

        current = self.microtosca.add_node(Service("cuurent"))
        new = self.microtosca.add_node(Service("new_node"))

        s1.add_interaction(current)
        s2.add_interaction(current)
        s3.add_interaction(current)
        discard.add_interaction(current)

        self.assertEqual(len(list(current.incoming_interactions)), 4)

        self.microtosca.relink_incoming(current, new, [discard])

        self.assertEqual(len(list(new.incoming_interactions)), 3)
        self.assertCountEqual(
            [rel.source for rel in new.incoming_interactions], [s1, s2, s3])
        self.assertNotIn(
            discard, [rel.source for rel in new.incoming_interactions])

        self.assertEqual(len(list(current.incoming_interactions)), 1)
        self.assertCountEqual(
            [rel.source for rel in current.incoming_interactions], [discard])
        self.assertNotIn(
            s1, [rel.source for rel in current.incoming_interactions])
        self.assertNotIn(
            s2, [rel.source for rel in current.incoming_interactions])
        self.assertNotIn(
            s3, [rel.source for rel in current.incoming_interactions])
