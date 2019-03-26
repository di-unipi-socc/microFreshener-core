from unittest import TestCase

from microanalyser.loader import YMLLoader
from microanalyser.analyser import MicroAnalyser

from microanalyser.analyser.sniffer import NoApiGatewaySmellSniffer, WobblyServiceInteractionSmellSniffer

class TestJSONLoader(TestCase):

    @classmethod
    def setUpClass(self):
        pass
        # file = 'data/examples/helloworld.json'
        # loader = YMLLoader()
        # micro_object = loader.load(file)
        # self.analyser = MicroAnalyser(micro_object)
    
    def test_SmellSniffer(self):
        pass
        # self.analyser.add_smell_sniffer(NoApiGatewaySmellSniffer())

        # smell = self.analyser.run()