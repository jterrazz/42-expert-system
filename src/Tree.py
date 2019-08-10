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

        rootNode.append_operand(atom_a, Sign.POSITIVE)
        rootNode.append_operand(atomB, Sign.POSITIVE)
        rootNode.append_operand(atomC, Sign.POSITIVE)
        rootNode.append_operand(atomD, Sign.POSITIVE)
        rootNode.append_operand(atomE, Sign.POSITIVE)
        self.root_node = rootNode

        connectorBC = ConnectorNode(ConnectorType.AND)
        connectorBC.append_operand(atomB, Sign.POSITIVE)
        connectorBC.append_operand(atomC, Sign.POSITIVE)

        atom_a.append_child(connectorBC, Sign.POSITIVE)

        connectorDE = ConnectorNode(ConnectorType.OR)
        connectorDE.append_operand(atomD, Sign.POSITIVE)
        connectorDE.append_operand(atomE, Sign.POSITIVE)
        atomB.append_child(connectorDE, Sign.POSITIVE)

        atomC.append_child(atomB, Sign.POSITIVE)

        connectorBC2 = ConnectorNode(ConnectorType.AND)
        connectorBC2.append_operand(atomC, Sign.POSITIVE)
        connectorBC2.append_operand(atomB, Sign.POSITIVE)

        connectorBCorA = ConnectorNode(ConnectorType.OR)
        connectorBCorA.append_operand(connectorBC2, Sign.POSITIVE)
        connectorBCorA.append_operand(atom_a, Sign.POSITIVE)
        atomD.append_child(connectorBCorA, Sign.POSITIVE)

    def add_atom(self, node):
        self.root_node.append_operand(node, Sign.POSITIVE)

    def __repr__(self):
        str = "🌲🌲🌲 \033[92mTree representation\033[0m 🌲🌲🌲\n"
        return str + self.parse_full_node(self.root_node, 0, True)

    @staticmethod
    def parse_full_node(node, increment, force_node):
        if node.parsed and not force_node:
            return ""

        str = ' ' * increment +  node.__repr__() + '\n'
        if node.parsed:
            return str

        node.parsed = True
        if isinstance(node, ConnectorNode):
            for child in node.operands:
                str += Tree.parse_full_node(child, increment + (4 if isinstance(child, ConnectorNode) else 0), True)
        for child in node.children:
            str += Tree.parse_full_node(child, increment + 4, False)
        node.parsed = False
        return str


tree = Tree()
print(tree)
