from unittest import TestCase

from microtosca.loader.yml import YmlLoader
from microtosca.graph.template import MicroToscaTemplate
from microtosca.analyser import MicroToscaAnalyser

class TestAnalyser(TestCase):

    @classmethod
    def setUpClass(self):
        file = 'data/examples/helloworld_squads.yml'
        self.microtosca_template = self.get_template(file)
        self.analyser = MicroToscaAnalyser(self.microtosca_template)

    def test_shared_database(self):
        dbshared = self.analyser.all_shared_databases()
        self.assertEqual(dbshared,['order_db (database)'])

    def test_not_independently_deployabe(self):
        nid = self.analyser.all_not_independently_deployabe()
        self.assertEqual(nid,['order (service)'])

    def test_not_horizzontally_scalable(self):
        nid = self.analyser.all_not_horizzontally_scalable()
        self.assertEqual(nid,['shipping (service)'])

    def test_not_fault_resilient(self):
        nid = self.analyser.all_not_fault_resilient()
        self.assertEqual(nid,['order (service)'])

    def get_template(file):
        loader = YmlLoader()
        microtosca_template = loader.parse(file)
        microtosca_template.update() 
        return microtosca_template