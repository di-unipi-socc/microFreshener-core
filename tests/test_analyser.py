from unittest import TestCase

from microanalyser.loader.yml import MicroToscaLoader
from microanalyser.model.template import MicroModel
from microanalyser.analyser import MicroAnalyser

class TestAnalyser(TestCase):

    @classmethod
    def setUpClass(self):
        file = 'data/examples/helloworld_squads.yml'
        self.microtosca_template = self.get_template(file)
        self.analyser = MicroAnalyser(self.microtosca_template)

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
        loader = MicroToscaLoader()
        microtosca_template = loader.load(file)
        microtosca_template.update() 
        return microtosca_template