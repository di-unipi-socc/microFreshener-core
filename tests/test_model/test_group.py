from unittest import TestCase

from microfreshener.core.model.microtosca import MicroToscaModel
from microfreshener.core.model.nodes import Service, Datastore, MessageBroker, MessageRouter
from microfreshener.core.errors import MicroToscaModelError, GroupNotFoundError, GroupNotFoundError
from microfreshener.core.model import Team, Edge


class TestGroupMicrotosca(TestCase):

    @classmethod
    def setUpClass(self):
        self.name = "prova-model"
        self.microtosca = MicroToscaModel(self.name)

    def test_create_team(self):
        first = self.microtosca.add_node(Service("first-team"))
        second = self.microtosca.add_node(Service("second-team"))
        team = Team("prova-team")
        team.add_member(first)
        team.add_member(second)
        self.assertIn(first, team)
        self.assertIn(second, team)
        self.assertEqual(len(team.members), 2)
        self.assertEqual(team[first.name], first)

    def test_add_get_team(self):
        team_name = "prova-team-add"
        first = self.microtosca.add_node(Service("first-team-add"))
        second = self.microtosca.add_node(Service("second-team-add"))
        team = Team(team_name)
        team.add_member(first)
        team.add_member(second)
        self.microtosca.add_group(team)
        self.assertIsInstance(self.microtosca.get_group(team_name), Team)
        self.assertEqual(self.microtosca.get_group(team_name), team)

    def test_get_team_error(self):
        with self.assertRaises(GroupNotFoundError):
            self.microtosca.get_group("fake team")

    def test_remove_member(self):
        first = self.microtosca.add_node(Service("fteam"))
        second = self.microtosca.add_node(Service("steam"))
        team = Team("pteam")
        team.add_member(first)
        team.add_member(second)
        self.assertEqual(len(team.members), 2)
        team.remove_member(first)
        self.assertIn(first, self.microtosca.nodes)
        self.assertEqual(len(team.members), 1)
        self.assertNotIn(first, team.members)
        self.assertIn(second, team.members)

    def test_add_edge(self):
        edge = Edge("myedge")
        edge.add_member(Service("first-edge"))
        edge.add_member(Service("second-edge"))
        self.microtosca.add_group(edge)
        self.assertEqual(len(edge.members), 2)
        self.assertIsInstance(self.microtosca.get_group("myedge"), Edge)
        
    def test_get_edge_error(self):
        microtosca = MicroToscaModel(self.name)
        with self.assertRaises(GroupNotFoundError):
            microtosca.edge
