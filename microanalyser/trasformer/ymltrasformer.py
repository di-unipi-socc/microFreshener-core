import yaml

from ..model.template import MicroModel
from ..model.relationships import RunTimeInteraction, DeploymentTimeInteraction
from ..model.nodes import Root, Service, Database, CommunicationPattern


class YMLTransformer(object):

    def __init__(self):
        pass

    # Transform a microModel Oject to a Dicionary format.
    # @input:  microModel 
    # @return: dict 
    def transform(self, micro_model):
        dict_model = self.serialize(micro_model)

        print (yaml.safe_dump(dict_model)    )
        # TODO: returns a JSON o bject instead of dict
        # ATTENTION: in the restfule api the Response() object requires a dict that are than converted into json
        # return json.dumps(self.serialize(micro_model), ensure_ascii=False)

    def serialize(self, obj):
        d = {}
        if (isinstance(obj, MicroModel)):
            d["node_template"] = {}
            # d["name"] = obj.name # name of the models
            # d['nodes'] = []      # nodes 
            # d['links'] = []      # links 
            for n in obj.nodes:
                ndict = {}
                # ndict['name'] = n.name
                # ndict['id'] = n.id
                if(isinstance(n, Service)):
                   ndict['type'] =  "micro.nodes.Service"
                elif(isinstance(n, Database)):
                    ndict['type'] =  "micro.nodes.Database"
                elif(isinstance(n, CommunicationPattern)):
                   ndict['type'] =  "micro.nodes.Communicationpattern"
                else:
                    # TODO throw an excpetion ?? Node not found
                    ndict['type'] =  None
                d["node_template"][n.name] = ndict
                #d['nodes'].append(ndict)

                for rel in n.relationships:
                    nrel = {}
                    # nrel['target'] = rel.target.id
                    # nrel['source'] = rel.source.id
                    nrel['target'] = rel.target.name
                    nrel['source'] = rel.source.name
                    # if(isinstance(rel.target, Root)):
                    #     nrel['target'] = rel.target.name
                    # else:
                    #     nrel['target'] = rel.target
                    if(isinstance(rel, DeploymentTimeInteraction)):
                        nrel['type'] = 'deploymenttime'
                    elif(isinstance(rel, RunTimeInteraction)):
                        nrel['type'] = 'runtime'
                    else:
                        nrel['type'] = None
                        #TODO Throw an exception type not recognized
                        raise ValueError('Relationship not recognized.')
                    d['links'].append(nrel)
        return d
