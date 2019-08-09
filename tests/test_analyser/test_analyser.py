from unittest import TestCase

from microfreshener.core.importer import YMLImporter
from microfreshener.core.analyser import MicroToscaAnalyser

from microfreshener.core.analyser.sniffer import NoApiGatewaySmellSniffer, WobblyServiceInteractionSmellSniffer, SharedPersistencySmellSniffer, CrossTeamDataManagementSmellSniffer


class TestAnalyser(TestCase):

    @classmethod
    def setUpClass(self):
        file = 'data/examples/hello-world/helloworld.yml'
        loader = YMLImporter()
        self.microtosca = loader.Import(file)

    def test_NoApiGatewaySmellSniffer(self):
        analyser = MicroToscaAnalyser(self.microtosca)
        analyser.add_group_smell_sniffer(
            NoApiGatewaySmellSniffer(self.microtosca))
        res = analyser.run()
        d = res['groups'][0]['smells'][0]['nodes']
        expected = ['order']
        self.assertEqual(d, expected)
    
    def test_WobblyServiceInteractionSniffer(self):
        analyser = MicroToscaAnalyser(self.microtosca)
        analyser.add_node_smell_sniffer(WobblyServiceInteractionSmellSniffer())
        res = analyser.run()
        
        actual_res = res['nodes'][0]['smells'][0]['links']
        expected_res = [{'source': 'order', 'target': 'shipping',  "type": "interaction"}]
        self.assertEqual(actual_res, expected_res)


    def test_SharedPersistencySmellSniffer(self):
        analyser = MicroToscaAnalyser(self.microtosca)
        analyser.add_node_smell_sniffer(SharedPersistencySmellSniffer())
        res = analyser.run()

        d = res['nodes'][0]['smells'][0]['links']
        my_res = [{'source': 'order', 'target': 'order_db',  "type": "interaction"}, {'source': 'shipping', 'target': 'order_db',  "type": "interaction"}]
        self.assertEqual(d, my_res)


    def test_SingleLayerTeamSniffer(self):
        analyser = MicroToscaAnalyser(self.microtosca)
        sltm = CrossTeamDataManagementSmellSniffer(self.microtosca)
        analyser.add_group_smell_sniffer(sltm)
        res = analyser.run()
        actual_res = res['groups'][0]['smells'][0]['links']
        expected_res = [{'source': 'shipping', 'target': 'order_db',  "type": "interaction"}]
        self.assertEqual(actual_res, expected_res)
        self.assertEqual(res['groups'][0]['smells'][0]['nodes'], [])

