from enum import Enum


class ConnectorType(Enum):
    OR = '|'
    AND = '&'
    XOR = '^'
    # EQUIVALENCE = '<=>'
    # IMPLICATION = '=>'


class Sign(Enum):
    POSITIVE = "+"
    NEGATIVE = "-"


class NodeLink:
    def __init__(self, next_node, sign):
        self.node = next_node
        self.sign = sign


# If connector, then first check if the connector can be deduced entirely and then do each element
#  Make a graph to explain that
class Node:
    def __init__(self):
        self.children = []
        self.parsed = 0
        self.result = None

    def append_child(self, node, sign):
        child = NodeLink(node, sign)
        self.children.append(child)

    # !!! Cas ou l'atom recherché est aussi dans un connecteur dès le début. Donc si un connector existe en tant que parent, tester ses regles pour en deduire le resultat

    # If is connector  need to save it and print only if there are childs available, expects the 3 cases below.
    # Need to delete a chain of connector if no condition available at the bottom

    # Simple solution for following: For connector_children we have to put them even if we printed them already
    # TODO Create an example doing that
    # If OR and there is one child avaiable put it
    # If AND and one is missing, remove the entire AND
    # If XOR and one child was already parsed, put it anyway but don't go further (because we can maybe deduce )
    # if isinstance(node, ConnectorNode):
    #     if node.type == ConnectorType.AND:
    #         return ""
    #
    # if children_str != "":
    #     return node_str + children_str
    # return node_str

    # def __repr__(self):
    #     print()
    #
    # @staticmethod
    # def node_repr_handler(node, children_result):
    #
    #
    # @staticmethod
    # def node_repr_stop_condition(node, child):
    #     if (node.parsed > 1)
    #         return True
    #
    # @staticmethod
    # def node_line_repr(node, level):
    #     node_str = ' ' * (level - 1) * 4
    #
    #     if level:
    #         node_str += "<== "
    #     node_str += "(" + (node.name if isinstance(node, AtomNode) else node.type.value) + ")\n"
    #
    #     return node_str
    #  No static
    # @staticmethod
    # def parse_node(node, level, handler, stop_condition):
    #     children_result = []
    #     node.parsed += 1
    #
    #     for child in node.children:
    #         if not stop_condition(node, child.node):  ## Replace by can_contain_result
    #             children_result.append(Node.parse_node(child.node, level, handler, stop_condition))
    #
    #     node.parsed -= 1
    #     return handler(node, children_result)


# A connector can be | & ^ -> <->
# XOR with 3 elements is possible ?
class ConnectorNode(Node):
    def __init__(self, connector_type):
        super(ConnectorNode, self).__init__()
        self.type = connector_type
        self.connector_nodes = []

    def append_connector_nodes(self, child, sign):
        link = NodeLink(child, sign)
        self.connector_nodes.append(link)

    # def set_connector_result(self):
    #     for node in self.connector_nodes:
    #         # We can probably use a while () WIth the real sign ^ | & BUT we also have to check for None != False !!!!!!
    #         if self.type == ConnectorType.OR and node.result:
    #             # Need to check all fucking nodes
    #             self.result = False # Change
    #             return
    #         elif self.type == ConnectorType.XOR and node.result != None:
    #             # Need to check all fucking nodes
    #             self.result = False # Change
    #             return
    #             # Set the other nodes to the deduced value
    #         elif self.type == ConnectorType.AND:
    #             self.result = False # Equal to the combined results
    #     return  self.result


class AtomNode(Node):
    def __init__(self, name):
        super(AtomNode, self).__init__()
        self.name = name
