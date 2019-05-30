from unittest import TestCase

from microfreshener.core.importer.jsonimporter import JSONImporter


class TestJSONLoader(TestCase):

    @classmethod
    def setUpClass(self):
        file = 'data/examples/hello-world/helloworld.json'
        loader = JSONImporter()
        self.microtosca_template = loader.Import(file)

    def test_number_nodes(self):
        self.assertEqual(len(list(self.microtosca_template.nodes)), 5)

    def test_get_node_by_id(self):
        self.assertEqual(self.microtosca_template['shipping'].name, "shipping")

    def test_get_services(self):
        self.assertEqual(len(list(self.microtosca_template.services)), 2)

    def test_node_relationships(self):
        shipping = self.microtosca_template["shipping"]
        rels = [link.target.name for link in shipping.relationships]
        self.assertEqual(rels, ['order_db', 'rabbitmq', 'order_db'])

    def test_node_deploymenttime_relationships(self):
        shipping = self.microtosca_template["shipping"]
        rels = [link.target.name for link in shipping.deployment_time]
        self.assertCountEqual(rels, ['order_db'])
        order = self.microtosca_template["order"]
        rels = [link.target.name for link in order.deployment_time]
        self.assertCountEqual(rels, ['shipping', 'order_db'])

    def test_node_runtime_relationships(self):
        shipping = self.microtosca_template["shipping"]
        rels = [link.target.name for link in shipping.run_time]
        self.assertCountEqual(rels, ['order_db', 'rabbitmq'])
        order = self.microtosca_template["order"]
        rels = [link.target.name for link in order.run_time]
        self.assertCountEqual(rels, ['shipping', 'order_db', 'rabbitmq'])

    def test_node_incoming_links(self):
        shipping = self.microtosca_template["shipping"]
        rels = [link.source.name for link in shipping.incoming]
        self.assertCountEqual(rels, ['order', 'order', 'gateway'])

        order = self.microtosca_template["order"]
        rels = [link.source.name for link in order.incoming]
        self.assertCountEqual(rels, [])

        rabbitmq = self.microtosca_template["rabbitmq"]
        rels = [link.source.name for link in rabbitmq.incoming]
        self.assertCountEqual(rels, ['shipping', 'order'])

        order_db = self.microtosca_template["order_db"]
        rels = [link.source.name for link in order_db.incoming]
        self.assertCountEqual(rels, ['shipping', 'order', 'shipping', 'order'])

    def test_node_incoming_runtime_links(self):
        shipping = self.microtosca_template["shipping"]
        rels = [link.source.name for link in shipping.incoming_run_time]
        self.assertCountEqual(rels, ['order', 'gateway'])

        order = self.microtosca_template["order"]
        rels = [link.source.name for link in order.incoming_run_time]
        self.assertCountEqual(rels, [])

        order_db = self.microtosca_template["order_db"]
        rels = [link.source.name for link in order_db.incoming_run_time]
        self.assertCountEqual(rels, ['shipping', 'order'])

        rabbitmq = self.microtosca_template["rabbitmq"]
        rels = [link.source.name for link in rabbitmq.incoming_run_time]
        self.assertCountEqual(rels, ['shipping', 'order'])

    def test_node_incoming_deployment_links(self):
        shipping = self.microtosca_template["shipping"]
        rels = [link.source.name for link in shipping.incoming_deployment_time]
        self.assertCountEqual(rels, ['order'])

        order = self.microtosca_template["order"]
        rels = [link.source.name for link in order.incoming_deployment_time]
        self.assertCountEqual(rels, [])

        order_db = self.microtosca_template["order_db"]
        rels = [link.source.name for link in order_db.incoming_deployment_time]
        self.assertCountEqual(rels, ['shipping', 'order'])

        rabbitmq = self.microtosca_template["rabbitmq"]
        rels = [link.source.name for link in rabbitmq.incoming_deployment_time]
        self.assertCountEqual(rels, [])

    def test_timedout_relationship(self):
        order = self.microtosca_template["order"]
        shipping = self.microtosca_template["shipping"]
        link_to_shipping = [
            link for link in order.run_time if link.target == shipping]
        self.assertEqual(len(link_to_shipping), 1)
        self.assertTrue(link_to_shipping[0].timeout)

    def test_edge_group(self):
        group = self.microtosca_template.get_group('edgenodes')
        self.assertEqual(group.name, "edgenodes")

        self.assertEqual(self.microtosca_template['shipping'] in group, True)
        self.assertEqual('shipping' in group, True)
        self.assertEqual(self.microtosca_template['rabbitmq'] in group, False)
        self.assertEqual('rabbitmq' in group, False)

        members = [m.name for m in group.members]
        self.assertCountEqual(members, ['shipping', 'order', 'gateway'])

    def test_squad_group(self):
        squad = self.microtosca_template.get_group('team1')
        self.assertEqual(squad.name, "team1")
        self.assertEqual(self.microtosca_template['shipping'] in squad, True)
        self.assertEqual('shipping' in squad, True)
        self.assertEqual(self.microtosca_template['rabbitmq'] in squad, True)
        self.assertEqual('rabbitmq' in squad, True)
        self.assertEqual(self.microtosca_template['order'] in squad, False)
        self.assertEqual('order' in squad, False)
        self.assertCountEqual([m.name for m in squad.members], [
                              'shipping', 'rabbitmq'])

        squad = self.microtosca_template.get_group('team2')
        self.assertEqual(squad.name, "team2")
        self.assertCountEqual([m.name for m in squad.members], [
                              'order', 'order_db'])

