from unittest import TestCase
from microfreshener.core.importer import YMLImporter
from microfreshener.core.analyser.sniffer import EndpointBasedServiceInteractionSmellSniffer
from microfreshener.core.analyser.smell import EndpointBasedServiceInteractionSmell


class TestEBSE(TestCase):

    @classmethod
    def setUpClass(self):
        file = 'data/tests/test_sniffer_ebsi.yml'
        loader = YMLImporter()
        self.micro_model = loader.Import(file)
        self.ebsiSniffer = EndpointBasedServiceInteractionSmellSniffer()

    def test_ebsi_source(self):
        source = self.micro_model["source"]
        smell = self.ebsiSniffer.snif(source)
        self.assertIsInstance(smell, EndpointBasedServiceInteractionSmell)
        self.assertTrue(smell.isEmpty())

    def test_ebsi_target(self):
        target = self.micro_model["target"]
        smell = self.ebsiSniffer.snif(target)
        self.assertFalse(smell.isEmpty())
        self.assertEqual(len(smell.getLinkCause()), 1)
        self.assertEqual(len(smell.getNodeCause()), 0)
        self.assertEqual(smell.getLinkCause()[
                         0].source, self.micro_model["source"])

    def test_ebsi_with_t(self):
        target = self.micro_model["target_t"]
        smell = self.ebsiSniffer.snif(target)
        self.assertFalse(smell.isEmpty())
        self.assertEqual(len(smell.getLinkCause()), 1)
        self.assertEqual(len(smell.getNodeCause()), 0)
        self.assertEqual(smell.getLinkCause()[
                         0].source, self.micro_model["source"])

    def test_ebsi_with_tc(self):
        target = self.micro_model["target_tc"]
        smell = self.ebsiSniffer.snif(target)
        self.assertFalse(smell.isEmpty())
        self.assertEqual(len(smell.getLinkCause()), 1)
        self.assertEqual(len(smell.getNodeCause()), 0)
        self.assertEqual(smell.getLinkCause()[
                         0].source, self.micro_model["source"])

    def test_ebsi_with_td(self):
        target = self.micro_model["target_td"]
        smell = self.ebsiSniffer.snif(target)
        self.assertTrue(smell.isEmpty())

    def test_ebsi_with_tcd(self):
        target = self.micro_model["target_tcd"]
        smell = self.ebsiSniffer.snif(target)
        self.assertTrue(smell.isEmpty())

    def test_esbi_with_c(self):
        target = self.micro_model["target_c"]
        smell = self.ebsiSniffer.snif(target)
        self.assertFalse(smell.isEmpty())
        self.assertEqual(len(smell.getLinkCause()), 1)
        self.assertEqual(len(smell.getNodeCause()), 0)
        self.assertEqual(smell.getLinkCause()[
                         0].source, self.micro_model["source"])

    def test_esbi_with_d(self):
        target = self.micro_model["target_d"]
        smell = self.ebsiSniffer.snif(target)
        self.assertTrue(smell.isEmpty())

    def test_esbi_with_cd(self):
        target = self.micro_model["target_cd"]
        smell = self.ebsiSniffer.snif(target)
        self.assertTrue(smell.isEmpty())

    def test_esbi_with_multi_links(self):
        target = self.micro_model["target_multi"]
        smell = self.ebsiSniffer.snif(target)
        self.assertFalse(smell.isEmpty())
        self.assertEqual(len(smell.getLinkCause()), 2)
        self.assertEqual(len(smell.getNodeCause()), 0)
        self.assertEqual(smell.getLinkCause()[
                         0].source, self.micro_model["source1"])
        self.assertEqual(smell.getLinkCause()[
                         1].source, self.micro_model["source2"])

    def test_esbi_with_composite_links(self):
        target = self.micro_model["target_composite"]
        smell = self.ebsiSniffer.snif(target)
        self.assertFalse(smell.isEmpty())
        self.assertEqual(len(smell.getLinkCause()), 6)
        self.assertEqual(len(smell.getNodeCause()), 0)
        self.assertEqual(smell.getLinkCause()[
                         0].source, self.micro_model["source3"])
        self.assertEqual(smell.getLinkCause()[
                         1].source, self.micro_model["source3"])
        self.assertEqual(smell.getLinkCause()[
                         2].source, self.micro_model["source4"])
        self.assertEqual(smell.getLinkCause()[
                         3].source, self.micro_model["source4"])
        self.assertEqual(smell.getLinkCause()[
                        4].source, self.micro_model["source5"])
        self.assertEqual(smell.getLinkCause()[
                        5].source, self.micro_model["source6"])

    def test_no_esbi_at_database_communicatiopattern(self):
        db = self.micro_model["db"]
        cp = self.micro_model["cp"]
        smell = self.ebsiSniffer.snif(db)
        self.assertTrue(smell is None)
        smell = self.ebsiSniffer.snif(cp)
        self.assertTrue(smell is None)
