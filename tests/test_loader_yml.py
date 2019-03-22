from unittest import TestCase

from microanalyser.loader import YMLLoader 

class TestYMLTrasformer(TestCase):

    @classmethod
    def setUpClass(self):
        file = 'data/examples/helloworld.yml'
        self.loader = YMLLoader()
        self.microtosca = self.loader.load(file)

    def test_number_nodes(self):
        self.assertEqual(len(list(self.microtosca.nodes)), 4)
        
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
        self.assertCountEqual(rels, ['order','order'])
        
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
        self.assertCountEqual(rels, ['order'])
        
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
        self.assertCountEqual(members, ['shipping','order'])