from expert_system.Tree import Tree
from expert_system.Node import AtomNode, ConnectorType, ConnectorNode

tree = Tree()
node_a = AtomNode("A")
node_b = AtomNode("B")
node_c = AtomNode("C")
node_or = ConnectorNode(ConnectorType.OR)
node_or.append_operands([node_a, node_b])
node_c.append_child(node_or)
tree.add_atom(node_a)
tree.add_atom(node_b)
print(tree.resolve_atom("C"))
