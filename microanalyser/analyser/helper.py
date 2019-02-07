
from .principles  import BOUNDED_CONTEXT, DECENTRALIZED_DATA, INDEPENDENTLY_DEPLOYABLE, HORIZZONTALLY_SCALABLE, FAULT_RESILIENCE

from .principles import  BoundedContextPrinciple, DecentralizedDataPrinciple, IndependentlyDeployablePrinciple, HorizzontallyScalablePrinciple, FaultResiliencePrinciple

def build_principle_from_name(name):
    if (name == BOUNDED_CONTEXT):
        return BoundedContextPrinciple()
    elif (name == DECENTRALIZED_DATA):
        return DecentralizedDataPrinciple()
    elif(name == INDEPENDENTLY_DEPLOYABLE):
        # print("creating ind dple principles")
        return IndependentlyDeployablePrinciple()
    elif (name == HORIZZONTALLY_SCALABLE):
        return HorizzontallyScalablePrinciple()
    elif (name == FAULT_RESILIENCE):
        return FaultResiliencePrinciple()

