
from ..model.nodes import Root, Service, Database, CommunicationPattern
from .helper import build_principle_from_name
from .principles import PRINCIPLES
from .principles import DecentraliseEverythingPrinciple, IndependentDeployabilityPrinciple, HorizontalScalabilityPrinciple, IsolateFailurePrinciple
from .antipatterns import DirectInteractionAntipattern, SharedPersistencyAntipattern, SharedPersistencyAntipattern,  DeploymentInteractionAntipattern, CascadingFailureAntipattern
from ..model.template import Service, Database, CommunicationPattern
import pprint

from ..logging import MyLogger

logger = MyLogger().get_logger()


class MicroAnalyser(object):

    def __init__(self, micro_model):
        self.micro_model = micro_model
        self.smell_sniffers = [] 

    def add_smell_sniffer(self, sniffer):
        self.smell_sniffers.append(sniffer)

    def run(self):
        res = {}
        nodes = []
        for node in self.micro_model.nodes:
            #  TODO: creare una classe ANode che identifica il nodo analizzato.
            anode = {'name': node.name, 'id': node.id}
            if(isinstance(node, Service)):
                anode["type"] =  "software"
            if(isinstance(node, Database)):
                anode["type"] =  "database"
            if(isinstance(node, CommunicationPattern)):
                anode["type"] =  "communicationpattern"
                anode['concrete_type'] = node.concrete_type
            smells = []
            for sniffer in self.smell_sniffers:
                    smell = sniffer.snif(node)
                    if(smell):
                        smells.append(smell.to_dict())
            anode['smells'] = smells
            nodes.append(anode)
        res['nodes'] = nodes
        return res


    # def analyse(self, nodes_to_exclude=[], principles_to_check=PRINCIPLES, config_nodes={}):
    #     ''' principles_to_check = ['independently deployable', horizzontally scalable, ]
    #        config_nodes  = { 'shipping': { 'antipatterns-to_eclude" :['ap1', 'ap2', 'ap3'] }
    #     '''
    #     logger.info("Analyser - analysing ...")
    #     results = {}
    #     nodes = []
    #     for node in self.micro_model.nodes:
    #         if node.name not in nodes_to_exclude:
    #             n = {"name": node.name, 'principles': self.analyse_node(node)}
    #             nodes.append(n)
    #     # execute the principles that involve all the nodes of the graph
    #     for principle in self.nodesAnalysers:
    #         res = principle.visit(self.micro_model)
    #         results
    #     results['nodes'] = nodes
    #     return results

    # def analyse_node(self, node):
    #     logger.debug("Analyser - analysing node {}.".format(node))
    #     principles = []
    #     for principle in self.nodesAnalysers:
    #         res = principle.visit(node)
    #         if(res is not None):
    #             principles.append(
    #                 {"name": principle.name, "antipatterns": res.to_dict()})
    #     return principles if principles else None

        # logger.debug("Analyser - analysing node {}.".format(node))
        # res = {'name' : node.name, 'id': node.id}
        # res['principles'] =  []
        # for principle_name in principles_to_check:
        #     logger.debug("Analyser - checking {} principle".format(principle_name))
        #     principleObject = build_principle_from_name(principle_name)
        #     principleObject.apply_to(node)
        #     if(not principleObject.isEmpty()):
        #         res['principles'].append(principleObject.to_dict())
        # return res

    '''
    {
    node : <name>
    type : Service | Database | CommunicationPattern
    principles : [
        {   id: 1,
            name: bounded context: {
            antipatterns : [
                {   id: 1,
                    name: wrong_cut 
                    cause: Interaction(x,y)
                    refactorings: [
                        {   id: 1,
                            name: movedbT1,
                            solution: 
                        },
                        {   id: 2,
                            name: movedbT2:
                            solution:  antipatterns : [
                {   id: 1,
                    name: wrong_cut 
                    cause: Interaction(x,y)
                    refactorings: [
                        {   id: 1,
                            name: movedbT1,
                            solution: 
                        },
                        {   id: 2,
                            name: movedbT2:
                            solution:  
                        },
                        {   id: 3
                            name: addManager: 
                            solution; 
                        }
                ]
            ]
        },
        {   id: 2
            name: decentralized data managment
            antipatterns :[
                {
                    name: shared persitency,
                    cause: interaction(),
                    refactorings: [
                        {
                            name:shares persistency
                            solution:
                        }
                ]
                }
            ]
        },
        {   id: 3
            name: independently deployable 
        ...
    ]
    '''
    # def analyse_node(self, node, principles_to_check=[], antipatterns_to_exclude=[]):
    #     logger.debug("Analyser - analysing node {}.".format(node))
    #     res = {'name' : node.name, 'id': node.id}
    #     res['principles'] =  []
    #     for principle_name in principles_to_check:
    #         logger.debug("Analyser - checking {} principle".format(principle_name))
    #         principleObject = build_principle_from_name(principle_name)
    #         principleObject.apply_to(node)
    #         if(not principleObject.isEmpty()):
    #             res['principles'].append(principleObject.to_dict())
    #     return res

    def analyse_squad(self, name, config_nodes={}):
        wc_rels = {'squad': name, "nodes": []}
        squad = self.micro_model.get_squad(name)
        for member in squad.members:
            wc_rels["nodes"].append(self.analyse_node(
                member, config_nodes.get(member.name, {})))
        return wc_rels

    # def _check_principle_on_node(self, node, principle):
    #     indDepl = IndependentDeployabilityPrinciple()
    #     indDepl.apply_to(node)
    #     if(not indDepl.isEmpty()):
    #         res['principles'].append(indDepl.to_dict())

    # def wrong_cut(self, node):
    #     interactions = []
    #     for relationship in node.relationships:
    #         source_node = relationship.source
    #         target_node = relationship.target
    #         source_squad = self.micro_model.squad_of(source_node)
    #         target_squad = self.micro_model.squad_of(target_node)
    #         if (isinstance(source_node, Service) and isinstance(target_node, Database)
    #             and source_squad != target_squad):
    #             interactions.append(relationship)
    #     return interactions

    # def shared_persistency(self, node):
    #     if(isinstance(node, Database)):
    #         return set(rel for rel in node.incoming)
    #     else: return None

    # def deployment_time_interaction(self, node):
    #     interaction = []
    #     if(isinstance(node, Service)):
    #          interaction = [dt_interaction for dt_interaction in node.deployment_time if (isinstance(dt_interaction.target, Service)
    #                         # TODO: cehck if is derived from a Communication Pattern
    #                         or isinstance(dt_interaction.target, CommunicationPattern))]
    #     return interaction

    # def direct_service_interaction(self, node):
    #     interactions = []
    #     if(isinstance(node, Service)):
    #         interactions = [up_rt for up_rt in node.up_run_time_requirements if (
    #             isinstance(up_rt.source, Service))]
    #     return interactions

    # def cascading_failures(self, node):
    #     interactions = []
    #     if(isinstance(node, Service)):
    #         interactions = [rt_int for rt_int in node.run_time if isinstance(rt_int.target, Service)]
    #         # TODO: guardare se esiste un path che arriva a un'altro servizio in cui non c'è un CircuiBreaker
    #         # nodes_patterns = [req.target for req in node.run_time if (isinstance(req.target, CommunicationPattern) and
    #         #                                              renq.target.concrete_type !=  CIRCUIT_BREAKER)
    #         #             ]
    #         # vs_patterns = [node for node in nodes_patterns if node.]
    #     return interactions
