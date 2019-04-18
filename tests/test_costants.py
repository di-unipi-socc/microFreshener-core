from unittest import TestCase

from microanalyser.analyser.constant import INDEPENDENT_DEPLOYABILITY


class TestCostant(TestCase):

    def test_principles_costants(self):
        self.assertEqual(INDEPENDENT_DEPLOYABILITY, "IndependentDeployability")
