from .analyser import MicroAnalyser
from .sniffer import EndpointBasedServiceInteractionSmellSniffer,NoApiGatewaySmellSniffer, WobblyServiceInteractionSmellSniffer, SharedPersistencySmellSniffer

class AnalyserBuilder(object):

  def __init__(self, micro_model):
    self.analyser = MicroAnalyser(micro_model)

  def add_node_smell_sniffer(self, name:str):
     pass

  def add_smells_related_to_principle(self, principle:str):
    # IndependentDeployability,HorizontalScalability,IsolateFailure,DecentraliseEverything
    sniffer:None
    if(principle == "HorizontalScalability"):
      self.analyser.add_node_smell_sniffer(EndpointBasedServiceInteractionSmellSniffer())
      self.analyser.add_group_smell_sniffer(NoApiGatewaySmellSniffer())
    elif (principle == "IsolateFailure"):
      self.analyser.add_node_smell_sniffer(WobblyServiceInteractionSmellSniffer())
    elif (principle == "IndependentDeployability"):
      pass
    elif (principle == "DecentraliseEverything"):
      self.analyser.add_node_smell_sniffer(SharedPersistencySmellSniffer())
      pass
    else:
      raise ValueError(' {} not recognized'.format(principle))

    # principle: = None
    # if (name == DecentraliseEverythingPrinciple.name):
    #     principle = DecentraliseEverythingPrinciple()
    # elif(name == IndependentDeployabilityPrinciple.name):
    #     principle = IndependentDeployabilityPrinciple()
    # elif (name == HorizontalScalabilityPrinciple.name):
    #     principle = HorizontalScalabilityPrinciple()
    # elif (name == IsolateFailurePrinciple.name):
    #     principle = IsolateFailurePrinciple()
    # else:
    #   raise ValueError('Name {} not recognized'.format(name))
    return self

  def build(self):
    return self.analyser