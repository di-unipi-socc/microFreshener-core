from unittest import TestCase

from microanalyser.loader import JSONLoader, YMLLoader
from microanalyser.trasformer import JSONTransformer



class TestJSONTranformer(TestCase):

    @classmethod
    def setUpClass(self):
        file = 'data/examples/helloworld.yml'
        self.loader = YMLLoader()
        self.microtosca = self.loader.load(file)
        self.tranformer = JSONTransformer()

    def test_dictionary_groups(self):
        edgeGroup = self.microtosca.get_group('edgenodes')
        group_dict = self.tranformer._transform_group(edgeGroup)
        self.assertEqual("name" in group_dict, True)
        self.assertEqual("type" in group_dict, True)
        self.assertEqual("members" in group_dict, True)

    def test_timedout_relationship(self):
        order = self.microtosca["order"]
        shipping = self.microtosca["shipping"]
        link_to_shipping = [link for link in order.run_time if link.target == shipping] 
        rel_dict = self.tranformer._transform_relationship(link_to_shipping[0])
        self.assertEqual("timeout" in rel_dict, True)
        self.assertEqual(rel_dict["timeout"], True)

        rabbitmq = self.microtosca["rabbitmq"]
        link_to_rabbitmq = [link for link in order.run_time if link.target == rabbitmq] 
        rel_dict = self.tranformer._transform_relationship(link_to_rabbitmq[0])
        self.assertEqual(rel_dict["timeout"], False)

    def test_squad_group(self): 
        squad =  self.microtosca.get_group("team1")
        squad_dict = self.tranformer._transform_group(squad)
        self.assertEqual(squad_dict['name'], "team1")
        self.assertEqual("type" in squad_dict, True)
        self.assertEqual(squad_dict['type'], "squadgroup")

        squad2 =  self.microtosca.get_group("team2")
        squad_dict = self.tranformer._transform_group(squad2)
        self.assertEqual('name' in squad_dict, True)
        self.assertEqual(squad_dict['name'], "team2")
        self.assertEqual("type" in squad_dict, True)
        self.assertEqual(squad_dict['type'], "squadgroup")
      





