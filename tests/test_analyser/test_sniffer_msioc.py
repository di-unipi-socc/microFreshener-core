from unittest import TestCase
from microfreshener.core.importer import YMLImporter
from microfreshener.core.analyser.sniffer import MultipleServicesInOneContainerSmellSniffer
from microfreshener.core.analyser.smell import MultipleServicesInOneContainerSmell


class TestEndpointBasedServiceInteraction(TestCase):

    @classmethod
    def setUpClass(self):
        file = 'data/tests/test_sniffer_msioc.yml'
        loader = YMLImporter()
        self.micro_model = loader.Import(file)
        self.msiocSniffer = MultipleServicesInOneContainerSmellSniffer()

    def test_msioc_no_link(self):
        source = self.micro_model["c0"]
        smell = self.msiocSniffer.snif(source)
        self.assertIsInstance(smell, MultipleServicesInOneContainerSmell)
        self.assertTrue(smell.isEmpty())

    def test_msioc_one_link(self):
        source = self.micro_model["c1"]
        smell = self.msiocSniffer.snif(source)
        self.assertIsInstance(smell, MultipleServicesInOneContainerSmell)
        self.assertTrue(smell.isEmpty())

    def test_msioc_two_links(self):
        source = self.micro_model["c23"]
        smell = self.msiocSniffer.snif(source)
        self.assertIsInstance(smell, MultipleServicesInOneContainerSmell)
        self.assertFalse(smell.isEmpty())
        self.assertEqual(len(smell.getLinkCause()), 2)
        src_nodes = list(map(lambda s: s.source, smell.getLinkCause()))
        self.assertEqual(len(src_nodes), 2)
        self.assertTrue(self.micro_model["s2"] in src_nodes)
        self.assertTrue(self.micro_model["s3"] in src_nodes)

    def test_msioc_three_links(self):
        source = self.micro_model["c456"]
        smell = self.msiocSniffer.snif(source)
        self.assertIsInstance(smell, MultipleServicesInOneContainerSmell)
        self.assertFalse(smell.isEmpty())
        self.assertEqual(len(smell.getLinkCause()), 3)
        src_nodes = list(map(lambda s: s.source, smell.getLinkCause()))
        self.assertEqual(len(src_nodes), 3)
        self.assertTrue(self.micro_model["s4"] in src_nodes)
        self.assertTrue(self.micro_model["s5"] in src_nodes)
        self.assertTrue(self.micro_model["s6"] in src_nodes)


