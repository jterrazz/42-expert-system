from expert_system.Tree import Tree
from expert_system.Node import AtomNode, NegativeNode, ConnectorNode, ConnectorType
#Use better comments  ??? Search what are docstring


class TreeFactory:
    '''
    A => B
    '''
    @staticmethod
    def get_ab():
        tree = Tree()
        node_a = AtomNode("A")
        node_b = AtomNode("B")
        node_b.append_child(node_a)
        tree.add_atom(node_a)
        tree.add_atom(node_b)
        return tree

    '''
    A | B => C
    '''
    @staticmethod
    def get_or_ab():
        tree = Tree()
        node_a = AtomNode("A")
        node_b = AtomNode("B")
        node_c = AtomNode("C")
        node_or = ConnectorNode(ConnectorType.OR)
        node_or.append_operands([node_a, node_b])
        node_c.append_child(node_or)
        tree.add_atoms([node_a, node_b, node_c])
        return tree

    '''
    A + B + C => D
    '''
    @staticmethod
    def get_and_abc():
        tree = Tree()
        node_a = AtomNode("A")
        node_b = AtomNode("B")
        node_c = AtomNode("C")
        node_d = AtomNode("D")
        tree.add_atoms([node_a, node_b, node_c, node_d])
        node_and = ConnectorNode(ConnectorType.AND)
        node_and.append_operands([node_a, node_b, node_c])
        node_d.append_child(node_and)
        return tree

    '''
    A | B | C => D
    '''
    @staticmethod
    def get_or_abc():
        tree = Tree()
        node_a = AtomNode("A")
        node_b = AtomNode("B")
        node_c = AtomNode("C")
        node_d = AtomNode("D")
        tree.add_atoms([node_a, node_b, node_c, node_d])
        node_and = ConnectorNode(ConnectorType.OR)
        node_and.append_operands([node_a, node_b, node_c])
        node_d.append_child(node_and)
        return tree

    '''
    A ^ B ^ C => D
    '''
    @staticmethod
    def get_xor_abc():
        tree = Tree()
        node_a = AtomNode("A")
        node_b = AtomNode("B")
        node_c = AtomNode("C")
        node_d = AtomNode("D")
        tree.add_atoms([node_a, node_b, node_c, node_d])
        node_and = ConnectorNode(ConnectorType.XOR)
        node_and.append_operands([node_a, node_b, node_c])
        node_d.append_child(node_and)
        return tree

    '''
    (A | B) | (B & C) => D
    '''
    @staticmethod
    def get_medium_0():
        tree = Tree()
        node_a = AtomNode("A")
        node_b = AtomNode("B")
        node_c = AtomNode("C")
        node_d = AtomNode("D")
        tree.add_atoms([node_a, node_b, node_c, node_d])
        node_or_0 = ConnectorNode(ConnectorType.OR)
        node_or_1 = ConnectorNode(ConnectorType.OR)
        node_and_0 = ConnectorNode(ConnectorType.AND)
        node_or_1.append_operands([node_a, node_b])
        node_and_0.append_operands([node_b, node_c])
        node_or_0.append_operands([node_or_1, node_and_0])
        node_d.append_child(node_or_0)
        return tree

    '''
    (A + B) => C
    D => (A + B)
    '''
    @staticmethod
    def get_hard_0():
        tree = Tree()
        node_a = AtomNode("A")
        node_b = AtomNode("B")
        node_c = AtomNode("C")
        node_d = AtomNode("D")
        tree.add_atoms([node_a, node_b, node_c, node_d])
        node_and_0 = ConnectorNode(ConnectorType.AND)
        node_and_0.append_operands([node_a, node_b])
        node_and_0.append_child(node_d)
        node_c.append_child(node_and_0)
        return tree
