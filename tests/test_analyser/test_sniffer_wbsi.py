from unittest import TestCase

from microfreshener.core.importer import YMLImporter
from microfreshener.core.analyser.sniffer import WobblyServiceInteractionSmellSniffer
from microfreshener.core.analyser.smell import WobblyServiceInteractionSmell
from microfreshener.core.model.groups import Edge


class TestWobblyserviceInteractionSmell(TestCase):

    @classmethod
    def setUpClass(self):
        file = 'data/tests/test_sniffer_wbsi.yml'
        loader = YMLImporter()
        self.micro_model = loader.Import(file)
        self.wbsiSniffer = WobblyServiceInteractionSmellSniffer()

    def test_wbsi(self):
        source = self.micro_model["source"]
        smell = self.wbsiSniffer.snif(source)
        self.assertIsInstance(smell, WobblyServiceInteractionSmell)
        self.assertFalse(smell.isEmpty())
        self.assertEqual(len(smell.getLinkCause()), 1)
        self.assertEqual(smell.getLinkCause()[0].target, self.micro_model["target"])
        
    
    def test_wbsi_with_c(self):
        source = self.micro_model["source_c"]
        smell = self.wbsiSniffer.snif(source)
        self.assertIsInstance(smell, WobblyServiceInteractionSmell)
        self.assertTrue(smell.isEmpty())
        self.assertEqual(len(smell.getLinkCause()), 0)
        self.assertEqual(len(smell.getNodeCause()), 0)
  
    def test_wbsi_with_d(self):
        source = self.micro_model["source_d"]
        smell = self.wbsiSniffer.snif(source)
        self.assertFalse(smell.isEmpty())
        self.assertEqual(len(smell.getLinkCause()), 1)
        self.assertEqual(len(smell.getNodeCause()), 0)
        self.assertEqual(smell.getLinkCause()[0].target, self.micro_model["target"])
    
    def test_wbsi_with_cd(self):
        source = self.micro_model["source_cd"]
        smell = self.wbsiSniffer.snif(source)
        self.assertTrue(smell.isEmpty())
        self.assertEqual(len(smell.getLinkCause()), 0)
        self.assertEqual(len(smell.getNodeCause()), 0)
    
    def test_wbsi_with_t(self):
        source = self.micro_model["source_t"]
        smell = self.wbsiSniffer.snif(source)
        self.assertTrue(smell.isEmpty())
        self.assertEqual(len(smell.getLinkCause()), 0)
        self.assertEqual(len(smell.getNodeCause()), 0)
    
    def test_wbsi_with_tc(self):
        source = self.micro_model["source_tc"]
        smell = self.wbsiSniffer.snif(source)
        self.assertTrue(smell.isEmpty())
        self.assertEqual(len(smell.getLinkCause()), 0)
        self.assertEqual(len(smell.getNodeCause()), 0)

    def test_wbsi_with_td(self):
        source = self.micro_model["source_td"]
        smell = self.wbsiSniffer.snif(source)
        self.assertTrue(smell.isEmpty())
        self.assertEqual(len(smell.getLinkCause()), 0)
        self.assertEqual(len(smell.getNodeCause()), 0)
        
    def test_wbsi_with_tcd(self):    
        source = self.micro_model["source_tcd"]
        smell = self.wbsiSniffer.snif(source)
        self.assertTrue(smell.isEmpty())
        self.assertEqual(len(smell.getLinkCause()), 0)
        self.assertEqual(len(smell.getNodeCause()), 0)
    
    def test_wbsi_to_messagerouter(self):    
        source = self.micro_model["source_mr"]
        smell = self.wbsiSniffer.snif(source)
        self.assertFalse(smell.isEmpty())
        self.assertEqual(len(smell.getLinkCause()), 1)
        self.assertEqual(len(smell.getNodeCause()), 0)
    
    def test_wbsi_to_messagerouter_with_t(self):    
        source = self.micro_model["source_mr_t"]
        smell = self.wbsiSniffer.snif(source)
        self.assertTrue(smell.isEmpty())
        self.assertEqual(len(smell.getLinkCause()), 0)
        self.assertEqual(len(smell.getNodeCause()), 0)
    
    def test_wbsi_to_messagerouter_with_c(self):    
        source = self.micro_model["source_mr_c"]
        smell = self.wbsiSniffer.snif(source)
        self.assertTrue(smell.isEmpty())
        self.assertEqual(len(smell.getLinkCause()), 0)
        self.assertEqual(len(smell.getNodeCause()), 0)

    def test_wbsi_to_messagerouter_with_d(self):    
        source = self.micro_model["source_mr_d"]
        smell = self.wbsiSniffer.snif(source)
        self.assertFalse(smell.isEmpty())
        self.assertEqual(len(smell.getLinkCause()), 1)
        self.assertEqual(len(smell.getNodeCause()), 0)

    def test_wbsi_to_messagerouter_with_tc(self):    
        source = self.micro_model["source_mr_tc"]
        smell = self.wbsiSniffer.snif(source)
        self.assertTrue(smell.isEmpty())
        self.assertEqual(len(smell.getLinkCause()), 0)
        self.assertEqual(len(smell.getNodeCause()), 0)
    
    def test_wbsi_to_messagerouter_with_td(self):    
        source = self.micro_model["source_mr_td"]
        smell = self.wbsiSniffer.snif(source)
        self.assertTrue(smell.isEmpty())
        self.assertEqual(len(smell.getLinkCause()), 0)
        self.assertEqual(len(smell.getNodeCause()), 0)
    
    def test_wbsi_to_messagerouter_with_cd(self):    
        source = self.micro_model["source_mr_cd"]
        smell = self.wbsiSniffer.snif(source)
        self.assertTrue(smell.isEmpty())
        self.assertEqual(len(smell.getLinkCause()), 0)
        self.assertEqual(len(smell.getNodeCause()), 0)
    
    def test_wbsi_to_messagerouter_with_tcd(self):    
        source = self.micro_model["source_mr_tcd"]
        smell = self.wbsiSniffer.snif(source)
        self.assertTrue(smell.isEmpty())
        self.assertEqual(len(smell.getLinkCause()), 0)
        self.assertEqual(len(smell.getNodeCause()), 0)
    
    def test_wbsi_from_message_router_to_service(self):    
        source = self.micro_model["mr"]
        smell = self.wbsiSniffer.snif(source)
        self.assertTrue(smell is None)
        

