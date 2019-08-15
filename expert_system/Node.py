from enum import Enum
import itertools


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

    def add_child(self, child):
        if child not in self.children:
            self.children.append(child)
        if self not in child.parents:
            child.parents.append(self)

    def parse_handler(self, node_handler, result_handler, negative, level, force_node):
        if not self.children.__len__():
            return ' ' * level + f'-{ self.node.__repr__()}\n'

        str = ' ' * level + "-\n"
        for child in self.children:
            str += child.parse_handler(node_handler, result_handler, True, level + 4, False)
        str += self.node.parse_handler(node_handler, result_handler, False, level, False)
        return str
        # return self.parse_handler(node_handler, result_handler, True, level, force_node)


class OperandState:
    def __init__(self, name, state):
        self.state = state
        self.name = name

    def __eq__(self, other):
        return self.name == other.name


# Need to keep in memory the replaced subsets (lets say we have A + B True and B + C True)
class ConnectorSimplifier:
    def __init__(self, type, operands):
        self.type = type
        self.operands = [OperandState(op.name, op.state) for op in operands]

    def replace(self, operands, value):
        name = ""
        # If value not found raise
        for op in operands:
            name += op.name
            self.operands.remove(op)
        self.operands.append(OperandState(name, value))

    def get_result(self):
        res = None
        for op in self.operands:
            if op.state is None:
                return None
            elif res is None:
                res = op.state
                continue
            elif self.type is ConnectorType.AND:
                res &= op.state
            elif self.type is ConnectorType.OR:
                res |= op.state
            elif self.type is ConnectorType.XOR:
                res ^= op.state
        return res


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
        self.parents = []
        self.visited = False
        self.state = False
        self.tree = tree
        self.negative = NegativeNode(self)

    def __repr_color__(self, str):
        if self.state is True:
            return f'\033[92m{str}\033[0m'
        elif self.state is False:
            return f'\033[91m{str}\033[0m'
        else:
            return f'\033[90m{str}\033[0m'

    # REDO REPR ################################
    def __full_repr__(self):
        self.parse(self.repr_node_handler, self.repr_result_handler)

    @staticmethod
    def repr_node_handler(node, negative, level):
        str = ' ' * level
        return str + node.__repr__() + "\n"

    @staticmethod
    def repr_result_handler(node, node_result, operand_results, children_results):
        str = node_result
        for res in operand_results:
            if res:
                str += res
        for res in children_results:
            if res:
                str += res
        return str
    # ##########################################

    def add_child(self, child):
        if child not in self.children:
            self.children.append(child)

    def set_status(self, status):
        self.state = status
        print(f'{ self.__repr__() } set to', status)
        return status

    def parse(self, node_handler, results_handler):
        """
            Because the nodes are interconnected in no particular order, we need a unique algorithm
            to parse the node children.

            This function is used mainly to
            - Print the node children
            - Resolve node values
        """

        return self.parse_handler(node_handler, results_handler, False, 0, True)

    def parse_handler(self, node_handler, result_handler, negative, level, force_node):
        children_res = []
        operands_res = []

        if self.visited and not force_node:
            return ""

        node_res = node_handler(self, negative, level)

        if self.visited:
            return node_res

        # Stop here if node is found but still do if printer

        if self.state is None:
            self.visited = True
            if isinstance(self, ConnectorNode):
                for child in self.operands:
                    operands_res.append(child.parse_handler(node_handler, result_handler, False, level + (4 if isinstance(child, ConnectorNode) else 0), True))
            for child in self.children:
                children_res.append(child.parse_handler(node_handler, result_handler, False, level + 4, False))
            # if self.negative.children.__len__():
            #     children_res.append(self.negative.parse_handler(node_handler, result_handler, True, level, False))  # Need to handle result better
            self.visited = False

        return result_handler(self, node_res, operands_res, children_res)

    def resolve(self):
        """ Returns and sets the current node state """
        return self.parse(self.resolve_node, self.resolve_results)

    @staticmethod
    def resolve_node(node, negative, level):
        print(f'Node { node.__repr__() } is', node.state)
        return node.state

    @staticmethod
    def resolve_results(node, node_res, operands_res, children_res):
        if node_res is not None:
            return node_res

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



                ### THIS WILL GO TO THE NEXT FUNCTION
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





                # IF NOT FOUND< WILL CHECK FOR
                # - ANY COMBINAISON OF OPERANDS SEPARATELY : (A + B + C) checks for (A + B) (B + C) (A + C) (A + B + C)
                # - WITH ANY OF THEIR CHILD for each case

                # We have to parse the list of connectors and set their state to visited
                # We can remove the child from connectors

                print("We try to complete the whole", node.operands)
                simplifier = ConnectorSimplifier(node.type, node.operands)
                for l in range(1, len(node.operands) + 1):
                    for subset in itertools.combinations(node.operands, l):





                        # IN the END INDIVIDUAL NODES SHOULD RESOLVE HERE
                        print("Will search the set:", subset)
                        simulated_connector = ConnectorNode(node.type, None)
                        simulated_connector.add_operands(subset)
                        try:
                            found_index = node.tree.connectors.index(simulated_connector)
                            node_state = node.tree.connectors[found_index].resolve()
                            if node_state:
                                simplifier.replace([OperandState(x.name, None) for x in subset], True)
                                result = simplifier.get_result()
                                if result is not None:
                                    return node.set_status(result)
                        except:
                            pass







                # It even if one node still remains none, we could potentially deduct it  // Or maybe not
                if found_none:
                    if node.type is ConnectorType.OR:
                        if res is False:
                            return node.set_status(None)
                    elif (node.type is ConnectorType.AND and res is True) or (node.type is ConnectorType.XOR):
                        return node.set_status(None)


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
            # if node.state is None and tested_parents is False:  # Find better way to check condition
            #     print("WILL CHECK FOR NODE PAERENTS")
            #     restart = False
            #     tested_parents = True
            #     for parent in node.parents:
            #         print("PARENT", parent.__repr__(), " Parsed ", parent.visited)
            #         # Need to handle negatives
            #         if parent.visited is False and parent.type is not ConnectorType.IMPLY:
            #             parent.resolve()

        return node.state


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

    def __repr__(self):
        return self.__repr_color__(f'({self.type.value})')

    def __eq__(self, other):
        if not isinstance(other, ConnectorNode):
            return False
        t = list(other.operands)  # make a mutable copy
        try:
            for elem in self.operands:
                t.remove(elem)
        except ValueError:
            return False
        return not t

    def add_child(self, child):
        if self.type is ConnectorType.IMPLY:
            raise BaseException("IMPLY Connectors can only have operands")
        super(ConnectorNode, self).add_child(child)

    def add_operand(self, operand):
        if self.type is ConnectorType.IMPLY and self.operands.__len__() > 0:
            raise BaseException("An imply connection must only have one operand")
        self.operands.append(operand)
        if self.type is not ConnectorType.IMPLY and self not in operand.parents:
            operand.parents.append(self)

    def add_operands(self, operands):
        [self.add_operand(op) for op in operands]

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
                    # if op.state is not self.state:
                        # raise ConfictError("XX was XXX and XXXX asked to be set to XXXXX")
                    op.state = self.state
        elif self.type is ConnectorType.OR:
            # Check for conflicts here too
            for i, op in enumerate(self.operands):
                if op.state is None:
                    none_index = i
                    none_number += 1
                    continue

                if total is None:
                    total = op.state
                else:
                    total |= op.state
            # Only if one is None then we can deduct
            if none_number is 1 and self.state is True and total is False:
                self.operands[none_index].set_status(True)


        # Try finding  common ft with OR
        elif self.type is ConnectorType.XOR:
            # Check for conflicts here too
            for i, op in enumerate(self.operands):
                if op.state is None:
                    none_index = i
                    none_number += 1
                    continue

                if total is None:
                    total = op.state
                elif op.state is not None:
                    total ^= op.state
            # Only if one is None then we can deduct
            if none_number is 1:
                self.operands[none_index].set_status(total ^ self.state)


            # Need OR and XOR cases
        return status


class AtomNode(Node):
    def __init__(self, name, tree):
        super(AtomNode, self).__init__(tree)
        self.name = name

    def __repr__(self):
        return self.__repr_color__(f'({self.name})')

    def __eq__(self, other):
        return isinstance(other, AtomNode) and self.name == other.name
