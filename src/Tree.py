# Rename Tree class
from Node import AtomNode, ConnectorNode, ConnectorType, Sign


# TODO Test to print with no nodes
class Tree:
    def __init__(self):
        self.atoms = []
        rootNode = ConnectorNode(ConnectorType.AND)

        atom_a = AtomNode('A')
        atomB = AtomNode('B')
        atomC = AtomNode('C')
        atomD = AtomNode('D')
        atomE = AtomNode('E')

        rootNode.append_connector_nodes(atom_a, Sign.POSITIVE)
        rootNode.append_connector_nodes(atomB, Sign.POSITIVE)
        rootNode.append_connector_nodes(atomC, Sign.POSITIVE)
        rootNode.append_connector_nodes(atomD, Sign.POSITIVE)
        rootNode.append_connector_nodes(atomE, Sign.POSITIVE)
        self.root_node = rootNode

        connectorBC = ConnectorNode(ConnectorType.AND)
        connectorBC.append_connector_nodes(atomB, Sign.POSITIVE)
        connectorBC.append_connector_nodes(atomC, Sign.POSITIVE)

        atom_a.append_child(connectorBC, Sign.POSITIVE)

        connectorDE = ConnectorNode(ConnectorType.OR)
        connectorDE.append_connector_nodes(atomD, Sign.POSITIVE)
        connectorDE.append_connector_nodes(atomE, Sign.POSITIVE)
        atomB.append_child(connectorDE, Sign.POSITIVE)

        atomC.append_child(atomB, Sign.POSITIVE)

        connectorBC2 = ConnectorNode(ConnectorType.AND)
        connectorBC2.append_connector_nodes(atomC, Sign.POSITIVE)
        connectorBC2.append_connector_nodes(atomB, Sign.POSITIVE)

        connectorBCorA = ConnectorNode(ConnectorType.OR)
        connectorBCorA.append_connector_nodes(connectorBC2, Sign.POSITIVE)
        connectorBCorA.append_connector_nodes(atom_a, Sign.POSITIVE)
        atomD.append_child(connectorBCorA, Sign.POSITIVE)

    # def resolve(self):
    # Resulte not until  true is found but also try filling everything to set some data

    def __repr__(self):
        print("🌲🌲🌲 \033[95mTree representation\033[0m 🌲🌲🌲")
        print (self.root_node)

tree = Tree()
# print(tree)
