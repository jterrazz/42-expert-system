from enum import Enum


class ConnectorType(Enum):
    OR = '|'
    AND = '&'
    XOR = '^'
    EQUIVALENCE = '<=>'
    IMPLICATION = '=>'


class NodeLink:
    def __init__(self, next_node, sign):
        self.node: next_node
        self.sign = sign


class Node:
    def __init__(self):
        self.nodes = []

    def append_node(self, node):
        self.nodes.append(node)


# A connector can be | & ^ -> <->
class ConnectorNode(Node):
    def __init__(self, connector_type):
        super(ConnectorNode, self).__init__() # TODO Not sure I need to call the parent init
        self.type = connector_type


class AtomNode(Node):
    def __init__(self, name):
        super(AtomNode, self).__init__() # TODO Not sure I need to call the parent init
        self.name = name
