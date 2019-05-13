from unittest import TestCase

from microanalyser.loader import YMLLoader
from microanalyser.model.relationships import RunTimeInteraction, DeploymentTimeInteraction
from microanalyser.analyser.sniffer import EndpointBasedServiceInteractionSmellSniffer, NoApiGatewaySmellSniffer, WobblyServiceInteractionSmellSniffer, SharedPersistencySmellSniffer, SingleLayerTeamSmellSniffer


class TestAnalyser(TestCase):

    @classmethod
    def setUpClass(self):
        file = 'data/examples/helloworld.yml'
        loader = YMLLoader()
        self.micro_model = loader.load(file)

    def test_EndpointBasedServiceInteractionSmell(self):
        shipping = self.micro_model["shipping"]
        ns = EndpointBasedServiceInteractionSmellSniffer()
        smell = ns.snif(shipping)
        self.assertEqual(smell.node, shipping)
        self.assertEqual(len(smell.getLinkCause()), 1)
        self.assertEqual(
            smell.getLinkCause()[0].source, self.micro_model["order"])

    def test_WobblyServiceInteractionSmell(self):
        order = self.micro_model["order"]
        sg = self.micro_model["shipping"]

        ws = WobblyServiceInteractionSmellSniffer()
        smell = ws.snif(order)

        self.assertEqual(smell.isEmpty(), True)
        # TODO: ADd a service node for ahaving a Wobbly service ineraction
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
        self.assertEqual(len(smell.getLinkCause()), 4)
        sources = [
            interaction.source.name for interaction in smell.getLinkCause()]
        self.assertCountEqual(
            sources,  ['shipping', 'order', 'shipping', 'order'])

    # GroupSmellSniffer
    def test_NoApiGatewaySmell(self):
        group = self.micro_model.get_group("edgenodes")
        nags = NoApiGatewaySmellSniffer(self.micro_model)
        smells = nags.snif(group)
        self.assertEqual(len(smells), 1)
        smell = smells[0]
        nodes = [node.name for node in smell.getNodeCause()]
        self.assertCountEqual(nodes, ['order'])

    def test_SingleLayerTeamSmell(self):
        team1 = self.micro_model.get_group("team1")
        sltm = SingleLayerTeamSmellSniffer(self.micro_model)
        smell = sltm.snif(team1)
        links = smell.getLinkCause()
        self.assertEqual(len(links), 2)
        self.assertIsInstance(links[0], RunTimeInteraction)
        self.assertEqual(links[0].source, self.micro_model['shipping'])
        self.assertEqual(links[0].target, self.micro_model['order_db'])
        self.assertIsInstance(links[1], DeploymentTimeInteraction)
        self.assertEqual(links[1].source, self.micro_model['shipping'])
        self.assertEqual(links[1].target, self.micro_model['order_db'])
