from expert_system.Tree import Tree
from expert_system.Node import AtomNode, ConnectorType, ConnectorNode

tree = Tree()
node_a = AtomNode("A")
node_b = AtomNode("B")
node_d = AtomNode("D")
imply_node = ConnectorNode(ConnectorType.IMPLY)
tree.add_atoms([node_a, node_b, node_d])
node_and_0 = ConnectorNode(ConnectorType.OR)
node_and_0.append_operands([node_a, node_b])
node_and_0.append_child(imply_node)
imply_node.append_operand(node_d)
tree.add_fact("D", True)
tree.add_fact("A", False)
assert tree.resolve_atom("B") is True
