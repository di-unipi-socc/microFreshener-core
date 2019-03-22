from unittest import TestCase

from microanalyser.loader.json import JSONLoader

class TestJSONLoader(TestCase):

    @classmethod
    def setUpClass(self):
        file = 'data/examples/helloworld.json'
        loader = JSONLoader()
        self.microtosca_template = loader.load(file)

    def test_number_nodes(self):
        self.assertEqual(len(list(self.microtosca_template.nodes)), 4)
    
    def test_get_node_by_id(self):
        self.assertEqual(self.microtosca_template['0d8d8e1e-82d5-4571-9718-632cc0d7c99e'].name, "shipping" )

    def test_get_services(self):
        self.assertEqual(len(list(self.microtosca_template.services)), 2)

    def test_node_relationships(self):
        shipping = self.microtosca_template.get_node_by_name("shipping")
        rels = [link.target.name for link in shipping.relationships]       
        self.assertEqual(rels, ['orderdb', 'rabbitmq', 'orderdb'])

    def test_node_deploymenttime_relationships(self):
        shipping = self.microtosca_template.get_node_by_name("shipping")
        rels = [link.target.name for link in shipping.deployment_time]       
        self.assertCountEqual(rels, ['orderdb'])
        order = self.microtosca_template.get_node_by_name("order")
        rels = [link.target.name for link in order.deployment_time]       
        self.assertCountEqual(rels, ['shipping','orderdb'])
                  
    def test_node_runtime_relationships(self):
        shipping = self.microtosca_template.get_node_by_name("shipping")
        rels = [link.target.name for link in shipping.run_time]       
        self.assertCountEqual(rels, ['orderdb','rabbitmq'])
        order = self.microtosca_template.get_node_by_name("order")
        rels = [link.target.name for link in order.run_time]       
        self.assertCountEqual(rels, ['shipping','orderdb','rabbitmq'])
    
    def test_node_incoming_links(self):
        shipping = self.microtosca_template.get_node_by_name("shipping")
        rels = [link.source.name for link in shipping.incoming]       
        self.assertCountEqual(rels, ['order','order'])
        
        order = self.microtosca_template.get_node_by_name("order")
        rels = [link.source.name for link in order.incoming]       
        self.assertCountEqual(rels, [])
        
        rabbitmq = self.microtosca_template.get_node_by_name("rabbitmq")
        rels = [link.source.name for link in rabbitmq.incoming]       
        self.assertCountEqual(rels, ['shipping','order'])
        
        orderdb = self.microtosca_template.get_node_by_name("orderdb")
        rels = [link.source.name for link in orderdb.incoming]       
        self.assertCountEqual(rels, ['shipping','order','shipping','order'])

    def test_node_incoming_runtime_links(self):
        shipping = self.microtosca_template.get_node_by_name("shipping")
        rels = [link.source.name for link in shipping.incoming_run_time]       
        self.assertCountEqual(rels, ['order'])
        
        order = self.microtosca_template.get_node_by_name("order")
        rels = [link.source.name for link in order.incoming_run_time]       
        self.assertCountEqual(rels, [])
        
        orderdb = self.microtosca_template.get_node_by_name("orderdb")
        rels = [link.source.name for link in orderdb.incoming_run_time]       
        self.assertCountEqual(rels, ['shipping','order'])
        
        rabbitmq = self.microtosca_template.get_node_by_name("rabbitmq")
        rels = [link.source.name for link in rabbitmq.incoming_run_time]       
        self.assertCountEqual(rels, ['shipping','order'])

    def test_node_incoming_deployment_links(self):
        shipping = self.microtosca_template.get_node_by_name("shipping")
        rels = [link.source.name for link in shipping.incoming_deployment_time]       
        self.assertCountEqual(rels, ['order'])
        
        order = self.microtosca_template.get_node_by_name("order")
        rels = [link.source.name for link in order.incoming_deployment_time] 
        self.assertCountEqual(rels, [])
        
        orderdb = self.microtosca_template.get_node_by_name("orderdb")
        rels = [link.source.name for link in orderdb.incoming_deployment_time]       
        self.assertCountEqual(rels, ['shipping','order'])
        
        rabbitmq = self.microtosca_template.get_node_by_name("rabbitmq")
        rels = [link.source.name for link in rabbitmq.incoming_deployment_time]       
        self.assertCountEqual(rels, [])
