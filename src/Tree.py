# Rename Tree class
from Node import AtomNode, ConnectorNode, ConnectorType, Sign


class Tree:
    def __init__(self):
        self.atoms = []
        self.root_node = ConnectorNode(ConnectorType.AND)

    def add_atom(self, node):
        self.root_node.append_operand(node, Sign.POSITIVE)

    def __repr__(self):
        str = "🌲🌲🌲 \033[92mTree representation\033[0m 🌲🌲🌲\n"
        return str + self.root_node.parse(self.print_node_handler, self.print_node_children_handler)

    @staticmethod
    def print_node_handler(node, negative, level):
        str = ' ' * level * 4
        if negative:
            str += '\033[97m!\033[0m'
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



# Example

tree = Tree()

atom_a = AtomNode('A')
atomB = AtomNode('B')
atomC = AtomNode('C')
atomD = AtomNode('D')
atomE = AtomNode('E')

tree.add_atom(atom_a)
tree.add_atom(atomB)
tree.add_atom(atomC)
tree.add_atom(atomD)
tree.add_atom(atomE)

connectorBC = ConnectorNode(ConnectorType.AND)
connectorBC.append_operand(atomB, Sign.POSITIVE)
connectorBC.append_operand(atomB, Sign.NEGATIVE)  # When the algo will check for incoherence it will bug here
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

print(tree)
