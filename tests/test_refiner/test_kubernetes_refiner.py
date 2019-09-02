from unittest import TestCase
from microfreshener.core.importer import YMLImporter

from microfreshener.core.refiner import KubernetesRefiner
class TestKubernetesRefiner(TestCase):

        @classmethod
        def setUpClass(self):
            self.microtosca = YMLImporter().Import('data/examples/sockshop/sockshop.yml')
            self.refiner = KubernetesRefiner('data/examples/sockshop/ksockshop.yml')
            self.kmicrotosca = self.refiner.Refine(self.microtosca)

        def test_refine_carts(self):  
            carts = self.kmicrotosca['carts']
            kcarts = self.kmicrotosca['kcarts']
            self.assertEqual(len(list(carts.incoming_interactions)), 1)
            self.assertEqual(len(list(kcarts.incoming_interactions)), 2)
            self.assertEqual(len(list(kcarts.interactions)), 1)
            self.assertEqual(kcarts.interactions[0].target, carts)


