
from ..model.nodes import Service, Database, CommunicationPattern
from ..analyser.sniffer import NodeSmellSniffer, GroupSmellSniffer
from ..logging import MyLogger

logger = MyLogger().get_logger()


from microanalyser.analyser.smell import WobblyServiceInteractionSmell, EndpointBasedServiceInteractionSmell


class MicroAnalyser(object):

    def __init__(self, micro_model):
        self.micro_model = micro_model
        # list of NodeSmellSniffer to be executed for each node
        self.node_smell_sniffers: [NodeSmellSniffer] = []
        # list of GroupSmellSniffers to be executed for each group
        self.group_smell_sniffers: [GroupSmellSniffer] = []
        self.ignored_smells_for_node = {}

    def ignore_smell_for_node(self, node, smell):
        if node not in self.ignored_smells_for_node:
            self.ignored_smells_for_node[node] = [smell]
        else:
            self.ignored_smells_for_node[node].apped(smell)

    def add_node_smell_sniffer(self, sniffer):
        assert isinstance(sniffer, NodeSmellSniffer)
        logger.info("Node Sniffer {} added".format(sniffer))
        self.node_smell_sniffers.append(sniffer)

    def add_group_smell_sniffer(self, sniffer):
        assert isinstance(sniffer, GroupSmellSniffer)
        logger.info("Group Sniffer {} added".format(sniffer))
        self.group_smell_sniffers.append(sniffer)

    def run(self):
        logger.info("Running analysis")
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
            if(isinstance(node, CommunicationPattern)):
                anode["type"] = "communicationpattern"
                anode['concrete_type'] = node.concrete_type
            smells = []
            for sniffer in self.node_smell_sniffers:
                smell = sniffer.snif(node)
                if(smell):
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
                    if isinstance(gsmells, list):
                        for smell in gsmells:
                            smells.append(smell.to_dict())
                    else:
                        smells.append(gsmells.to_dict())

            if(smells):
                agroup['smells'] = smells
                groups.append(agroup)
        result['groups'] = groups

        return result
