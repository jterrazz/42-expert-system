from expert_system.Tree import Tree
from expert_system.Node import AtomNode, ConnectorType, ConnectorNode

tree = Tree()
node_a = AtomNode("A")
node_b = AtomNode("B")
node_c = AtomNode("C")
node_d = AtomNode("D")
tree.add_atoms([node_a, node_b, node_c, node_d])
node_or_0 = ConnectorNode(ConnectorType.OR)
node_or_0.append_operands([node_a, node_b])

d_imply = ConnectorNode(ConnectorType.IMPLY)
node_or_0.append_child(d_imply)
d_imply.append_child(node_d)

c_imply = ConnectorNode(ConnectorType.IMPLY)
c_imply.append_child(node_or_0)
node_c.append_child(c_imply)
tree.add_fact("D", False)
assert tree.resolve_atom("A") is None
assert tree.resolve_atom("B") is None
assert tree.resolve_atom("C") is None
