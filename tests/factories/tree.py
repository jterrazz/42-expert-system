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
