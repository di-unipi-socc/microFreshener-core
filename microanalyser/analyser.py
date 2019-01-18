from .model.nodes import Service, Database, CommunicationPattern
from .model.relationships import InteractsWith
from .model.template import MicroModel

class MicroAnalyser(object):

    def __init__(self, micro_model):
        self.micro_model = micro_model
        self.antipatterns = {} # dictionary  of function to be execetued on each node for discover an antipatterns
        self.antipatterns['shared_database'] = self.shared_database
        self.antipatterns['not_independently_deployable'] = self.independently_deployabe
        self.antipatterns['not_horizzontally_scalable'] = self.horizzontally_scalable
        self.antipatterns['not_fault_resilient'] = self.fault_resilient
        self.antipatterns['wrong_cut'] = self.wrong_cut


        # self.wrong_cuts_relationships = []
        # self.shared_databases = []
        # self.not_independently_deployabe_services = []
        # self.not_horizzontally_scalable_services = []
        # self.not_fault_resilient_services = []

    def analyse(self):
        nodes_ap = []
        for node in self.micro_model.nodes:
            nodes_ap.append(self.analyse_node(node))
        return nodes_ap
    
    def analyse_node(self, node):
        node_dict = {'node': node, 
                    'name': node.name,
                    'antipatterns': []
                    }
        for name, funct in self.antipatterns.items():
            node_dict['antipatterns'].append({name: funct(node)})
        return node_dict
                
    def analyse_squad(self, name):
        wc_rels = {'squad':name, "nodes": []}
        squad = self.micro_model.get_squad(name)
        for member in squad.members:
           wc_rels["nodes"].append(self.analyse_node(member))
        return wc_rels

    def wrong_cut(self, node):
        interactions = []
        # if(isinstance(node, Service)):
        for relationship in node.relationships:
            source_node = relationship.source
            target_node = relationship.target
            source_squad = self.micro_model.squad_of(source_node)
            target_squad = self.micro_model.squad_of(target_node)
            if (isinstance(source_node, Service) and isinstance(target_node, Database)
                and source_squad != target_squad):
                interactions.append(relationship)
        return interactions


    def shared_database(self, node):
        if(isinstance(node, Database)):
            return set(rel for rel in node.incoming)
        else: return None
 
    def independently_deployabe(self, node):
        interaction = []
        if(isinstance(node, Service)):
             interaction = [dt_interaction for dt_interaction in node.deployment_time if (isinstance(dt_interaction.target, Service)
                            # TODO: cehck if is derived from a Communication Pattern
                            or isinstance(dt_interaction.target, CommunicationPattern))]
        return interaction

    def horizzontally_scalable(self, node):
        interaction = []
        if(isinstance(node, Service)):
            interactions = [up_rt for up_rt in node.up_run_time_requirements if (
                isinstance(up_rt.source, Service))]
        return interaction

    def fault_resilient(self, node):
        interactions = []
        if(isinstance(node, Service)):
            interactions = [rt_int for rt_int in node.run_time if isinstance(rt_int.target, Service)]
            # TODO: guardare se esiste un path che arriva a un'altro servizio in cui non c'è un CircuiBreaker
            # odes_patterns = [req.target for req in node.run_time if (isinstance(req.target, CommunicationPattern) and
            #                                              renq.target.concrete_type !=  CIRCUIT_BREAKER)
            #             ]
            # vs_patterns = [node for node in nodes_patterns if node.]
        return interactions

    # shared persitency antipattern
    def all_shared_databases(self):
        """Check the  presence of inapprorpiate service intimacy and shared persistency antipatterns"""
        shared_databases = []
        for node in self.micro_model.databases:
            if(self.is_shared_database(node)):
                shared_databases.append(str(node))
        return shared_databases

    def all_not_independently_deployabe(self):
        service_with_deployment_interactions = []
        for node in self.micro_model.services:
            if(not self.is_independently_deployabe(node)):
                service_with_deployment_interactions.append(str(node))
        return service_with_deployment_interactions

    def all_not_horizzontally_scalable(self):
        services_with_direct_run_time = []
        for node in self.micro_model.services:
            if(not self.is_horizzontally_scalable(node)):
                services_with_direct_run_time.append(str(node))
        return services_with_direct_run_time

    def all_not_fault_resilient(self):
        services_not_fault_resilient = []
        for node in self.micro_model.services:
            if(not self.is_fault_resilient(node)):
                services_not_fault_resilient.append(str(node))
        return services_not_fault_resilient
