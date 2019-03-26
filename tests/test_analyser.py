from unittest import TestCase

from microanalyser.loader import YMLLoader
from microanalyser.analyser import MicroAnalyser

from microanalyser.analyser.sniffer import NoApiGatewaySmellSniffer, WobblyServiceInteractionSmellSniffer, SharedPersistencySmellSniffer

class TestJSONLoader(TestCase):

    @classmethod
    def setUpClass(self):
        file = 'data/examples/helloworld.yml'
        loader = YMLLoader()
        self.micro_object = loader.load(file)
        # self.analyser = MicroAnalyser(micro_object)
        # self.analyser.add_node_smell_sniffer(SharedPersistencySmellSniffer())
    
    def test_NoApiGatewaySmellSniffer(self):
        analyser = MicroAnalyser(self.micro_object)
        analyser.add_group_smell_sniffer(NoApiGatewaySmellSniffer())
        res = analyser.run()
        r = {'nodes': [], 'groups': [{'name': 'edgenodes', 'smells': [{'name': 'NoApiGateway', 'group': 'edgenodes', 'cause': ['order']}]}]}
        self.assertDictEqual(res,r)
    
    def test_SharedPersistencySmellSniffer(self):
        analyser = MicroAnalyser(self.micro_object)
        analyser.add_node_smell_sniffer(SharedPersistencySmellSniffer())
        res = analyser.run()
        r = {'nodes': [{'name': 'order_db', 'id': 'node_order_db', 'type': 'database', 'smells': [{'name': 'SharedPersistencySmell','cause': [{'source': 'order', 'target': 'order_db', 'type': 'deploymenttime'}, {'source': 'shipping', 'target': 'order_db', 'type': 'deploymenttime'}, {'source': 'order', 'target': 'order_db', 'type': 'runtime'}, {'source': 'shipping', 'target': 'order_db', 'type': 'runtime'}]}]}], 'groups': []}
        self.assertDictEqual(res,r)