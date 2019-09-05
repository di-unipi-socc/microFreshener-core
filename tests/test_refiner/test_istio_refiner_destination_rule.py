from unittest import TestCase
from microfreshener.core.refiner import IstioRefiner
from microfreshener.core.refiner.istiorefiner import IDestinationRule

import yaml


class TestIstioRefinerLoad(TestCase):

    @classmethod
    def setUpClass(self):
        self.refiner = IstioRefiner(
            'data/tests/refiner/test_load_kingress.yml')
        self.document = """
            apiVersion: networking.istio.io/v1alpha3
            kind: DestinationRule
            metadata:
                name: httpbin
            spec:
                host: httpbin
                trafficPolicy:
                    connectionPool:
                        tcp:
                            maxConnections: 1
                        http:
                            http1MaxPendingRequests: 1
                            maxRequestsPerConnection: 1
                    outlierDetection:
                        consecutiveErrors: 1
                        interval: 1s
                        baseEjectionTime: 3m
                        maxEjectionPercent: 100
            """

    def test_load_destination_rule(self):
        doc = yaml.load(self.document)
        ds = self.refiner._load_destination_rule_object(doc)
        self.assertIsInstance(ds, IDestinationRule)
        self.assertEqual(ds.name, "httpbin")
        self.assertEqual(ds.host, "httpbin")
        self.assertTrue(ds.is_circuit_breaker())
        self.assertFalse(ds.is_load_balancer())
