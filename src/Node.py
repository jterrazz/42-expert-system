from enum import Enum


class ConnectorType(Enum):
    OR = '|'
    AND = '&'
    XOR = '^'


# Not need anymore
class Sign(Enum):
    POSITIVE = "+"
    NEGATIVE = "-"


class NegativeNode:
    def __init__(self, positive_node):
        self.node = positive_node
        self.children = []

    def append_child(self, child):
        self.children.append(child)

    # Add the negative state here
    def parse_handler(self, node_handler, result_handler, negative, level, force_node):
        if not self.children.__len__():
            return ' ' * level + f'-{ self.node.__repr__()}\n'

        str = ' ' * level + "-\n"
        for child in self.children:
            str += child.parse_handler(node_handler, result_handler, True, level + 4, False)
        str += self.node.parse_handler(node_handler, result_handler, False, level, False)
        return str
        # return self.parse_handler(node_handler, result_handler, True, level, force_node)


class Node:
    def __init__(self):
        self.children = []
        self.parsed = 0
        self.result = None
        self.negative = NegativeNode(self)

    def append_child(self, child):
        self.children.append(child)

    def parse(self, node_handler, child_results_handler):
        return self.parse_handler(node_handler, child_results_handler, False, 0, True)

    def parse_handler(self, node_handler, result_handler, negative, level, force_node):
        if self.parsed and not force_node:
            return ""

        node_result = node_handler(self, negative, level)
        if self.parsed:
            return node_result

        self.parsed = True
        child_results = []
        operand_results = []
        if isinstance(self, ConnectorNode):
            for child in self.operands:
                operand_results.append(child.parse_handler(node_handler, result_handler, False, level + (4 if isinstance(child, ConnectorNode) else 0), True))
        for child in self.children:
            child_results.append(child.parse_handler(node_handler, result_handler, False, level + 4, False))
        if self.negative.children.__len__():
            child_results.append(self.negative.parse_handler(node_handler, result_handler, True, level, False)) # Need to handle result better
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

    def append_operand(self, child):
        self.operands.append(child)


class AtomNode(Node):
    def __init__(self, name):
        super(AtomNode, self).__init__()
        self.name = name

    def __repr__(self):
        return f'({self.name})'
