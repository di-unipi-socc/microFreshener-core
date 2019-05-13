from unittest import TestCase

from microanalyser.loader import YMLLoader
from microanalyser.analyser.sniffer import EndpointBasedServiceInteractionSmellSniffer


class TestEBSE(TestCase):

    @classmethod
    def setUpClass(self):
        file = 'data/examples/test_sniffer_ebsi.yml'
        loader = YMLLoader()
        self.micro_model = loader.load(file)
        self.ebsiSniffer = EndpointBasedServiceInteractionSmellSniffer()

    def test_no_ebsi_in_source(self):
        source = self.micro_model["source"]
        smell = self.ebsiSniffer.snif(source)
        self.assertTrue(smell.isEmpty())

    def test_yes_ebsi(self):
        target = self.micro_model["target"]
        smell = self.ebsiSniffer.snif(target)
        self.assertFalse(smell.isEmpty())
        self.assertEqual(len(smell.getLinkCause()), 1)
        self.assertEqual(len(smell.getNodeCause()), 0)
        self.assertEqual(smell.getLinkCause()[0].source, self.micro_model["source"])
  
    def test_no_ebsi_with_timeout(self):
        target = self.micro_model["target_t"]
        smell = self.ebsiSniffer.snif(target)
        self.assertTrue(smell.isEmpty())

        target = self.micro_model["target_tc"]
        smell = self.ebsiSniffer.snif(target)
        self.assertTrue(smell.isEmpty())

        target = self.micro_model["target_td"]
        smell = self.ebsiSniffer.snif(target)
        self.assertTrue(smell.isEmpty())

        target = self.micro_model["target_tcd"]
        smell = self.ebsiSniffer.snif(target)
        self.assertTrue(smell.isEmpty())
    
    def test_yes_esbi_with_no_timeout(self):
        target = self.micro_model["target_c"]
        smell = self.ebsiSniffer.snif(target)
        self.assertFalse(smell.isEmpty())

        target = self.micro_model["target_d"]
        smell = self.ebsiSniffer.snif(target)
        self.assertFalse(smell.isEmpty())

        target = self.micro_model["target_cd"]
        smell = self.ebsiSniffer.snif(target)
        self.assertFalse(smell.isEmpty())

    def test_yes_esbi_multi_links(self):
        target = self.micro_model["target_multi"]
        smell = self.ebsiSniffer.snif(target)
        self.assertFalse(smell.isEmpty())
        self.assertEqual(len(smell.getLinkCause()), 2)
        self.assertEqual(len(smell.getNodeCause()), 0)
        self.assertEqual(smell.getLinkCause()[0].source, self.micro_model["source1"])
        self.assertEqual(smell.getLinkCause()[1].source, self.micro_model["source2"])
    
    def test_yes_esbi_composite_links(self):
        target = self.micro_model["target_composite"]
        smell = self.ebsiSniffer.snif(target)
        self.assertFalse(smell.isEmpty())
        self.assertEqual(len(smell.getLinkCause()), 3)
        self.assertEqual(len(smell.getNodeCause()), 0)
        self.assertEqual(smell.getLinkCause()[0].source, self.micro_model["source3"])
        self.assertEqual(smell.getLinkCause()[1].source, self.micro_model["source5"])
        self.assertEqual(smell.getLinkCause()[2].source, self.micro_model["source6"])
    
    def test_no_esbi_at_database_communicatiopattern(self):
        db = self.micro_model["db"]
        cp = self.micro_model["cp"]
        smell = self.ebsiSniffer.snif(db)
        self.assertTrue(smell is None)
        smell = self.ebsiSniffer.snif(cp)
        self.assertTrue(smell is None)

