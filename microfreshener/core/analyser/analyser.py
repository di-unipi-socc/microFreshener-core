
from ..model import Service, Database, CommunicationPattern, MessageBroker, MessageRouter
from ..analyser.sniffer import NodeSmellSniffer, GroupSmellSniffer
from ..logging import MyLogger

logger = MyLogger().get_logger()

from microfreshener.core.analyser.smell import WobblyServiceInteractionSmell, EndpointBasedServiceInteractionSmell


class MicroToscaAnalyser(object):

    def __init__(self, micro_model):
        self.micro_model = micro_model
        # list of NodeSmellSniffer to be executed for each node
        self.node_smell_sniffers: [NodeSmellSniffer] = []
        # list of GroupSmellSniffers to be executed for each group
        self.group_smell_sniffers: [GroupSmellSniffer] = []
        # list of smell to be ignored for each node
        self.ignored_smells_for_node = {}

    def ignore_smell_for_node(self, node, smell):
        if node.name not in self.ignored_smells_for_node:
            self.ignored_smells_for_node[node.name] = [smell]
        else:
            self.ignored_smells_for_node[node.name].apped(smell)

    def get_ignore_smells_for_node(self, node):
        return self.ignored_smells_for_node.get(node.name, None)

    def add_node_smell_sniffer(self, sniffer):
        assert isinstance(sniffer, NodeSmellSniffer)
        logger.debug("Node Sniffer {} added".format(sniffer))
        self.node_smell_sniffers.append(sniffer)

    def get_node_smell_sniffer(self):
        return self.node_smell_sniffers

    def add_group_smell_sniffer(self, sniffer):
        assert isinstance(sniffer, GroupSmellSniffer)
        logger.info("Group Sniffer {} added".format(sniffer))
        self.group_smell_sniffers.append(sniffer)

    def run(self):
        logger.debug("Running analysis")
        # Return a dictionary with two fields of types: ANodes:[], AGroups:[]
        result = {}
        nodes = []
        for node in self.micro_model.nodes:
            #  TODO: creare una classe ANode che identifica il nodo analizzato.
            anode = {'name': node.name}
            if(isinstance(node, Service)):
                anode["type"] = "software"
            if(isinstance(node, Database)):
                anode["type"] = "database"
            if(isinstance(node, MessageBroker)):
                anode["type"] = "communicationpattern"
                # TODO: remove concrete type
                anode['concrete_type'] = "messageBroker"
            if(isinstance(node, MessageRouter)):
                anode["type"] = "communicationpattern"
                # TODO: remove concrete type
                anode['concrete_type'] = "messageRouter"

            smells = []
            for sniffer in self.node_smell_sniffers:
                # if self.get_ignore_smells_for_node(node) or sniffer not in self.get_ignore_smells_for_node(node):
                smell = sniffer.snif(node)
                if(smell and not smell.isEmpty()):
                    smells.append(smell.to_dict())
            if(smells):  # add only nodes that has at least one smell
                anode['smells'] = smells
                nodes.append(anode)
        result['nodes'] = nodes

        groups = []
        for group in self.micro_model.groups:
            # TODO: create a AGroup class to mantain the resultults af the analysis
            agroup = {'name': group.name}
            smells = []
            for gsniffer in self.group_smell_sniffers:
                gsmells = gsniffer.snif(group)
                if(gsmells):
                    # NoApiGatewaysmellSniffer returns a list of node-based noApiGatewaySmellSniffer
                    if isinstance(gsmells, list):
                        for smell in gsmells:
                            if(not smell.isEmpty()):
                                smells.append(smell.to_dict())
                    else:
                        if(not gsmells.isEmpty()):
                            smells.append(gsmells.to_dict())
            if(smells):
                agroup['smells'] = smells
                groups.append(agroup)
        result['groups'] = groups

        return result
