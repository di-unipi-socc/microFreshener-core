import yaml

from ..model.template import MicroModel
from ..model.relationships import RunTimeInteraction, DeploymentTimeInteraction
from ..model.nodes import Root, Service, Database, CommunicationPattern


class YMLTransformer(object):

    def __init__(self):
        pass

    # Transform a microModel Oject to a Dicionary format.
    # @params:  microModel 
    # @return:  dictionary 
    def transform(self, micro_model):
        dict_model = self.serialize(micro_model)
        # ATTENTION: in the restful api the Response() 
        # object requires a dict that are than converted into json (or yml?)
        # return yaml.dump(dict_model, default_flow_style=False)
        return dict_model
        
    def serialize(self, obj):
        # d = {"topology_template":{
        #     "node_templates" : {
        #         "order": {
        #             "type": "micro.nodes.Service",
        #             "requirements": [
        #                 {"run_time": "order_db"},
        #                 {"run_time": "rabbitmq"},
        #                 {"run_time": "shipping"},
        #                 {"deployment_time": "order_db"},
        #                 {"deployment_time": "shipping"},
        #                 {"deployment_time": "rabbitmq"}
        #             ]
        #         }
        #     }
        # }}
        # return d
        d = {"topology_template":{}}
        if (isinstance(obj, MicroModel)):
            node_templates = {}
            for n in obj.nodes:
                node = {}
                nodeType = None
                if(isinstance(n, Service)):
                    nodeType =  "micro.nodes.Service"
                elif(isinstance(n, Database)):
                    nodeType =  "micro.nodes.Database"
                elif(isinstance(n, CommunicationPattern)):
                    nodeType =  "micro.nodes.Communicationpattern"
                else:
                    raise ValueError("Type of node not recognized {}".format(n))
                node['type'] = nodeType
                requirements = []
                for rel in n.relationships:
                    if(isinstance(rel, DeploymentTimeInteraction)):
                        requirements.append({'deployment_time': rel.target.name })
                    elif(isinstance(rel, RunTimeInteraction)):
                        requirements.append({'run_time': rel.target.name })
                    else:
                        raise ValueError("Relationship not recognized {}".format(rel))
                if requirements: node['requirements'] = requirements
                node_templates[n.name] = node
            d["topology_template"]["node_templates"] = node_templates
        return d
