from unittest import TestCase
from microfreshener.core.importer import YMLImporter
from microfreshener.core.model import Team, Edge

class TestYMLloaderNodes(TestCase):

    @classmethod
    def setUpClass(self):
        file = 'data/tests/test_groups.yml'
        self.importer = YMLImporter()
        self.microtosca = self.importer.Import(file)

    def test_team1(self):
        t1 = self.microtosca.get_group("team1")
        self.assertEqual(len(t1.members),2)
        self.assertIsInstance(t1, Team)
    
    def test_team2(self):
        t2 = self.microtosca.get_group("team2")
        self.assertEqual(len(t2.members),3)
        self.assertIsInstance(t2, Team)

    def test_team3(self):
        t3 = self.microtosca.get_group("team3")
        self.assertEqual(len(t3.members),2)
        self.assertIsInstance(t3, Team)
    
    def test_edge(self):
        edge = self.microtosca.get_group("edgenodes")
        self.assertEqual(len(edge.members), 3) #  Database node cannot be into an Edge group
        self.assertIsInstance(edge, Edge)