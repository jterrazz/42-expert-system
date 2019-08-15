import re

from .Node import AtomNode, ConnectorNode, ConnectorType
from .parsers.NPIParser import OPERATORS

LST_OP = {'+': ConnectorType.AND, '|': ConnectorType.OR, '^': ConnectorType.XOR}
REGEX_OP = r'\+|\^|\||!'


class Tree:
    """
    A tree stores the state of the expert system based on rules, facts and queries
    """

    def __init__(self):
        """
        Atoms and connectors store the list of UNIQUE elements. It means that the same instance of the Atom "A"
        will be used for all the equations. It also means the same for connectors (A connector is considered equal
        if its operands are the same: (A & B) is the same as (B & A))

        The root_node allows to connect all the nodes. It creates a unique tree for all the rules.
        """

        self.atoms = {}
        self.connectors = []
        self.root_node = ConnectorNode(ConnectorType.AND, self)
        self.root_node.parsed = True

    def __repr__(self):
        return "🌲🌲🌲 \033[92mTree representation\033[0m 🌲🌲🌲\n" \
            + self.root_node.__full_repr__()

    def create_atom(self, atom_name):
        """
        Each new atom is stored inside a dictionary for convenience and also avoid duplication.
        """

        atom = self.atoms.get(atom_name)
        if atom is None:
            atom = AtomNode(atom_name, self)
            self.atoms[atom_name] = atom
            self.root_node.append_operand(atom)
        return atom

    def create_connector(self, type):
        # TODO Probably need to store it like atoms else delete this function
        connector = ConnectorNode(type, self)
        return connector

    def set_atom_state(self, atom_name, value):
        atom = self.atoms.get(atom_name)
        if atom is None:
            raise BaseException("The fact doesn't match any known atom")
        atom.state = value

    def resolve_query(self, query):
        # if log
        print("\033[95mQUERY: Get the value of", query, "\033[0m")

        atom = self.atoms.get(query)
        if atom is None:
            raise BaseException("The query doesn't match any known atom")
        return atom.resolve()


class NPITree(Tree):
    """
    Creates a tree from rules facts and queries
    """

    def __init__(self, npi_rules, facts, queries):
        """
        Rules must use the NPI notation (ex: AB+C|)
        Facts and queries must be represented as arrays of single characters (ex: Facts = ["A", "B"])
        """

        super(NPITree, self).__init__()
        self.create_atom_lst(npi_rules)
        self.set_atoms_state(npi_rules, facts, queries)
        self.set_atoms_relations(npi_rules)

    def create_atom_lst(self, npi_rules):
        for rule in npi_rules:
            atoms = list(re.sub(REGEX_OP, '', rule.npi_left))
            atoms += list(re.sub(REGEX_OP, '', rule.npi_right))
            self.atoms.update(dict((atom_str, self.create_atom(atom_str)) for atom_str in atoms))

    def set_atoms_state(self, npi_rules, facts, queries):
        """
        Atoms are by default False.
        If an atom is in the facts, its state becomes True.
        If an atom is in the conclusion side, its state becomes None (undefined).
        """

        atoms_in_conclusion = []
        for rule in npi_rules:
            atoms_in_conclusion += list(re.sub(REGEX_OP, '', rule.npi_right))
        for fact in facts:
            self.set_atom_state(fact, True)
        for atom in atoms_in_conclusion:
            self.set_atom_state(atom, None)

    def set_atoms_relations(self, rules):
        print(self.atoms)

        if self.atoms.__len__() is 0:
            raise BaseException("The tree is empty")

        for rule in rules:
            stack = []

            # TODO Do same function for left and right
            # Handle only one and node
            for x in rule.npi_left:
                if x not in OPERATORS:
                    stack.append(self.atoms[x])
                else:
                    # TODO Later use not duplicated connectors
                    connector_x = self.create_connector(LST_OP[x])
                    # TODO Check if pop return not None
                    connector_x.append_operands([stack.pop(), stack.pop()])

                    # Put in right too
                    # TODO Check if infinite recursion can happen (if A child of B and B child of A)
                    try:
                        i = self.connectors.index(connector_x)
                        connector_x = self.connectors[i]
                    except:
                        self.connectors.append(connector_x)

                    stack.append(connector_x)
                    #handle !

            left_start = stack.pop()
            stack = []
            for x in rule.npi_right:
                if x not in OPERATORS:
                    stack.append(self.atoms[x])
                    if self.atoms[x].state is False:
                        self.atoms[x].state = None
                else:
                    # TODO Later use not duplicated connectors
                    connector_x = self.create_connector(LST_OP[x])
                    # TODO Check if pop return not None
                    connector_x.append_operands([stack.pop(), stack.pop()])

                    # Put in right too
                    # TODO Check if infinite recursion can happen (if A child of B and B child of A)
                    try:
                        i = self.connectors.index(connector_x)
                        connector_x = self.connectors[i]
                    except:
                        self.connectors.append(connector_x)

                    stack.append(connector_x)
            right_start = stack.pop()

            # TODO Handle EQUAL
            connector_imply = self.create_connector(ConnectorType.IMPLY)
            right_start.append_child(connector_imply)
            connector_imply.append_operand(left_start)
