from .antipatterns import WRONG_CUT, SHARED_PERSISTENCY

PROPERTIES = BOUNDED_CONTEXT, DECENTRALIZED_DATA, INDEPENDENTLY_DEPLOYABLE, HORIZZONTALLY_SCALABLE, FAULT_RESILIENCE=\
             'boundedContext', 'decentralizedData', 'independentlyDeployable', 'horizzontallyScalable', 'faultResilience'


CONFIG_ANALYSER = {
    'principles': [
        {
            "name": BOUNDED_CONTEXT,
            "antipatterns":[ 
                {
                    "name": WRONG_CUT
                },
            ]
        },
        {
            "name": DECENTRALIZED_DATA,
            "antipatterns":[ 
                {
                    "name": SHARED_PERSISTENCY
                },
            ]
        }
    ]
    
}