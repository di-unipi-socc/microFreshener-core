from unittest import TestCase

from microfreshener.core.analyser.smell import NoApiGatewaySmell
from microfreshener.core.analyser.sniffer import NoApiGatewaySmellSniffer
from microfreshener.core.model import (Datastore, Edge, MessageBroker,
                                       MessageRouter, MicroToscaModel, Service)


class TestNoApiGatewaySmell(TestCase):

    @classmethod
    def setUpClass(self):
        self.service1 = Service("sr")
        self.service2 = Service("sr2")
        self.datastore = Datastore("db")
        self.msg_router = MessageRouter("mr")
        self.msg_router1 = MessageRouter("mr1")
        self.msg_broker = MessageBroker("mb")

    def test_yes_apgw_with_service(self):
        micro_model = MicroToscaModel("test-noapigateway-smell")
        edge = Edge("edgenodes-service")
        edge.add_member(self.service1)
        micro_model.add_group(edge)

        apgwSniffer = NoApiGatewaySmellSniffer(micro_model)
        smells = apgwSniffer.snif(edge)
        for smell in smells:
            self.assertIsInstance(smell, NoApiGatewaySmell)
        self.assertEqual(len(smells), 1)

    def test_yes_apgw_with_messagebroker(self):
        micro_model = MicroToscaModel("test-noapigateway-smell")
        edge = Edge("edgenodes-msgbroker")
        edge.add_member(self.msg_broker)
        micro_model.add_group(edge)

        apgwSniffer = NoApiGatewaySmellSniffer(micro_model)
        smells = apgwSniffer.snif(edge)
        for smell in smells:
            self.assertIsInstance(smell, NoApiGatewaySmell)
        self.assertEqual(len(smells), 1)

    def test_no_apgw_with_messagerouter(self):
        micro_model = MicroToscaModel("test-noapigateway-smell")
        edge = Edge("edgenodes-msgrouter")
        edge.add_member(self.msg_router)
        micro_model.add_group(edge)

        apgwSniffer = NoApiGatewaySmellSniffer(micro_model)
        smells = apgwSniffer.snif(edge)
        self.assertEqual(len(smells), 0)

    def test_yes_apgw(self):
        micro_model = MicroToscaModel("test-noapigateway-mell")
        edge = Edge("edgenodes")
        edge.add_member(self.service1)
        edge.add_member(self.datastore)
        edge.add_member(self.msg_router)
        edge.add_member(self.msg_broker)

        apgwSniffer = NoApiGatewaySmellSniffer(micro_model)
        micro_model.add_group(edge)
        smells = apgwSniffer.snif(edge)
        for smell in smells:
            self.assertIsInstance(smell, NoApiGatewaySmell)
        self.assertEqual(len(smells), 2)

    def test_yes_apgw2(self):
        micro_model = MicroToscaModel("test-noapigateway-smell")
        edge = Edge("edgenodes-2")
        edge.add_member(self.service1)
        edge.add_member(self.service2)
        edge.add_member(self.msg_router)

        apgwSniffer = NoApiGatewaySmellSniffer(micro_model)
        smells = apgwSniffer.snif(edge)
        for smell in smells:
            self.assertIsInstance(smell, NoApiGatewaySmell)
        self.assertEqual(len(smells), 2)

    def test_no_apgw(self):
        micro_model = MicroToscaModel("microtosca-no-spigwsmwll")
        edge = Edge("edgenodes-nosmell")
        edge.add_member(self.msg_router)
        edge.add_member(self.msg_router1)
        edge.add_member(self.datastore)

        apgwSniffer = NoApiGatewaySmellSniffer(micro_model)
        smells = apgwSniffer.snif(edge)
        self.assertEqual(len(smells), 0)
