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
        connectorBC.append_operand(atomB, Sign.NEGATIVE)
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
        return str + self.root_node.parse(self.print_node_handler, self.print_node_children_handler)

    @staticmethod
    def print_node_handler(node, negative, level):
        str = ' ' * level * 4
        if (negative):
            str += '\033[91m-\033[0m'
        if isinstance(node, ConnectorNode):
            return str + '\033[95m' + node.__repr__() + '\033[0m\n'
        return str + '\033[94m' + node.__repr__() + '\033[0m\n'

    @staticmethod
    def print_node_children_handler(node, node_result, operand_results, children_results):
        str = node_result
        for res in operand_results:
            str += res
        for res in children_results:
            str += res
        return str

tree = Tree()
print(tree)
