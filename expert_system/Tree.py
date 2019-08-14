from .Node import AtomNode, ConnectorNode, ConnectorType


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
            raise BaseException("Node was already created")

    def add_atoms(self, nodes):
        for node in nodes:
            self.add_atom(node)

    """
    Build helpers
    """

    def create_atom(self, name):
        atom = AtomNode(name)
        self.add_atom(atom)
        return atom

    def create_connector(self, type):
        connector = ConnectorNode(type)
        # TODO Probably need to save connectors in list
        return connector

    def add_fact(self, fact_name, value):
        # TODO Check for duplications
        for atom in self.atoms:
            if isinstance(atom, AtomNode) and atom.name is fact_name:
                atom.status = value

    """
    Resolver
    """

    def resolve_atom(self, atom_name):
        print("WILL RESOLVE ATOM", atom_name)
        for atom in self.atoms:
            if isinstance(atom, AtomNode) and atom.name is atom_name:
                return atom.resolve()
        return None





    # TODO MOVE THIS

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


"""
Build a tree from NPI notation.
- npi_rules formatted as "AB+"
- facts formatted as ["A", "B"]
"""


class NPITree(Tree):
    def __init__(self, npi_rules, facts):
        super(NPITree, self).__init__()
        self.init_nodes(npi_rules)
        self.set_facts(facts)

    def init_nodes(self, rules):
        ########################################
        # TMP Example for: ((A + B + C) | D) => E
        ########################################

        atom_a = self.create_atom("A")
        atom_b = self.create_atom("B")
        atom_c = self.create_atom("C")
        atom_d = self.create_atom("D")
        atom_e = self.create_atom("E")

        connector_and_abc = self.create_connector(ConnectorType.AND)
        connector_and_abc.append_operands([atom_a, atom_b, atom_c])
        # Or
        # connector_and_abc.append_operand(atom_a)
        # connector_and_abc.append_operand(atom_b)
        # connector_and_abc.append_operand(atom_c)

        connector_or = self.create_connector(ConnectorType.OR)
        connector_or.append_operands([connector_and_abc, atom_d])

        # Each imply connector must be unique
        connector_imply = self.create_connector(ConnectorType.IMPLY)
        atom_e.append_child(connector_imply)
        connector_imply.append_operand(connector_or)

        ########################################
        ########################################
        ########################################

        if self.atoms.__len__() is 0:
            raise BaseException("The tree is empty")

    def set_facts(self, facts):
        for fact in facts:
            self.add_fact(fact, True)
        return
