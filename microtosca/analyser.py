from graph.nodes import Service, Database, CommunicationPattern
from graph.relationships import InteractsWith
from graph.template import MicroToscaTemplate

class MicroToscaAnalyser(object):

    def __init__(self, micro_tosca_template):
        self.micro_template = micro_tosca_template

    # shared persitency antipattern
    def shared_databases_antipatterns(self):
        """Check the  presence of inapprorpiate service intimacy and shared persistency antipatterns"""
        shared_databases = []
        for node in self.micro_template.databases:
            s = set(rel for rel in node.incoming)
            if( len(s) > 1):
                shared_databases.append(node)
        return shared_databases

    def deployment_time_interaction_antipattern(self):
        service_with_deployment_interactions = {}
        for node in self.micro_template.services:
            interaction = [depl_int for depl_int in node.deployment_time 
                            if (isinstance(depl_int.target, Service) or 
                                isinstance(depl_int.target, CommunicationPattern))
                        ]
            if(interaction):
                service_with_deployment_interactions.update({node.name: interaction})
        return service_with_deployment_interactions   

    def direct_run_time_interaction(self):
        services_with_direct_run_time  = {}
        for node in self.micro_template.services:
            vs_nodes = [req for req in node.up_run_time_requirements if (isinstance(req.source, Service))]
            if(vs_nodes):
                services_with_direct_run_time.update({node.name: vs_nodes})
        return services_with_direct_run_time

    def cascading_failures(self):
        services_not_fault_resilient  = {}
        for node in self.micro_template.services:
            reqs_node = [req for req in node.run_time if isinstance(req.target, Service)]
            # TODO: guardare se esiste un path che arriva a un'altro servizio in cui non c'è un CircuiBreaker
            # odes_patterns = [req.target for req in node.run_time if (isinstance(req.target, CommunicationPattern) and 
            #                                              renq.target.concrete_type !=  CIRCUIT_BREAKER)
            #             ]
            # vs_patterns = [node for node in nodes_patterns if node.]
            if(reqs_node):
                services_not_fault_resilient.update({node.name: reqs_node})
        return services_not_fault_resilient

