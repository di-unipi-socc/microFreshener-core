from unittest import TestCase

from microanalyser.loader.json import JSONLoader


class TestJSONLoader(TestCase):

    @classmethod
    def setUpClass(self):
        file = 'data/examples/hello-world-ok.json'
        loader = JSONLoader()
        self.microtosca_template = loader.load(file)
        self.microtosca_template.update() 

    def test_number_nodes(self):
        self.assertEqual(len(list(self.microtosca_template.nodes)), 4)

