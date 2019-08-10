from enum import Enum


class ConnectorType(Enum):
    OR = '|'
    AND = '&'
    XOR = '^'
    NOT = '!'


class Sign(Enum):
    POSITIVE = "+"
    NEGATIVE = "-"


class Node:
    def __init__(self):
        self.children = []
        self.parsed = 0
        self.result = None
        self.negative_node = None

    def append_child(self, child, sign):
        if sign == Sign.NEGATIVE:
            if not self.negative_node:
                self.negative_node = ConnectorNode(ConnectorType.NOT)
            self.negative_node.children.append(child)
        else:
            self.children.append(child)

'''
A connector can be one of | & ^ -> <->
'''


class ConnectorNode(Node):
    def __init__(self, connector_type):
        super(ConnectorNode, self).__init__()
        self.type = connector_type
        self.operands = []

    def __repr__(self):
        return "Connector: " + self.type.value + "\n"

    def append_operand(self, child, sign):
        if sign == Sign.NEGATIVE:
            if not self.negative_node:
                self.negative_node = ConnectorNode(ConnectorType.NOT)
            self.negative_node.operands.append(child)
        else:
            self.operands.append(child)


class AtomNode(Node):
    def __init__(self, name):
        super(AtomNode, self).__init__()
        self.name = name

    def __repr__(self):
        return "Atom: " + self.name + "\n"
