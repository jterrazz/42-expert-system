from enum import Enum
from expert_system.Log import Logger

logger = Logger("Node")


class ConnectorType(Enum):
    OR = '|'
    AND = '&'
    XOR = '^'
    IMPLY = '<='


class Node:
    """
    A Node is the main element stored in the tree. Each node is connected to each other in a parent/child relation.
    If we know the value of the child, we can deduct the value of the parent.
    For example, for the rule A => B, (A) is child of (=>) child of (B). By knowing A, we can deduct the parents values.
    """

    def __init__(self, tree):
        self.children = []
        self.operand_parents = []
        self.visited = False
        self.state = False
        self.state_fixed = False
        self.tree = tree

    def __repr_color__(self, str):
        if self.state is True:
            return f'\033[92m{str}\033[0m'
        elif self.state is False:
            return f'\033[91m{str}\033[0m'
        else:
            return f'\033[90m{str}\033[0m'

    def add_child(self, child):
        if child not in self.children:
            self.children.append(child)

    def set_status(self, status, is_fixed):
        if self.state_fixed is True and is_fixed is True and self.state is not None and self.state != status:
            raise BaseException("Confict")

        if self.state != status:
            logger.info(f'{self.__repr__()} set to {status}')

        self.state = status
        self.state_fixed = is_fixed
        return status

    def solve(self):
        if self.visited is True:
            return self.state

        state = None
        if self.state is not None:
            logger.info(f"{self} returns {self.state}")
            state = self.state
            if self.state_fixed is True:
                return state

        fixed_ret = []
        unfixed_ret = []

        logger.info(f"{self} will resolve from children {self.children}")
        f, u = self.solve_grouped_nodes(self.children, False)
        fixed_ret.extend(f)
        unfixed_ret.extend(u)

        logger.info(f"{self} will resolve from parents {self.operand_parents}")
        self.solve_grouped_nodes(self.operand_parents, True)

        ret = fixed_ret if fixed_ret.__len__() is not 0 else unfixed_ret
        if ret.__len__() is not 0:
            if True in ret:
                state = True
            else:
                state = False

        is_fixed = True if fixed_ret.__len__() is not 0 else False

        need_reverse = True
        if state is None:
            need_reverse = False
            state = self.state

        if state is not None:
            if isinstance(self, NegativeNode) and need_reverse:
                state = not state if state is not None else None
            return self.set_status(state, is_fixed)
        return None

    def solve_grouped_nodes(self, nodes, checking_parents):
        self.visited = True

        fixed_res = []
        unfixed_res = []
        for child in nodes:
            if checking_parents and isinstance(child, ConnectorNode) and child.type is not ConnectorType.AND:
                continue
            r = child.solve()
            if isinstance(self, NegativeNode) and isinstance(child, ConnectorNode) and child.type is ConnectorType.IMPLY and not checking_parents:
                r = not r if r is not None else None
            if r is not None and child.state_fixed:
                fixed_res.append(r)
            elif r is not None:
                unfixed_res.append(r)

        self.visited = False
        return fixed_res, unfixed_res


class NegativeNode(Node):
    def __init__(self, child):
        if child is None:
            raise BaseException("A negative node should have one child")

        super(NegativeNode, self).__init__(None)
        self.state = None
        self.add_child(child)

    def __repr__(self):
        return self.__repr_color__(f"!{ self.children[0] }")

    def add_child(self, child):
        super(NegativeNode, self).add_child(child)
        child.operand_parents.append(self)

    def set_status(self, status, is_fixed):
        res = super(NegativeNode, self).set_status(status, is_fixed)
        self.children[0].set_status(not res if res is not None else None, is_fixed)
        return res


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
        return self.__repr_color__(f'({self.type.value}) .operands: { self.operands }')

    def set_status(self, status, is_fixed):
        """ When a connector (&, |, ^) gets a value, we can sometimes deduct the value of its operands. """
        super(ConnectorNode, self).set_status(status, is_fixed)

        if self.type is ConnectorType.AND and status is True:
            for op in self.operands:
                op.set_status(status, is_fixed)
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
            return self.state

        logger.info(f"{self} will resolve from operands: {self.operands}")

        self.visited = True
        if self.type is ConnectorType.IMPLY:
            ret = self.operands[0].solve()
            self.set_status(ret, self.operands[0].state_fixed)
            self.visited = False
            return ret

        res = None
        found_none = False
        has_fixed_operands = False

        for op in self.operands:
            op_res = op.solve()
            if op.state_fixed is True:
                has_fixed_operands = True
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
            return self.set_status(res, has_fixed_operands)

        return super(ConnectorNode, self).solve()


class AtomNode(Node):
    def __init__(self, name, tree):
        super(AtomNode, self).__init__(tree)
        self.name = name

    def __repr__(self):
        return self.__repr_color__(f'({self.name})')

    def __eq__(self, other):
        return isinstance(other, AtomNode) and self.name == other.name
