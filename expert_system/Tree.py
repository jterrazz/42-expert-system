from .Node import AtomNode, ConnectorNode, ConnectorType
import re
from .parsers.NPIParser import OPERATORS


LST_OP = {'+': ConnectorType.AND, '|': ConnectorType.OR, '^': ConnectorType.XOR}

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


"""
Build a tree from NPI notation.
- npi_rules formatted as "AB+"
- facts formatted as ["A", "B"]
"""


class NPITree(Tree):
    def __init__(self, npi_rules, facts, queries):
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
        ########################################
        # TMP Example for: !((A + B + C) | D) => !E

        # atom_a = self.create_atom("A")
        # atom_b = self.create_atom("B")
        # atom_c = self.create_atom("C")
        # atom_d = self.create_atom("D")
        # atom_e = self.create_atom("E")
        #
        # connector_and_abc = self.create_connector(ConnectorType.AND)
        # connector_and_abc.append_operands([atom_a, atom_b, atom_c])
        # Or
        # connector_and_abc.append_operand(atom_a)
        # connector_and_abc.append_operand(atom_b)
        # connector_and_abc.append_operand(atom_c)

        # connector_or = self.create_connector(ConnectorType.OR)
        # connector_or.append_operands([connector_and_abc, atom_d])

        # Each imply connector must be unique
        # connector[_imply = self.create_connector(ConnectorType.IMPLY)
        # atom_e.append_child(connector_imply)
        # connector_imply.append_operand(connector_or)

        ########################################
        ########################################
        ########################################

        # tmp = 'A'
        # connector_and_ab = self.create_connector(ConnectorType.AND)
        # connector_and_ab.append_operands([self.good_atoms[tmp], self.good_atoms['B']])
        # connector_imply_ab = self.create_connector(ConnectorType.IMPLY)
        # self.good_atoms['C'].append_child(connector_imply_ab)
        # connector_imply_ab.append_operand(connector_and_ab)
        #
        # connector_and_de = self.create_connector(ConnectorType.AND)
        # connector_and_de.append_operands([self.good_atoms['D'], self.good_atoms['E']])
        # connector_imply_de = self.create_connector(ConnectorType.IMPLY)
        # self.good_atoms['F'].append_child(connector_imply_de)
        # connector_imply_de.append_operand(connector_and_de)

        if self.atoms.__len__() is 0:
            raise BaseException("The tree is empty")

        """
        A ^ B = > C  # A and B are True, so C is False
        D ^ E = > F  # Only D is True, so F is True
        G ^ H = > I  # Only H is True, so I is True
        J ^ K = > L  # J and K are False, so J is False

        =ABDH
        ?CFIL
        """
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


            """
            A => E
            D => A | B
            
            =D
            ?E
            
            """
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
