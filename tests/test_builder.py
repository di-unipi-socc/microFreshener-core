from unittest import TestCase


from microanalyser.loader import YMLLoader
from microanalyser.analyser.builder import AnalyserBuilder
from microanalyser.analyser.smell import WobblyServiceInteractionSmell
from microanalyser.analyser.sniffer import NoApiGatewaySmellSniffer, EndpointBasedServiceInteractionSmellSniffer, WobblyServiceInteractionSmellSniffer, SharedPersistencySmellSniffer, SingleLayerTeamSmellSniffer


class TestAnalyserBUilder(TestCase):

    @classmethod
    def setUpClass(self):
        file = 'data/examples/helloworld.yml'
        loader = YMLLoader()
        self.micro_object = loader.load(file)

    def test_AddSmellSniffer(self):
        builder = AnalyserBuilder(self.micro_object)
        builder.add_smell(4)
        analyser = builder.build()
        sniffers = analyser.get_node_smell_sniffer()
        self.assertEqual(len(sniffers), 1)
        self.assertIsInstance(sniffers[0], WobblyServiceInteractionSmellSniffer)
    
    def test_AddIgnoreSmellForNode(self):
        builder = AnalyserBuilder(self.micro_object)
        order = self.micro_object['order']
        builder.ignore_smell_for_node(order, 4) #WobblyServiceInteractionSmell)
        analyser = builder.build()
        self.assertTrue(len(analyser.get_ignore_smells_for_node(order)),1)
        self.assertIsInstance(analyser.get_ignore_smells_for_node(order)[0], WobblyServiceInteractionSmell)
        
    def test_IgnoredSmellAnalysis(self):
        builder = AnalyserBuilder(self.micro_object)
        shipping = self.micro_object['shipping']
        builder.add_smell(2)
        builder.add_smell(3)
        builder.add_smell(4)
        builder.add_smell(6)
        builder.ignore_smell_for_node(shipping, 3) #EndpointBasedServiceInteractionSmellSniffer)
        analyser = builder.build()
        res = analyser.run()
        self.assertTrue(shipping.name  not in [node['name'] for node in res['nodes']])




