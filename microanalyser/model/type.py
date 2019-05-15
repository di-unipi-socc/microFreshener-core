# MicroTosca types

# MICROTOSCA NODE TYPES
SERVICE = 'micro.nodes.Service'
DATABASE = 'micro.nodes.Database'

COMMUNICATION_PATTERN = 'micro.nodes.CommunicationPattern'
MESSAGE_BROKER = 'micro.nodes.MessageBroker'
MESSAGE_ROUTER = 'micro.nodes.MessageRouter'

CIRCUIT_BREAKER = 'micro.nodes.CircuitBreaker'
API_GATEWAY="micro.nodes.ApiGateway"

# MICROTOSCA RELATIONSHIP TYPES
INTERACT_WITH = 'micro.relationships.InteractsWith'
INTERACT_WITH_TIMEOUT_PROPERTY = "timeout"
INTERACT_WITH_CIRCUIT_BREAKER_PROPERTY = "circuit_breaker"
INTERACT_WITH_DYNAMIC_DISCOVEY_PROPERTY = "dynamic_discovery"

RUN_TIME = "run_time"
DEPLOYMENT_TIME = "deployment_time"

# MICROTOSCA GROUP TYPES
TEAM = 'micro.groups.Team'
EDGE = 'micro.groups.Edge'


