from .analyser import MicroAnalyser
from .sniffer import EndpointBasedServiceInteractionSmellSniffer, NoApiGatewaySmellSniffer, WobblyServiceInteractionSmellSniffer, SharedPersistencySmellSniffer

from .constant import SMELL_ENDPOINT_BASED_SERVICE_INTERACTION, SMELL_NO_API_GATEWAY


class AnalyserBuilder(object):

    def __init__(self, micro_model):
        self.analyser = MicroAnalyser(micro_model)

    def add_smell(self, smell: int):
        if(smell == 1):  # MUltiple services in the same container
            pass
        elif(smell == 2):  # SMELL_NO_API_GATEWAY):
            self.analyser.add_group_smell_sniffer(NoApiGatewaySmellSniffer())
        elif (smell == 3):  # SMELL_ENDPOINT_BASED_SERVICE_INTERACTION):
            self.analyser.add_node_smell_sniffer(
                EndpointBasedServiceInteractionSmellSniffer())
        elif(smell == 4):  # WOBBLY SERGICE INTERACTION
            self.analyser.add_node_smell_sniffer(
                WobblyServiceInteractionSmellSniffer())
        elif (smell == 5):  # ESB MISUSE
            pass
        elif (smell == 6):  # SHARED PERSITENCY
            self.analyser.add_node_smell_sniffer(
                SharedPersistencySmellSniffer())
        elif (smell == 7):  # "Single Layer Team"
            pass 
        else:
            raise ValueError('Smell {} not recognized'.format(smell))
        return self

    def add_smells_related_to_principle(self, principle: str):
        # IndependentDeployability,HorizontalScalability,IsolateFailure,DecentraliseEverything
        sniffer: None
        if(principle == "HorizontalScalability"):
            self.analyser.add_node_smell_sniffer(
                EndpointBasedServiceInteractionSmellSniffer())
            self.analyser.add_group_smell_sniffer(NoApiGatewaySmellSniffer())
        elif (principle == "IsolateFailure"):
            self.analyser.add_node_smell_sniffer(
                WobblyServiceInteractionSmellSniffer())
        elif (principle == "IndependentDeployability"):
            pass
        elif (principle == "Decentralization"):
            self.analyser.add_node_smell_sniffer(
                SharedPersistencySmellSniffer())
            pass
        else:
            raise ValueError('Principle {} not recognized'.format(principle))
        return self

    def build(self):
        return self.analyser
