# Rename Tree class
from Node import AtomNode, ConnectorNode, ConnectorType, Sign


class Tree:
    def __init__(self):
        self.atoms = []
        self.root_node = ConnectorNode(ConnectorType.AND)

    def add_atom(self, node):
        self.root_node.append_operand(node)

    def __repr__(self):
        str = "🌲🌲🌲 \033[92mTree representation\033[0m 🌲🌲🌲\n"
        return str + self.root_node.parse(self.print_node_handler, self.print_node_children_handler)

    @staticmethod
    def print_node_handler(node, negative, level):
        str = ' ' * level
        # if negative:
        #     str += '\033[97m!\033[0m'
        if isinstance(node, ConnectorNode):
            return str + '\033[95m' + node.__repr__() + '\033[0m\n'
        return str + '\033[94m' + node.__repr__() + '\033[0m\n'

    @staticmethod
    def print_node_children_handler(node, node_result, operand_results, children_results):
        str = node_result
        for res in operand_results:
            if res:
                str += res
        for res in children_results:
            if res:
                str += res
        return str



# Example

tree = Tree()

atom_a = AtomNode('A')
atomB = AtomNode('B')
atomC = AtomNode('C')
atomD = AtomNode('D')
atomE = AtomNode('E')
atomY = AtomNode('Y')

tree.add_atom(atom_a)
tree.add_atom(atomB)
tree.add_atom(atomC)
tree.add_atom(atomD)
tree.add_atom(atomE)

connectorBC = ConnectorNode(ConnectorType.AND)
connectorBC.append_operand(atomB)
connectorBC.append_operand(atomB.negative)  # When the algo will check for incoherence it will bug here
connectorBC.append_operand(atomC)

connectorBC.negative.append_child(atomE.negative) # TODO Badly printed
connectorBC.append_child(atomE.negative)

# atom_a.negative.append_child(connectorBC) # should print as -(A)
atom_a.negative.append_child(connectorBC.negative)
# atomB.negative.append_child(atomY)

connectorDE = ConnectorNode(ConnectorType.OR)
connectorDE.append_operand(atomD)
connectorDE.append_operand(atomE)
atomB.append_child(connectorDE)

atomC.append_child(atomB)

connectorBC2 = ConnectorNode(ConnectorType.AND)
connectorBC2.append_operand(atomC)
connectorBC2.append_operand(atomB)

connectorBCorA = ConnectorNode(ConnectorType.OR)
connectorBCorA.append_operand(connectorBC2)
connectorBCorA.append_operand(atom_a)
atomD.append_child(connectorBCorA)

print(tree)
