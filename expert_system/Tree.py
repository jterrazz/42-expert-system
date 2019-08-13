# Rename Tree class
from .Node import AtomNode, ConnectorNode, ConnectorType
from expert_system.helper.Error import TreeError
# Find a python already made error class ???




# TODO Check for no duplicated also in the Conenctors
# TODO Do methods for create Atom in tree
class Tree:
    def __init__(self):
        self.atoms = []
        self.root_node = ConnectorNode(ConnectorType.AND)
        self.root_node.parsed = True

    def __repr__(self):
        return "🌲🌲🌲 \033[92mTree representation\033[0m 🌲🌲🌲\n" \
            + self.root_node.parse(self.repr_node_handler, self.repr_result_handler)

    def add_atom(self, node):
        if node not in self.atoms:
            self.root_node.append_operand(node)
            self.atoms.append(node)
        else:
            raise TreeError("Node was already created")

    def add_atoms(self, nodes):
        for node in nodes:
            self.add_atom(node)

    def add_fact(self, fact_name, value):
        for atom in self.atoms:
            if isinstance(atom, AtomNode) and atom.name is fact_name:
                atom.status = value

    def resolve_atom(self, atom_name):
        print("WILL RESOLVE ATOM", atom_name)
        for atom in self.atoms:
            if isinstance(atom, AtomNode) and atom.name is atom_name:
                return atom.resolve()
        return None

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
