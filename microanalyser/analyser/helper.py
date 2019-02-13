
from .principles import  DecentraliseEverythingPrinciple, IndependentDeployabilityPrinciple, HorizontalScalabilityPrinciple, IsolateFailurePrinciple

def build_principle_from_name(name):
    if (name == DecentraliseEverythingPrinciple.name):
        return DecentraliseEverythingPrinciple()
    elif(name == IndependentDeployabilityPrinciple.name):
        return IndependentDeployabilityPrinciple()
    elif (name == HorizontalScalabilityPrinciple.name):
        return HorizontalScalabilityPrinciple()
    elif (name == IsolateFailurePrinciple.name):
        return IsolateFailurePrinciple()

