from unittest import TestCase

from microanalyser.loader import YMLLoader
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
        shipping = self.micro_model["shipping"]
        ns = EndpointBasedServiceInteractionSmellSniffer()
        smell = ns.snif(shipping)
        self.assertEqual(smell.node, shipping)
        self.assertEqual(len(smell.caused_by), 1)
        self.assertEqual(
            (smell.caused_by[0]).source, self.micro_model["order"])

    def test_WobblyServiceInteractionSmell(self):
        order = self.micro_model["order"]
        sg = self.micro_model["shipping"]

        ws = WobblyServiceInteractionSmellSniffer()
        smell = ws.snif(order)

        # TODO: ADd a service node for ahaving a Wobblye service ineraction
        # the order to shipping interaction now has a timedout interaction
        
        # self.assertEqual(smell.node, order)
        # self.assertEqual(len(smell.caused_by), 1)
        # self.assertEqual(
        #     smell.caused_by[0].source, order)  # self.micro_model["order"])
        # self.assertEqual(
        #     (smell.caused_by[0]).target, self.micro_model["shipping"])

    def test_SharedPersistencySmell(self):
        orderdb = self.micro_model["order_db"]
        ws = SharedPersistencySmellSniffer()
        smell = ws.snif(orderdb)
        self.assertEqual(len(smell.caused_by), 4)
        sources = [interaction.source.name for interaction in smell.caused_by]
        self.assertCountEqual(
            sources,  ['shipping', 'order', 'shipping', 'order'])

    # GroupSmellSniffer
    def test_NoApiGatewaySmell(self):
        group = self.micro_model.get_group("edgenodes")
        napis = NoApiGatewaySmellSniffer()
        smell = napis.snif(group)
        self.assertEqual(len(smell.caused_by), 1)
        nodes = [node.name for node in smell.caused_by]
        self.assertCountEqual(nodes, ['order'])
