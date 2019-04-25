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

    def test_NoApiGatewaySmellSniffer(self):
        analyser = MicroAnalyser(self.micro_object)
        analyser.add_group_smell_sniffer(NoApiGatewaySmellSniffer())
        res = analyser.run()
        d = res['groups'][0]['smells'][0]['cause']
        expected = ['order']
        self.assertEqual(d, expected)

    def test_SharedPersistencySmellSniffer(self):
        analyser = MicroAnalyser(self.micro_object)
        analyser.add_node_smell_sniffer(SharedPersistencySmellSniffer())
        res = analyser.run()
        d = res['nodes'][0]['smells'][0]['cause']
        my_res = [{'source': 'order', 'target': 'order_db', 'type': 'deploymenttime'}, {'source': 'shipping', 'target': 'order_db', 'type': 'deploymenttime'}, {
            'source': 'order', 'target': 'order_db', 'type': 'runtime'}, {'source': 'shipping', 'target': 'order_db', 'type': 'runtime'}]
        self.assertEqual(d, my_res)


    def test_ignored_smell(self):
        analyser = MicroAnalyser(self.micro_object)
        analyser.add_node_smell_sniffer(SharedPersistencySmellSniffer())
