from .analyser import MicroToscaAnalyser
from .sniffer import EndpointBasedServiceInteractionSmellSniffer, NoApiGatewaySmellSniffer, WobblyServiceInteractionSmellSniffer, SharedPersistencySmellSniffer, CrossTeamDataManagementSmellSniffer

from .constant import SMELL_ENDPOINT_BASED_SERVICE_INTERACTION, SMELL_NO_API_GATEWAY


class MicroToscaAnalyserBuilder(object):

    def __init__(self, micro_model):
        self.micro_model = micro_model
        self.analyser = MicroToscaAnalyser(micro_model)

    def add_smell(self, smell: int):
        if(smell == 1):     # Multiple services in the same container
            pass
        elif(smell == 2):   # NO_API_GATEWAY
            self.analyser.add_group_smell_sniffer(NoApiGatewaySmellSniffer(self.micro_model))
        elif (smell == 3):  # ENDPOINT_BASED_SERVICE_INTERACTION):
            self.analyser.add_node_smell_sniffer(
                EndpointBasedServiceInteractionSmellSniffer())
        elif(smell == 4):   # WOBBLY SERGICE INTERACTION
            self.analyser.add_node_smell_sniffer(
                WobblyServiceInteractionSmellSniffer())
        elif (smell == 5):  # ESB MISUSE
            pass
        elif (smell == 6):  # SHARED PERSITENCY
            self.analyser.add_node_smell_sniffer(
                SharedPersistencySmellSniffer())
        elif (smell == 7):  # SINGLE LAYER MICROTOSCA_GROUPS_TEAM
            self.analyser.add_group_smell_sniffer(CrossTeamDataManagementSmellSniffer(self.micro_model))
        else:
            raise ValueError('Smell {} not recognized'.format(smell))
        return self

    def ignore_smell_for_node(self, node, smell:int):
        if(smell == 1):     # Multiple services in the same container
            pass
        elif(smell == 2):   # NO_API_GATEWAY
            self.analyser.add_group_smell_sniffer(NoApiGatewaySmellSniffer(self.micro_model))
        elif (smell == 3):  # ENDPOINT_BASED_SERVICE_INTERACTION):
           self.analyser.ignore_smell_for_node(node,  EndpointBasedServiceInteractionSmellSniffer())
        elif(smell == 4):   # WOBBLY SERGICE INTERACTION
            self.analyser.ignore_smell_for_node(node, WobblyServiceInteractionSmellSniffer())
        elif (smell == 5):  # ESB MISUSE
            pass
        elif (smell == 6):  # SHARED PERSITENCY
            self.analyser.add_node_smell_sniffer(
                SharedPersistencySmellSniffer())
        elif (smell == 7):  # SINGLE LAYER MICROTOSCA_GROUPS_TEAM
            self.analyser.add_group_smell_sniffer(CrossTeamDataManagementSmellSniffer(self.micro_model))
        else:
            raise ValueError('Smell {} not recognized'.format(smell))
        return self
        
        
    def build(self):
        return self.analyser
