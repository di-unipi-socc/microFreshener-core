from unittest import TestCase

from microfreshener.core.importer import YMLImporter
from microfreshener.core.model import Service, Datastore, CommunicationPattern, MessageBroker, MessageRouter, KIngress, KProxy, KService

class TestYMLImporterNodes(TestCase):

    @classmethod
    def setUpClass(self):
        file = 'data/tests/test_nodes.yml'
        self.importer = YMLImporter()
        self.microtosca = self.importer.Import(file)

    def test_service(self):
        s1 = self.microtosca['my_service']
        self.assertIsInstance(s1, Service)
        self.assertEqual(s1.name, "my_service")
    
    def test_database(self):
        db = self.microtosca['my_datastore']
        self.assertIsInstance(db, Datastore)
        self.assertEqual(db.name, "my_datastore")
    
    def test_messagebroker(self):
        mb = self.microtosca['my_messagebroker']
        self.assertIsInstance(mb, MessageBroker)
        self.assertEqual(mb.name, "my_messagebroker")
    
    def test_messagerouter(self):
        mr = self.microtosca['my_messagerouter']
        self.assertIsInstance(mr, MessageRouter)
        self.assertEqual(mr.name, "my_messagerouter")
        self.assertEqual(mr.label, "MR")
    
    def test_kservice(self):
        mr = self.microtosca['my_kservice']
        self.assertIsInstance(mr, KService)
        self.assertEqual(mr.name, "my_kservice")
    
    def test_kproxy(self):
        mr = self.microtosca['my_kproxy']
        self.assertIsInstance(mr, KProxy)
        self.assertEqual(mr.name, "my_kproxy")
    
    def test_kingress(self):
        mr = self.microtosca['my_kingress']
        self.assertIsInstance(mr, KIngress)
        self.assertEqual(mr.name, "my_kingress")

