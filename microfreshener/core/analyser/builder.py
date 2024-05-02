from .analyser import MicroToscaAnalyser
from .costants import SMELL_WOBBLY_SERVICE_INTERACTION_SMELL, SMELL_SHARED_PERSISTENCY, SMELL_SINGLE_LAYER_TEAMS, \
    SMELL_MULTIPLE_SERVICES_IN_ONE_CONTAINER, SMELL_ESB_MISUSE, SMELL_TIGHTLY_COUPLED_TEAMS, SMELL_SHARED_BOUNDED_CONTEXT
from .sniffer import EndpointBasedServiceInteractionSmellSniffer, NoApiGatewaySmellSniffer, \
    WobblyServiceInteractionSmellSniffer, SharedPersistencySmellSniffer, SingleLayerTeamsSmellSniffer, \
    MultipleServicesInOneContainerSmellSniffer, TightlyCoupledTeamsSmellSniffer, SharedBoundedContextSmellSniffer

from .constant import SMELL_ENDPOINT_BASED_SERVICE_INTERACTION, SMELL_NO_API_GATEWAY


class MicroToscaAnalyserBuilder(object):

    def __init__(self, micro_model):
        self.micro_model = micro_model
        self.analyser = MicroToscaAnalyser(micro_model)

    def add_smell(self, smell: str):
        if smell == SMELL_MULTIPLE_SERVICES_IN_ONE_CONTAINER or smell == 1:
            self.analyser.add_node_smell_sniffer (MultipleServicesInOneContainerSmellSniffer())
        elif smell == SMELL_NO_API_GATEWAY or smell == 2:
            self.analyser.add_group_smell_sniffer(NoApiGatewaySmellSniffer(self.micro_model))
        elif smell == SMELL_ENDPOINT_BASED_SERVICE_INTERACTION or smell == 3:
            self.analyser.add_node_smell_sniffer(EndpointBasedServiceInteractionSmellSniffer())
        elif smell == SMELL_WOBBLY_SERVICE_INTERACTION_SMELL  or smell == 4:
            self.analyser.add_node_smell_sniffer(WobblyServiceInteractionSmellSniffer())
        elif smell == SMELL_ESB_MISUSE  or smell == 5:
            pass
        elif smell == SMELL_SHARED_PERSISTENCY or smell == 6:
            self.analyser.add_node_smell_sniffer(SharedPersistencySmellSniffer())
        elif smell == SMELL_SINGLE_LAYER_TEAMS or smell == 7:
            self.analyser.add_group_smell_sniffer(SingleLayerTeamsSmellSniffer(self.micro_model))
        elif smell == SMELL_TIGHTLY_COUPLED_TEAMS or smell == 8:
            self.analyser.add_group_smell_sniffer(TightlyCoupledTeamsSmellSniffer(self.micro_model))
        elif smell == SMELL_SHARED_BOUNDED_CONTEXT or smell == 9:
            self.analyser.add_group_smell_sniffer(SharedBoundedContextSmellSniffer(self.micro_model))
        else:
            raise ValueError('Smell {} not recognized'.format(smell))
        return self

    def ignore_smell_for_node(self, node, smell:int):
        if(smell == SMELL_MULTIPLE_SERVICES_IN_ONE_CONTAINER):
            self.analyser.ignore_smell_for_node(node, MultipleServicesInOneContainerSmellSniffer())
        elif smell == SMELL_NO_API_GATEWAY:
            self.analyser.add_group_smell_sniffer(NoApiGatewaySmellSniffer(self.micro_model))
        elif smell == SMELL_ENDPOINT_BASED_SERVICE_INTERACTION:
           self.analyser.ignore_smell_for_node(node,  EndpointBasedServiceInteractionSmellSniffer())
        elif smell == SMELL_WOBBLY_SERVICE_INTERACTION_SMELL:
            self.analyser.ignore_smell_for_node(node, WobblyServiceInteractionSmellSniffer())
        elif smell == SMELL_ESB_MISUSE:
            pass
        elif smell == SMELL_SHARED_PERSISTENCY:
            self.analyser.add_node_smell_sniffer(SharedPersistencySmellSniffer())
        elif smell == SMELL_SINGLE_LAYER_TEAMS:
            self.analyser.add_group_smell_sniffer(SingleLayerTeamsSmellSniffer(self.micro_model))
        elif smell == SMELL_TIGHTLY_COUPLED_TEAMS:
            self.analyser.add_group_smell_sniffer(TightlyCoupledTeamsSmellSniffer(self.micro_model))
        elif smell == SMELL_SHARED_BOUNDED_CONTEXT:
            self.analyser.add_group_smell_sniffer(SharedBoundedContextSmellSniffer(self.micro_model))
        else:
            raise ValueError('Smell {} not recognized'.format(smell))
        return self
        
    def add_all_sniffers(self):
        self.analyser.add_node_smell_sniffer(EndpointBasedServiceInteractionSmellSniffer())
        self.analyser.add_node_smell_sniffer(WobblyServiceInteractionSmellSniffer())
        self.analyser.add_node_smell_sniffer(SharedPersistencySmellSniffer())
        self.analyser.add_node_smell_sniffer(MultipleServicesInOneContainerSmellSniffer())
        self.analyser.add_group_smell_sniffer(NoApiGatewaySmellSniffer(self.micro_model))
        self.analyser.add_group_smell_sniffer(SingleLayerTeamsSmellSniffer(self.micro_model))
        self.analyser.add_group_smell_sniffer(TightlyCoupledTeamsSmellSniffer(self.micro_model))
        self.analyser.add_group_smell_sniffer(SharedBoundedContextSmellSniffer(self.micro_model))
        return self

    def build(self):
        return self.analyser
