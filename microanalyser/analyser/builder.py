from .analyser import MicroAnalyser
from .principles import  DecentraliseEverythingPrinciple, IndependentDeployabilityPrinciple, HorizontalScalabilityPrinciple, IsolateFailurePrinciple
from .principles import Principle
from .sniffer import EndpointBasedServiceInteractionSmellSniffer, WobblyServiceInteractionSmellSniffer, SharedPersistencySmellSniffer

class AnalyserBuilder(object):

  def __init__(self, micro_model):
    self.analyser = MicroAnalyser(micro_model)

  def add_smells_related_to_principle(self, principle:str):
    # IndependentDeployability,HorizontalScalability,IsolateFailure,DecentraliseEverything
    sniffer:None
    if(principle == "HorizontalScalability"):
      self.analyser.add_smell_sniffer(EndpointBasedServiceInteractionSmellSniffer())
    elif (principle == "IsolateFailure"):
      self.analyser.add_smell_sniffer(WobblyServiceInteractionSmellSniffer())
    elif (principle == "IndependentDeployability"):
      pass
    elif (principle == "DecentraliseEverything"):
      self.analyser.add_smell_sniffer(SharedPersistencySmellSniffer())
      pass
    else:
      raise ValueError('Principle {} not recognized'.format(principle))

    # principle:Principle = None
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