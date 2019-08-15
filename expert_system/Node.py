from enum import Enum
from expert_system.helpers.Error import TreeError


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


# Rename parent to operand_parent (find the Real name maybe connector)
class Node:
    def __init__(self, tree):
        self.children = []
        self.parents = []
        self.parsed = False
        self.status = None
        self.tree = tree
        self.negative = NegativeNode(self)

    def append_child(self, child):
        if child not in self.children:
            self.children.append(child)

    def set_status(self, status):
        self.status = status
        print(f'{ self.__repr__() } set to', status)
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
        print(f'Node { node.__repr__() } is', node.status)
        return node.status

    @staticmethod
    def resolve_results(node, node_res, operands_res, children_res):
        # print("Resolving children", node.status)

        if node_res is not None:
            return node_res

        # Better tests
        # RESTART CANT HAPPEND HERE
        restart = True
        tested_parents = False

        while restart:
            restart = False
            # First try child results
            for child_res in children_res:
                if child_res is not None:
                    return node.set_status(child_res)

            # Need refactoring
            # Next try from the operands

            if isinstance(node, ConnectorNode):
                res = None
                found_none = False

                for op_res in operands_res:
                    # If none stop

                    # NEED TO CHECK ALL CHILDS ????? OR SIMPLY DON"T ALLOW MANY OPERANDS FOR THIS OP
                    if node.type is ConnectorType.IMPLY:
                        return node.set_status(op_res)
                        # return node.set_status(True if (op_res is True) else None)

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


                # Will check here  for similar Connectors nodes based on childs
                # for op in node.operands:
                #     for child in op_res






                if res is not None:
                    return node.set_status(res)

                # Check for similar connectors based on operand children
                # # If it's NPI tree
                # Maybe delete tree reference from Node Class
                # if node.type is not ConnectorType.IMPLY:
                    # for connector in node.tree.good_connectors:
                    #     for child in node.children:
                    #         if
                    # for op in node.operands:



            # Next try if a parent node
            # if node.status is None and tested_parents is False:  # Find better way to check condition
            #     print("WILL CHECK FOR NODE PAERENTS")
            #     restart = False
            #     tested_parents = True
            #     for parent in node.parents:
            #         print("PARENT", parent.__repr__(), " Parsed ", parent.parsed)
            #         # Need to handle negatives
            #         if parent.parsed is False and parent.type is not ConnectorType.IMPLY:
            #             parent.resolve()

        return node.status

'''
A connector can be one of | & ^ -> <->
'''


class ConnectorNode(Node):
    def __init__(self, connector_type, tree):
        super(ConnectorNode, self).__init__(tree)
        self.type = connector_type
        self.operands = []

    def __eq__(self, other):
        # TODO Maybe check if both classes are operands
        return tuple(self.operands) == tuple(other.operands) and self.type is other.type

    def __repr__(self):
        return repr_node_status(f'({self.type.value})', self.status)

    def append_child(self, child):
        if self.type is ConnectorType.IMPLY:
            raise BaseException("Implications child must set as an operand")
        super(ConnectorNode, self).append_child(child)

    def append_operand(self, operand):
        if self.type is ConnectorType.IMPLY and self.operands.__len__() > 0:
            raise BaseException("An imply connection must only have one operand")
        self.operands.append(operand)

        # PROBABLY ADD NO CONDITION FOR IMPLICATION
        if self not in operand.parents:
            operand.parents.append(self)

    def append_operands(self, operands):
        for op in operands:
            self.append_operand(op)

    def set_status(self, status):
        super(ConnectorNode, self).set_status(status)

        if status is None:
            return status

        total = None
        none_number = 0
        none_index = 0

        # GET RECURSIVELY THEIR VALUE FOR ALL OPERANDS WITH THE 3 TYPES AND FIND UNIT TEST FOR IT !!!!!!!!!!

        # Pass result to children
        if self.type is ConnectorType.AND:
            if status is True:
                for op in self.operands:
                    # if op.status is not self.status:
                        # raise ConfictError("XX was XXX and XXXX asked to be set to XXXXX")
                    op.status = self.status
        elif self.type is ConnectorType.OR:
            # Check for conflicts here too
            for i, op in enumerate(self.operands):
                if op.status is None:
                    none_index = i
                    none_number += 1
                    continue

                if total is None:
                    total = op.status
                else:
                    total |= op.status
            # Only if one is None then we can deduct
            if none_number is 1 and self.status is True and total is False:
                self.operands[none_index].set_status(True)


        # Try finding  common ft with OR
        elif self.type is ConnectorType.XOR:
            # Check for conflicts here too
            for i, op in enumerate(self.operands):
                if op.status is None:
                    none_index = i
                    none_number += 1
                    continue

                if total is None:
                    total = op.status
                elif op.status is not None:
                    total ^= op.status
            # Only if one is None then we can deduct
            if none_number is 1:
                self.operands[none_index].set_status(total ^ self.status)


            # Need OR and XOR cases
        return status

class AtomNode(Node):
    def __init__(self, name, tree):
        super(AtomNode, self).__init__(tree)
        self.name = name

    # def __eq__(self, other):
    #     return self.name == other.name

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
