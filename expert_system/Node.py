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
        self.status = None
        self.negative = NegativeNode(self)

    def append_child(self, child):
        self.children.append(child)

    def set_status(self, status):
        self.status = status

    '''
    Recursive parser, used for
    - Printing the node children
    - Resolving node values
    
    node_handler() is executed for each node, and the children result is passed to the results_handler()
    The level parameter represents the depth of the node.
    '''

    def parse(self, node_handler, results_handler):
        return self.parse_handler(node_handler, results_handler, False, 0, True)

    # Node handler could be a self class
    # Rename to node_res, operands_res, children_res
    def parse_handler(self, node_handler, result_handler, negative, level, force_node):
        if self.parsed and not force_node:
            return ""

        node_result = node_handler(self, negative, level)
        if self.parsed:
            return node_result

        child_results = []
        operand_results = []

        if self.status is None:
            self.parsed = True
            if isinstance(self, ConnectorNode):
                for child in self.operands:
                    operand_results.append(child.parse_handler(node_handler, result_handler, False, level + (4 if isinstance(child, ConnectorNode) else 0), True))
            for child in self.children:
                child_results.append(child.parse_handler(node_handler, result_handler, False, level + 4, False))
            if self.negative.children.__len__():
                child_results.append(self.negative.parse_handler(node_handler, result_handler, True, level, False))  # Need to handle result better
            self.parsed = False

        return result_handler(self, node_result, operand_results, child_results)

    '''
    The function uses the parse method ... etc
    '''

    def resolve(self):
        return self.parse(self.resolve_node, self.resolve_results)

    @staticmethod
    def resolve_node(node, negative, level):
        print("resolving node", node.status)
        return node.status

    @staticmethod
    def resolve_results(node, node_res, operands_res, children_res):
        # print("Resolving children", node.status)

        for child_res in  children_res:
            if child_res is not None:
                node.status = child_res
                return node.status

        # Need refactoring
        if isinstance(node, ConnectorNode):
            res = None
            found_none = False
            for op_res in operands_res:
                # If none stop

                if res is None:
                    res = op_res
                    continue

                if op_res is None:
                    found_none = True
                    continue

                if node.type is ConnectorType.AND:
                    res &= op_res
                elif node.type is ConnectorType.OR:
                    res |= op_res
                else:
                    res ^= op_res

            if found_none:
                if node.type is ConnectorType.OR and res is False:
                    node.status = None
                    return node.status
                elif node.type is ConnectorType.AND or node.type is ConnectorType.XOR:
                    node.status = None
                    return node.status

            node.status = res
            return res

        # Set node.status if children give it
        print("Resolved children", node.status)

        return node.status

'''
A connector can be one of | & ^ -> <->
'''


class ConnectorNode(Node):
    def __init__(self, connector_type):
        super(ConnectorNode, self).__init__()
        self.type = connector_type
        self.operands = []

    def __repr__(self):
        return repr_node_status(f'({self.type.value})', self.status)

    def append_operand(self, operand):
        self.operands.append(operand)

    def append_operands(self, operands):
        for op in operands:
            self.append_operand(op)


class AtomNode(Node):
    def __init__(self, name):
        super(AtomNode, self).__init__()
        self.name = name

    def __repr__(self):
        return repr_node_status(f'({self.name})', self.status)

# Put in class
def repr_node_status(str, value):
    if value is True:
        return f'\033[92m{ str }\033[0m'
    elif value is False:
        return f'\033[91m{ str }\033[0m'
    else:
        return f'\033[90m{ str }\033[0m'
