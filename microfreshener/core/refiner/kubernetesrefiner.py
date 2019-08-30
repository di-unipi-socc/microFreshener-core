from .irefiner import Refiner
from ..model import MicroToscaModel
from ..model.nodes import KIngress, KService, KProxy
from ..logging import MyLogger

import yaml

logger = MyLogger().get_logger()

class KubernetesRefiner(Refiner):

    def __init__(self, yml_file):
        self.yml_file = yml_file
        self.kdeployemnts = []
        self.kservices = []
        with open(self.yml_file, 'r') as stream:
            docs = yaml.load_all(stream)
            for doc in docs:
                self._load_kobject(doc)

    def Refine(self, microtosca: MicroToscaModel)->MicroToscaModel:
        self.microtosca = microtosca
        for kservice in self.kservices:
            self.refine_kservice(kservice)
        return self.microtosca

    def refine_kservice(self, kservice):
        selected_name = kservice.selector.get('name')
        selected_node = self.microtosca[selected_name]
        incoming_interactions = list(selected_node.incoming_interactions)
        for incoming in incoming_interactions:
            if isinstance(incoming.source, KService):
                raise Exception(
                    f"{selected_node} has already a kservice defined")
        for incoming in  incoming_interactions:
            incoming.source.remove_interaction(incoming)
            incoming.source.add_interaction(kservice, False, False, True)
        kservice.add_interaction(selected_node)
        self.microtosca.add_node(kservice)

    def _load_kobject(self, kobject):
        # if(kobject.get("kind") == "Deployment"):
        #     self.kdeployemnts.append(self._load_kdeployment(kobject))
        if(kobject.get("kind") == "Service"):
            self.kservices.append(self._load_kservice(kobject))
        # if(kobject.get("kind") == "Ingress"):
        #     self._load_kingress(kobject)

    def _load_kdeployment(self, kobject):
        name = None
        labels = []
        if "metadata" in kobject.keys():
            metadata = kobject.get("metadata")
            if "name" in metadata.keys():
                name = metadata.get("name")
            if "labels" in metadata.keys():
                labels = metadata.get("labels")
        return {"name": name, "labels": labels}

    def _load_kservice(self, kobject):
        kservice = None
        if "metadata" in kobject.keys():
            metadata = kobject.get("metadata")
            if "name" in metadata.keys():
                name = f"k{metadata.get('name')}"
        if "spec" in kobject.keys():
            spec = kobject.get("spec")
            if "selector" in spec.keys():
                selector = spec.get("selector")
                #  <key: value>
                #  the service target all the pods with a label that match the key:value
        return KService(name, selector)

    def _load_kingress(self, kobject):
        name = None
        selector = None
        if "metadata" in kobject.keys():
            metadata = kobject.get("metadata")
            if "name" in metadata.keys():
                name = metadata.get("name")
        if "spec" in kobject.keys():
            spec = kobject.get("spec")
            if "rules" in spec.keys():
                selector = spec.get("selector")
        return {"name": name, "selector": selector}
