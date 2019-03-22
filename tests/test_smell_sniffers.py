from unittest import TestCase

from microanalyser.loader.json import JSONLoader
from microanalyser.model.template import MicroModel
from microanalyser.analyser.builder import AnalyserBuilder
from microanalyser.analyser.principles import IndependentDeployabilityPrinciple

from microanalyser.analyser.sniffer import EndpointBasedServiceInteractionSmellSniffer, NoApiGatewaySmellSniffer, WobblyServiceInteractionSmellSniffer, SharedPersistencySmellSniffer

class TestAnalyser(TestCase):

    @classmethod
    def setUpClass(self):
        file = 'data/examples/helloworld.json'
        loader = JSONLoader()
        self.micro_model = loader.load(file)
        #self.analyser = AnalyserBuilder(self.micro_model).add_principle("IndependentDeployability").build()

    def test_EndpointBasedServiceInteractionSmell(self):
        shipping =  self.micro_model.get_node_by_name("shipping")
        ns = EndpointBasedServiceInteractionSmellSniffer()
        smell = ns.snif(shipping)
        self.assertEqual(smell.node, shipping)
        self.assertEqual(len(smell.caused_by), 1)
        self.assertEqual((smell.caused_by[0]).source, self.micro_model.get_node_by_name("order"))
    
    def test_NoApiGatewaySmell(self):
        # TODO. apigateway in not workiong (beacuse it require the gorup of nodes exernals)
        order =  self.micro_model.get_node_by_name("order")
        ag = NoApiGatewaySmellSniffer()
        smell = ag.snif(order)
        self.assertEqual(smell, None)
        
    def test_WobblyServiceInteractionSmell(self):
        order =  self.micro_model.get_node_by_name("order")
        ws = WobblyServiceInteractionSmellSniffer()
        smell = ws.snif(order)
        self.assertEqual(smell.node, order)
        self.assertEqual(len(smell.caused_by), 1)
        self.assertEqual((smell.caused_by[0]).target, self.micro_model.get_node_by_name("shipping"))
    
    def test_SharedPersistencySmell(self):
        orderdb =  self.micro_model.get_node_by_name("orderdb")
        ws = SharedPersistencySmellSniffer()
        smell = ws.snif(orderdb)
        self.assertEqual(len(smell.caused_by), 4)
        sources = [interaction.source.name for interaction in smell.caused_by]
        self.assertEqual(sources,  ['shipping', 'order', 'shipping', 'order'])
