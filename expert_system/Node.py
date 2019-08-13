from enum import Enum


class ConnectorType(Enum):
    OR = '|'
    AND = '&'
    XOR = '^'
    IMPLY = '<='


# Not need anymore
class Sign(Enum):
    POSITIVE = "+"
    NEGATIVE = "-"


# Use common structure class with children and parents
class NegativeNode:
    def __init__(self, positive_node):
        self.node = positive_node
        self.children = []
        self.parents = []

    def append_child(self, child):
        if child not in self.children:
            self.children.append(child)
        if self not in child.parents:
            child.parents.append(self)

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
        self.parents = []
        self.parsed = 0
        self.status = None
        self.negative = NegativeNode(self)

    def append_child(self, child):
        if child not in self.children:
            self.children.append(child)
        if self not in child.parents:
            self.parents.append(self)

    def set_status(self, status):
        self.status = status
        print(f'{ self.__repr__() } is now', status)
        return status

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

        # Stop here if node is found

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
        print(f'Current node { node.__repr__() } is', node.status)
        return node.status

    @staticmethod
    def resolve_results(node, node_res, operands_res, children_res):
        # print("Resolving children", node.status)

        if node_res is not None:
            return node_res

        # Better tests
        restart = True
        tested_parents = False
        while restart:
            print("Resolving the node ", node.__repr__())
            restart = False
            # First try child results
            for child_res in children_res:
                if child_res is not None:
                    return node.set_status(child_res)
            print("BLYATTTT1")

            # Need refactoring
            # Next try from the operands
            if isinstance(node, ConnectorNode):
                res = None
                found_none = False
                print("BLYATTTT2")

                for op_res in operands_res:
                    # If none stop
                    print("BLYATTTT3")

                    # NEED TO CHECK ALL CHILDS ????? OR SIMPLY DON"T ALLOW MANY OPERANDS FOR THIS OP
                    if node.type is ConnectorType.IMPLY:
                        return node.set_status(True if (res is True) else None)

                    if op_res is None:
                        found_none = True
                        continue

                    if res is None:
                        res = op_res
                        continue

                    if node.type is ConnectorType.AND:
                        res &= op_res
                    elif node.type is ConnectorType.OR:
                        res |= op_res
                    elif node.type is ConnectorType.XOR:
                        res ^= op_res

                if found_none:
                    if node.type is ConnectorType.OR:
                        if res is False:
                            return node.set_status(None)
                    elif (node.type is ConnectorType.AND and res is True) or (node.type is ConnectorType.XOR):
                        return node.set_status(None)

                if res is not None:
                    return node.set_status(res)

            # Next try if a parent node
            if node.status is None and tested_parents is False:  # Find better way to check condition
                print("Node status is actually ", node.status, " and node will check for parents")

                # restart = True
                tested_parents = True
                for parent in node.parents:
                    print("CHECKING PARENT :", parent.__repr__())
                    # Need to handle negatives
                    if parent.parsed is False:
                        parent.parsed = True
                        parent.resolve()
                        parent.parsed = False
                print("ENDING CHECKING PARENTS: Node", node.__repr__())

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

    def set_status(self, status):
        super(ConnectorNode, self).set_status(status)

        # Pass result to children
        print("Will deduct node", self.__repr__())
        if status is True:
            print("WILL INDEEDDD   DEDUCT")
            if self.type is ConnectorType.AND:
                for op in self.operands:
                    # if op.status is not self.status:
                        # raise ConfictError("XX was XXX and XXXX asked to be set to XXXXX")
                    op.status = self.status
            # Need OR and XOR cases
        print("ENDED THE DEDUCTION")
        return status

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
