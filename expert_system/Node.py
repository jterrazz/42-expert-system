from enum import Enum
import itertools


class ConnectorType(Enum):
    OR = '|'
    AND = '&'
    XOR = '^'
    IMPLY = '<='


# # Use common structure class with children and parents
# class NegativeNode:
#     def __init__(self, positive_node):
#         self.node = positive_node
#         self.children = []
#         self.parents = []
#
#     def add_child(self, child):
#         if child not in self.children:
#             self.children.append(child)
#         if self not in child.parents:
#             child.parents.append(self)
#
#     def parse_handler(self, node_handler, result_handler, negative, level, force_node):
#         if not self.children.__len__():
#             return ' ' * level + f'-{ self.node.__repr__()}\n'
#
#         str = ' ' * level + "-\n"
#         for child in self.children:
#             str += child.parse_handler(node_handler, result_handler, True, level + 4, False)
#         str += self.node.parse_handler(node_handler, result_handler, False, level, False)
#         return str
#         # return self.parse_handler(node_handler, result_handler, True, level, force_node)


# class OperandState:
#     def __init__(self, name, state):
#         self.state = state
#         self.name = name
#
#     def __eq__(self, other):
#         return self.name == other.name
#
#     def __repr__(self):
#         return f"name: { self.name }, state: { self.state }"
#
#
# # Need to keep in memory the replaced subsets (lets say we have A + B True and B + C True)
# class ConnectorSimplifier:
#     def __init__(self, type, operands):
#         self.type = type
#         self.operands = [OperandState(op.name, op.state) for op in operands]
#
#     def replace(self, operands, value):
#         name = ""
#         # If value not found raise
#         for op in operands:
#             name += op.name
#             self.operands.remove(op)
#         print("Will simplify the subset", name, " with value", value)
#         self.operands.append(OperandState(name, value))
#
#     def get_result(self):
#         found_none = False
#         res = None
#
#         for op in self.operands:
#             if op.state is None:
#                 found_none = True
#                 continue
#             elif res is None:
#                 res = op.state
#                 continue
#             elif self.type is ConnectorType.AND:
#                 res &= op.state
#             elif self.type is ConnectorType.OR:
#                 res |= op.state
#             elif self.type is ConnectorType.XOR:
#                 res ^= op.state
#
#         if found_none:
#             if (self.type is ConnectorType.OR and res is False) or (self.type is ConnectorType.AND and res is True) or (self.type is ConnectorType.XOR):
#                 return None
#         print("Simplifier returns", res)
#         return res

# A => E
# X => A + C


# Rename parent to operand_parent (find the Real name maybe connector)
# Find example of a Connector that must be resolved thanks to its parent
class Node:
    """
    A Node is the main element stored in the tree. Each node is connected to each other in a parent/child relation.
    If we know the value of the child, we can deduct the value of the parent.
    For example, for the rule A => B, (A) is child of (=>) child of (B). By knowing A, we can deduct the parents values.
    """

    def __init__(self, tree):
        """ Children and parents must be unique """

        self.children = []
        self.operand_parents = []
        self.visited = False
        self.state = False
        self.tree = tree
        # self.negative = NegativeNode(self)

    def __repr_color__(self, str):
        if self.state is True:
            return f'\033[92m{str}\033[0m'
        elif self.state is False:
            return f'\033[91m{str}\033[0m'
        else:
            return f'\033[90m{str}\033[0m'

    def __full_repr__(self):
        # TODO
        return "Not implemented yet"

    def add_child(self, child):
        if child not in self.children:
            self.children.append(child)

    def set_status(self, status):
        self.state = status
        print(f'{ self.__repr__() } set to', status)
        return status

    def solve(self):
        if self.visited:
            return None
        if self.state is not None:
            print(self, "is", self.state)
            return self.state
        print(self, "search")

        ret = None
        self.visited = True
        full_children_ret = [child.solve() for child in self.children]
        resolved_children = [x for x in full_children_ret if x is not None]
        if resolved_children.__len__() is not 0:
            if all(x == resolved_children[0] for x in resolved_children):
                ret = resolved_children[0]
            else:
                raise BaseException("Resolution from children gave different results")
        self.visited = False

        if ret is not None:
            return self.set_status(ret)
        return self.deduct_from_parents()

    def deduct_from_parents(self):
        self.visited = True
        all_parents_ret = [parent.solve() for parent in self.operand_parents]
        resolved_parents = [x for x in all_parents_ret if x is not None]
        if resolved_parents.__len__() is not 0:
            if all(x == resolved_parents[0] for x in resolved_parents):
                ret = resolved_parents[0]
            else:
                raise BaseException("Resolution from children gave different results")
        else:
            ret = None
        self.visited = False
        return ret


class ConnectorNode(Node):
    """
    A connector node represents a relation in the set: AND, OR, XOR, IMPLY.
    You must differentiate the node operands from children.
    """

    def __init__(self, connector_type, tree):
        super(ConnectorNode, self).__init__(tree)
        self.type = connector_type
        self.operands = []
        self.state = None
        self.is_root = False

    def __repr__(self):
        return self.__repr_color__(f'({self.type.value})')

    # def __eq__(self, other):
    #     if not isinstance(other, ConnectorNode):
    #         return False
    #     t = list(other.operands)
    #     try:
    #         for elem in self.operands:
    #             t.remove(elem)
    #     except ValueError:
    #         return False
    #     return not t

    def set_status(self, status):
        super(ConnectorNode, self).set_status(status)

        # Here we'll set the operands deducted values
        if self.type is ConnectorType.AND:
            for op in self.operands:
                op.set_status(status)
        return status

    def add_operand(self, operand):
        if self.type is ConnectorType.IMPLY and self.operands.__len__() > 0:
            raise BaseException("An imply connection must only have one operand")
        self.operands.append(operand)
        if self.is_root is False and self.type is not ConnectorType.IMPLY and self not in operand.operand_parents:
            operand.operand_parents.append(self)

    def add_operands(self, operands):
        [self.add_operand(op) for op in operands]

    def solve(self):
        if self.visited:
            return None
        print(self, "resolving from operands:", self.operands)

        self.visited = True
        if self.type is ConnectorType.IMPLY:
            return self.operands[0].solve()

        res = None
        found_none = False

        for op in self.operands:
            op_res = op.solve()
            if op_res is None:
                found_none = True
                continue
            elif res is None:
                res = op_res
            elif self.type is ConnectorType.AND:
                res &= op_res
            elif self.type is ConnectorType.OR:
                res |= op_res
            elif self.type is ConnectorType.XOR:
                res ^= op_res

        self.visited = False

        if found_none and ((self.type is ConnectorType.OR and res is False) or\
                    (self.type is ConnectorType.AND and res is True) or\
                    (self.type is ConnectorType.XOR)):
            return None

        if res is not None:
            return self.set_status(res)

        return super(ConnectorNode, self).solve()




    # USE THIS IF OR IN CONCLUSION
    #     for l in range(1, len(node.operands) + 1):
    #         for subset in itertools.combinations(node.operands, l):


class AtomNode(Node):
    def __init__(self, name, tree):
        super(AtomNode, self).__init__(tree)
        self.name = name

    def __repr__(self):
        return self.__repr_color__(f'({self.name})')

    def __eq__(self, other):
        return isinstance(other, AtomNode) and self.name == other.name
