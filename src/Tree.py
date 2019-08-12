# Rename Tree class
from Node import AtomNode, ConnectorNode, ConnectorType, Sign


class Tree:
    def __init__(self):
        self.atoms = []
        self.root_node = ConnectorNode(ConnectorType.AND)

    def __repr__(self):
        return "🌲🌲🌲 \033[92mTree representation\033[0m 🌲🌲🌲\n" \
            + self.root_node.parse(self.repr_node_handler, self.repr_result_handler)

    def add_atom(self, node):
        if node not in self.atoms:
            self.root_node.append_operand(node)
            self.atoms.append(node)

    def add_fact(self, fact_name, value):
        for atom in self.atoms:
            if isinstance(atom, AtomNode) and atom.name is fact_name:
                atom.status = value

    def resolve_atom(self, atom_name):
        for atom in self.atoms:
            if isinstance(atom, AtomNode) and atom.name is atom_name:
                return atom.resolve()
        return False

    @staticmethod
    def repr_node_handler(node, negative, level):
        str = ' ' * level
        return str + node.__repr__() + "\n"

    @staticmethod
    def repr_result_handler(node, node_result, operand_results, children_results):
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
# tree.add_atom(atomY)


tree.add_atom(atomB)
tree.add_atom(atomC)
# tree.add_atom(atomD)
# tree.add_atom(atomE)

connectorBC = ConnectorNode(ConnectorType.AND)
connectorBC.append_operand(atomB)
# connectorBC.append_operand(atomB.negative)  # When the algo will check for incoherence it will bug here
connectorBC.append_operand(atomC)

# connectorBC.negative.append_child(atomE.negative) # TODO Badly printed
# connectorBC.append_child(atomE.negative)

# atom_a.append_child(atomY)
atom_a.append_child(connectorBC) # should print as -(A)
# atom_a.negative.append_child(connectorBC.negative)
# atomB.negative.append_child(atomY)

# connectorDE = ConnectorNode(ConnectorType.OR)
# connectorDE.append_operand(atomD)
# connectorDE.append_operand(atomE)
# atomB.append_child(connectorDE)
#
# atomC.append_child(atomB)
#
# connectorBC2 = ConnectorNode(ConnectorType.AND)
# connectorBC2.append_operand(atomC)
# connectorBC2.append_operand(atomB)
#
# connectorBCorA = ConnectorNode(ConnectorType.OR)
# connectorBCorA.append_operand(connectorBC2)
# connectorBCorA.append_operand(atom_a)
# atomD.append_child(connectorBCorA)

tree.add_fact("B", True)
tree.add_fact("C", True)
# tree.add_fact("A", True)

print(tree)

print("Final result:", tree.resolve_atom("A"))

print(tree)
