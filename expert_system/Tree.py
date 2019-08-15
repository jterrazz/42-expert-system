from .Node import AtomNode, ConnectorNode, ConnectorType
import re
from .parsers.NPIParser import OPERATORS

LST_OP = {'+': ConnectorType.AND, '|': ConnectorType.OR, '^': ConnectorType.XOR}

# TODO Check for no duplicated also in the Conenctors


class Tree:
    """ A tree stores the state of the expert system based on rules, facts and queries """
    def __init__(self):
        self.atoms = []
        self.root_node = ConnectorNode(ConnectorType.AND, self)
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
        atom = AtomNode(name, self)
        self.add_atom(atom)
        return atom

    def create_connector(self, type):
        connector = ConnectorNode(type, self)
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
        print("\033[95mQUERY: Get the value of the fact", atom_name, "\033[0m")
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


class NPITree(Tree):
    def __init__(self, npi_rules, facts, queries):
        """
        Build a tree from NPI notation.
        - npi_rules formatted as "AB+"
        - facts formatted as ["A", "B"]
        """
        super(NPITree, self).__init__()
        self.good_atoms = {}
        self.good_connectors = []
        self.set_atoms(npi_rules)
        self.set_facts(facts, queries)
        self.set_node_relations(npi_rules)


    def set_atoms(self, npi_rules):
        for rule in npi_rules:
            atoms = list(re.sub(r'\+|\^|\||!', '', rule.npi_left))
            atoms += list(re.sub(r'\+|\^|\||!', '', rule.npi_right))
            self.good_atoms.update(dict((atom_str, self.create_atom(atom_str)) for atom_str in atoms))

    def set_node_relations(self, rules):
        print(self.good_atoms)

        if self.atoms.__len__() is 0:
            raise BaseException("The tree is empty")

        for rule in rules:
            stack = []

            # TODO Do same function for left and right
            # Handle only one and node
            for x in rule.npi_left:
                if x not in OPERATORS:
                    stack.append(self.good_atoms[x])
                else:
                    # TODO Later use not duplicated connectors
                    connector_x = self.create_connector(LST_OP[x])
                    # TODO Check if pop return not None
                    connector_x.append_operands([stack.pop(), stack.pop()])

                    # Put in right too
                    # TODO Check if infinite recursion can happen (if A child of B and B child of A)
                    try:
                        i = self.good_connectors.index(connector_x)
                        connector_x = self.good_connectors[i]
                    except:
                        self.good_connectors.append(connector_x)

                    stack.append(connector_x)
                    #handle !

            left_start = stack.pop()
            stack = []
            for x in rule.npi_right:
                if x not in OPERATORS:
                    stack.append(self.good_atoms[x])
                    if self.good_atoms[x].status is False:
                        self.good_atoms[x].status = None
                else:
                    # TODO Later use not duplicated connectors
                    connector_x = self.create_connector(LST_OP[x])
                    # TODO Check if pop return not None
                    connector_x.append_operands([stack.pop(), stack.pop()])

                    # Put in right too
                    # TODO Check if infinite recursion can happen (if A child of B and B child of A)
                    try:
                        i = self.good_connectors.index(connector_x)
                        connector_x = self.good_connectors[i]
                    except:
                        self.good_connectors.append(connector_x)

                    stack.append(connector_x)
            right_start = stack.pop()

            # TODO Handle EQUAL
            connector_imply = self.create_connector(ConnectorType.IMPLY)
            right_start.append_child(connector_imply)
            connector_imply.append_operand(left_start)

    def set_facts(self, facts, queries):
        # Set know fact atoms to True
        for fact in facts:
            self.add_fact(fact, True)
        # Set know other facts as false (if not in queries)
        for atom in self.atoms:
            if isinstance(atom, AtomNode) and atom.status is None and atom.name not in queries:
                atom.status = False
        return
