from enum import Enum


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
        """ Children and parents must be unique """

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

    def __full_repr__(self):
        # TODO
        return "Not implemented yet"

    def add_child(self, child):
        if child not in self.children:
            self.children.append(child)

    def set_status(self, status, is_fixed):
        # TODO Add check if value was already set
        self.state = status
        self.state_fixed = is_fixed
        print(f'{ self.__repr__() } set to', status, f"(result is {is_fixed})")
        return status

    def solve(self):
        if self.visited is True:
            return None

        if self.state is not None:
            print(self, "is", self.state)
            return self.state
        print(self, "search, with children:", self.children)

        ret = None
        self.visited = True

        fixed_res = []
        unfixed_res = []

        for child in self.children:
            r = child.solve()
            if r is not None and child.state_fixed:
                fixed_res.append(r)
            elif r is not None:
                unfixed_res.append(r)

        res = fixed_res if fixed_res.__len__() is not 0 else unfixed_res
        if res.__len__() is not 0:
            # if all(x == res[0] for x in res):
                ret = res[0]
            # else:
                # raise BaseException("Resolution from children gave different results")

        self.visited = False

        if ret is not None:
            return self.set_status(ret, True)
        return self.deduct_from_parents()

    def deduct_from_parents(self):
        self.visited = True

        all_parents_ret = [parent.solve() for parent in self.operand_parents]
        resolved_parents = [x for x in all_parents_ret if x is not None]
        if resolved_parents.__len__() is not 0:
            if all(x == resolved_parents[0] for x in resolved_parents):
                ret = resolved_parents[0]
            else:
                raise BaseException("Resolution from parents gave different results")
        else:
            ret = None
        self.visited = False
        return ret


class NegativeNode(Node):
    def __init__(self, child):
        if child is None:
            raise BaseException("A negative node should have one child")

        super(NegativeNode, self).__init__(None)
        self.state = None
        self.add_child(child)

        # TODO Add a only one must be set assert
        # TODO Example: X =>  !A + B

    def __repr__(self):
        return self.__repr_color__(f"!{ self.children[0] }")

    def add_child(self, child):
        super(NegativeNode, self).add_child(child)
        child.operand_parents.append(self)

    def solve(self):
        res = super(NegativeNode, self).solve()
        return not res if res is not None else None

    def set_status(self, status, is_fixed):
        res = super(NegativeNode, self).set_status(status, is_fixed)
        # not value if value is not None else None
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
            return None
        print(self, "resolving from operands:", self.operands)

        self.visited = True
        if self.type is ConnectorType.IMPLY:
            ret = self.operands[0].solve()
            self.state_fixed = self.operands[0].state_fixed
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

        print("YOOOOO")

        if res is not None:
            return self.set_status(res, has_fixed_operands)

        return super(ConnectorNode, self).solve()


class AtomNode(Node):
    def __init__(self, name, tree):
        super(AtomNode, self).__init__(tree)
        self.name = name

    def __repr__(self):
        return self.__repr_color__(f'({self.name}, fixed:{self.state_fixed})')

    def __eq__(self, other):
        return isinstance(other, AtomNode) and self.name == other.name
