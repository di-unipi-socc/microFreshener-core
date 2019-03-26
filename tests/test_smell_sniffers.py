from unittest import TestCase

from microanalyser.loader import YMLLoader
from microanalyser.model.template import MicroModel
from microanalyser.analyser.builder import AnalyserBuilder
from microanalyser.analyser.principles import IndependentDeployabilityPrinciple

from microanalyser.analyser.sniffer import EndpointBasedServiceInteractionSmellSniffer, NoApiGatewaySmellSniffer, WobblyServiceInteractionSmellSniffer, SharedPersistencySmellSniffer

class TestAnalyser(TestCase):

    @classmethod
    def setUpClass(self):
        # file = 'data/examples/helloworld.json'
        # loader = JSONLoader()
        file = 'data/examples/helloworld.yml'
        loader = YMLLoader()
        self.micro_model = loader.load(file)

    def test_EndpointBasedServiceInteractionSmell(self):
        shipping =  self.micro_model.get_node_by_name("shipping")
        ns = EndpointBasedServiceInteractionSmellSniffer()
        smell = ns.snif(shipping)
        self.assertEqual(smell.node, shipping)
        self.assertEqual(len(smell.caused_by), 1)
        self.assertEqual((smell.caused_by[0]).source, self.micro_model.get_node_by_name("order"))
    
    def test_NoApiGatewaySmell(self):
        group =  self.micro_model.get_group("edgenodes")
        napis = NoApiGatewaySmellSniffer()
        smells = napis.snif(group)
        self.assertEqual(len(smells), 1)
        nodes = [smell.node.name for smell in smells]
        self.assertCountEqual(nodes, ['order'])
        
    def test_WobblyServiceInteractionSmell(self):
        order =  self.micro_model.get_node_by_name("order")
        ws = WobblyServiceInteractionSmellSniffer()
        smell = ws.snif(order)
        self.assertEqual(smell.node, order)
        self.assertEqual(len(smell.caused_by), 1)
        self.assertEqual((smell.caused_by[0]).target, self.micro_model.get_node_by_name("shipping"))
    
    def test_SharedPersistencySmell(self):
        orderdb =  self.micro_model.get_node_by_name("order_db")
        ws = SharedPersistencySmellSniffer()
        smell = ws.snif(orderdb)
        self.assertEqual(len(smell.caused_by), 4)
        sources = [interaction.source.name for interaction in smell.caused_by]
        self.assertCountEqual(sources,  ['shipping', 'order', 'shipping', 'order'])
