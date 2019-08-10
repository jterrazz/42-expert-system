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

    def parse(self, node_handler, child_results_handler):
        return self.parse_handler(node_handler, child_results_handler, 0, True)

    def parse_handler(self, node_handler, result_handler, level, force_node):
        if self.parsed and not force_node:
            return ""

        node_result = node_handler(self, level)
        if self.parsed:
            return node_result

        self.parsed = True
        child_results = []
        operand_results = []
        if isinstance(self, ConnectorNode):
            for child in self.operands:
                operand_results.append(child.parse_handler(node_handler, result_handler, level + (1 if isinstance(child, ConnectorNode) else 0), True))
        for child in self.children:
            child_results.append(child.parse_handler(node_handler, result_handler, level + 1, False))
        self.parsed = False

        return result_handler(self, node_result, operand_results, child_results)

'''
A connector can be one of | & ^ -> <->
'''


class ConnectorNode(Node):
    def __init__(self, connector_type):
        super(ConnectorNode, self).__init__()
        self.type = connector_type
        self.operands = []

    def __repr__(self):
        return f'({self.type.value})'

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
        return f'({self.name})'
