from unittest import TestCase

from microanalyser.loader import JSONLoader
from microanalyser.trasformer import YMLTransformer



class TestYMLTranformer(TestCase):

    @classmethod
    def setUpClass(self):
        file = 'data/examples/helloworld.json' 
        loader = JSONLoader()
        microtosca_template = loader.load(file)
        self.tranformer = YMLTransformer()
        self.dict_model = self.tranformer.transform(microtosca_template)

    def test_dictionary_created(self):
        ntemplate = {'topology_template': {
                'node_templates':  {
                    'order': {
                        'requirements': [
                                    {'run_time': 'shipping'},  
                                    {'run_time': 'orderdb'},
                                    {'run_time': 'rabbitmq'},
                                    {'deployment_time': 'shipping'},
                                    {'deployment_time': 'orderdb'}
                                    ],
                        'type': 'micro.nodes.Service'},
                    'orderdb': {
                        'type': 'micro.nodes.Database'},
                    'rabbitmq': {
                        'type': 'micro.nodes.Communicationpattern'},
                    'shipping': {
                        'requirements': [{'run_time': 'orderdb'},
                                        {'run_time': 'rabbitmq'},
                                        {'deployment_time': 'orderdb'}],
                        'type': 'micro.nodes.Service'}
                }
            }
        }
        self.assertDictEqual(self.dict_model, ntemplate)



