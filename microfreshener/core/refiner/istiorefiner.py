from .irefiner import IRefiner
from ..model import MicroToscaModel
from ..model.nodes import KProxy

from ..errors import GroupNotFoundError, MicroToscaModelError
from ..model.groups import Edge
from ..logging import MyLogger

from nested_lookup import get_occurrence_of_key
from nested_lookup import nested_lookup
import yaml

logger = MyLogger().get_logger()


class IstioRefiner(IRefiner):

    def __init__(self, yml_file):
        self.yml_file = yml_file
        self._destination_rules = []

    def Refine(self, microtosca: MicroToscaModel) -> MicroToscaModel:
        self._load_istio_kobjects()
        self.microtosca = microtosca
        for iproxy in self._destination_rules:
            self.refine_destination_rule(iproxy)
        return self.microtosca

    def refine_destination_rule(self, drule):
        try:
            logger.info("refine node : {}".format(drule.host))
            if(drule.is_circuit_breaker()):
                node = self.microtosca[drule.host]
                for incoming in node.incoming_interactions:
                    incoming.set_circuit_breaker(True)
        except MicroToscaModelError as e:
            logger.error(e.message)

    def _load_istio_kobjects(self):
        with open(self.yml_file, 'r') as stream:
            docs = yaml.load_all(stream)
            for doc in docs:
                self._load_istio_object(doc)

    def _load_istio_object(self, kobject):
        if(kobject.get("kind") == "DestinationRule"):
            self._destination_rules.append(
                self._load_destination_rule_object(kobject))

    def _load_destination_rule_object(self, kobject):
        destination_rule = None
        if "metadata" in kobject.keys():
            metadata = kobject.get("metadata")
            name = nested_lookup('name', metadata)
            if len(name) == 0:
                raise Exception(f"Name in {kobject} not found")
            name = name[0]
        if "spec" in kobject.keys():
            spec = kobject.get("spec")
            host = nested_lookup('host', spec)
            if len(host) == 0:
                raise Exception(f"Host in {kobject} not found")
            host = host[0]
            policies = nested_lookup('trafficPolicy', spec)
            destination_rule = IDestinationRule(name, host, policies)
        return destination_rule


class IDestinationRule():
    def __init__(self, name, host, traffic_policies):
        self._name = name
        self._host = host
        # [ {'loadBalancer':...}, {'connectionPool':...}]
        self._policies = traffic_policies

    @property
    def host(self):
        return self._host

    @property
    def name(self):
        return self._name

    @property
    def traffic_policy(self):
        return self._policy

    def is_circuit_breaker(self):
        for policy in self._policies:
            print(policy)
            if get_occurrence_of_key(policy, "connectionPool") > 0:
                return True
        return False

    def is_load_balancer(self):
        for policy in self._policies:
            if get_occurrence_of_key(policy, "loadBalancer") > 0:
                return True
        return False

    def __str__(self):
        return '{} ({})'.format(self._name, 'IDestinationRule')
