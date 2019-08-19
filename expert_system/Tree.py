import re

from .Node import AtomNode, ConnectorNode, ConnectorType, NegativeNode
from .parser.Rule import OPERATORS, ImplicationType

LST_OP = {'+': ConnectorType.AND, '|': ConnectorType.OR, '^': ConnectorType.XOR}
REGEX_OP = r'\+|\^|\||!'


class TreeRelation:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"<TreeRelation> .left: {self.left}, .right: {self.right}"

    def validate(self):
        print("Validation")
        left = self.left.solve()
        right = self.right.solve()
        print("Left part is", left)
        print("Right part is", right)
        if left is True and right is False:
            raise BaseException("Error: There is a contradiction in the rules")


class Tree:
    """
    A tree stores the state of the expert system based on rules, facts and queries
    """

    def __init__(self):
        """
        Atoms store the list of UNIQUE elements. It means that the same instance of the Atom "A"
        will be used for all the equations.

        The root_node allows to connect all the nodes. It creates a unique tree for all the rules.
        """

        self.atoms = {}
        self.connectors = []
        self.implications = []
        self.root_node = ConnectorNode(ConnectorType.AND, self)
        self.root_node.parsed = True
        self.root_node.is_root = True

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
            self.root_node.add_operand(atom)
        return atom

    def create_connector(self, type):
        # TODO Probably need to store it like atoms else delete this function
        connector = ConnectorNode(type, self)
        return connector

    def set_atom_state(self, atom_name, value):
        atom = self.atoms.get(atom_name)
        if atom is None:
            raise BaseException("The fact", atom_name, " doesn't match any known atom")
        atom.state = value
        if value is True:
            atom.state_fixed = True

    def resolve_query(self, query):
        # if log
        print("\033[95mQUERY: Get the value of", query, "\033[0m")

        atom = self.atoms.get(query)
        if atom is None:
            raise BaseException("The query doesn't match any known atom")
        ret = atom.solve()
        self.validate_tree()
        return ret

    def validate_tree(self):
        for c in self.implications:
            c.validate()


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
            if rule.type is ImplicationType.EQUAL:
                atoms_in_conclusion += list(re.sub(REGEX_OP, '', rule.npi_left))

        for atom in atoms_in_conclusion:
            self.set_atom_state(atom, None)
        for fact in facts:
            self.set_atom_state(fact, True)

    def set_atoms_relations(self, rules):
        """
        Rules are formatted using the NPI notation.
        """
        if self.atoms.__len__() is 0:
            raise BaseException("The tree is empty")

        for rule in rules:
            left = self.set_atom_relations_from_npi(rule.npi_left)
            right = self.set_atom_relations_from_npi(rule.npi_right)

            connector_imply = self.create_connector(ConnectorType.IMPLY)
            right.add_child(connector_imply)
            connector_imply.add_operand(left)
            self.implications.append(TreeRelation(left, right))
            if rule.type is ImplicationType.EQUAL:
                connector_imply_1 = self.create_connector(ConnectorType.IMPLY)
                left.add_child(connector_imply_1)
                connector_imply_1.add_operand(right)
                self.implications.append(TreeRelation(right, left))

    def set_atom_relations_from_npi(self, npi_rule):
        stack = []

        for x in npi_rule:
            # TODO If operator == !, then use the negative version
            if x not in OPERATORS:
                stack.append(self.atoms[x])
            elif x == '!':
                child = stack.pop()
                connector_not = NegativeNode(child)
                child.operand_parents.append(connector_not)
                stack.append(connector_not)
            else:
                pop0 = stack.pop()
                pop1 = stack.pop()
                if isinstance(pop0, ConnectorNode) and pop0.type is LST_OP[x]:
                    pop0.add_operand(pop1)
                    new_connector = pop0
                    self.connectors.pop()
                elif isinstance(pop1, ConnectorNode) and pop1.type is LST_OP[x]:
                    pop1.add_operand(pop0)
                    new_connector = pop1
                    self.connectors.pop()
                else:
                    connector_x = self.create_connector(LST_OP[x])
                    connector_x.add_operands([pop0, pop1])
                    new_connector = connector_x
                self.connectors.append(new_connector)
                stack.append(new_connector)

        return stack.pop()
