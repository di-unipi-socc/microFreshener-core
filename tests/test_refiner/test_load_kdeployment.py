from unittest import TestCase
from microfreshener.core.refiner import KubernetesRefiner

class TestKubernetesRefiner(TestCase):

    @classmethod
    def setUpClass(self):
        self.refiner = KubernetesRefiner('data/tests/refiner/test_load_kdeployment.yml')

    def test_load_kdeployment(self):
        docs = self.refiner.load_kubernetes_objects()



            