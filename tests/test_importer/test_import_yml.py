from unittest import TestCase

from microfreshener.core.importer import YMLImporter 

class TestYMLLoader(TestCase):

    @classmethod
    def setUpClass(self):
        file = 'data/examples/hello-world/helloworld.yml'
        self.importer = YMLImporter()
        self.microtosca = self.importer.Import(file)

    def test_number_nodes(self):
        self.assertEqual(len(list(self.microtosca.nodes)), 5)
        
    def test_get_node_by_name(self):
        self.assertEqual(self.microtosca['shipping'].name, "shipping" )
    
    def test_get_services(self):
        self.assertEqual(len(list(self.microtosca.services)), 2)
    
    def test_node_relationships(self):
        shipping = self.microtosca["shipping"]
        rels = [link.target.name for link in shipping.relationships]       
        self.assertCountEqual(rels, ['order_db', 'rabbitmq', 'order_db'])

    def test_node_deploymenttime_relationships(self):
        shipping = self.microtosca["shipping"]
        rels = [link.target.name for link in shipping.deployment_time]       
        self.assertCountEqual(rels, ['order_db'])
        order = self.microtosca["order"]
        rels = [link.target.name for link in order.deployment_time]       
        self.assertCountEqual(rels, ['shipping','order_db'])
    
    def test_node_runtime_relationships(self):
        shipping = self.microtosca["shipping"]
        rels = [link.target.name for link in shipping.run_time]       
        self.assertCountEqual(rels, ['order_db','rabbitmq'])
        order = self.microtosca["order"]
        rels = [link.target.name for link in order.run_time]       
        self.assertCountEqual(rels, ['shipping','order_db','rabbitmq'])
    
    def test_node_incoming_links(self):
        shipping = self.microtosca["shipping"]
        rels = [link.source.name for link in shipping.incoming]       
        self.assertCountEqual(rels, ['order','order', 'gateway'])
        
        order = self.microtosca["order"]
        rels = [link.source.name for link in order.incoming]       
        self.assertCountEqual(rels, [])
        
        rabbitmq = self.microtosca["rabbitmq"]
        rels = [link.source.name for link in rabbitmq.incoming]       
        self.assertCountEqual(rels, ['shipping','order'])
        
        orderdb = self.microtosca["order_db"]
        rels = [link.source.name for link in orderdb.incoming]       
        self.assertCountEqual(rels, ['shipping','order','shipping','order'])

    def test_node_incoming_runtime_links(self):
        shipping = self.microtosca["shipping"]
        rels = [link.source.name for link in shipping.incoming_run_time]       
        self.assertCountEqual(rels, ['order', 'gateway'])
        
        order = self.microtosca["order"]
        rels = [link.source.name for link in order.incoming_run_time]       
        self.assertCountEqual(rels, [])
        
        orderdb = self.microtosca["order_db"]
        rels = [link.source.name for link in orderdb.incoming_run_time]       
        self.assertCountEqual(rels, ['shipping','order'])
        
        rabbitmq = self.microtosca["rabbitmq"]
        rels = [link.source.name for link in rabbitmq.incoming_run_time]       
        self.assertCountEqual(rels, ['shipping','order'])
    
    def test_node_incoming_deployment_links(self):
        shipping = self.microtosca["shipping"]
        rels = [link.source.name for link in shipping.incoming_deployment_time]       
        self.assertCountEqual(rels, ['order'])
        
        order = self.microtosca["order"]
        rels = [link.source.name for link in order.incoming_deployment_time] 
        self.assertCountEqual(rels, [])
        
        orderdb = self.microtosca["order_db"]
        rels = [link.source.name for link in orderdb.incoming_deployment_time]       
        self.assertCountEqual(rels, ['shipping','order'])
        
        rabbitmq = self.microtosca["rabbitmq"]
        rels = [link.source.name for link in rabbitmq.incoming_deployment_time]       
        self.assertCountEqual(rels, [])
    
    def test_edge_group(self):
        group = self.microtosca.get_group('edgenodes')
        self.assertEqual(group.name, "edgenodes")

        self.assertEqual(self.microtosca['shipping'] in group, True)
        self.assertEqual('shipping' in group, True)
        self.assertEqual(self.microtosca['rabbitmq'] in group, False)
        self.assertEqual('rabbitmq' in group, False)

        members = [m.name for m in group.members]
        self.assertCountEqual(members, ['shipping','order','gateway'])

    def test_squad_group(self):
        squad = self.microtosca.get_group('team1')
        self.assertEqual(squad.name, "team1")
        self.assertEqual(self.microtosca['shipping'] in squad, True)
        self.assertEqual('shipping' in squad, True)
        self.assertEqual(self.microtosca['rabbitmq'] in squad, True)
        self.assertEqual('rabbitmq' in squad, True)
        self.assertEqual(self.microtosca['order'] in squad, False)
        self.assertEqual('order' in squad, False)
        self.assertCountEqual([m.name for m in squad.members], ['shipping','rabbitmq'])

        squad = self.microtosca.get_group('team2')
        self.assertEqual(squad.name, "team2")
        self.assertCountEqual([m.name for m in squad.members], [
                              'order', 'order_db'])






   