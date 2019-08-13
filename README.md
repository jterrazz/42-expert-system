# 42-expert-system

> Python implementation of a backward chaining inference engine.


Put in requirment.txt:
> pip install -U pytest
>
>python3 -m pytest -v

## Presentation

The project receives an **input file** as the first parameter.

The file should describe a set of rules, initial facts and queries.

```
# Example of input file

# Rules and symbols
C           => E        # C implies E
A + B + C   => D        # A and B and C implies D
A | B       => C        # A or B implies C
A + !B      => F        # A and not B implies F
C | !G      => H        # C or not G implies H
V ^ W       => X        # V xor W implies X
A + B       => Y + Z    # A and B implies Y and Z
C | D       => X | V    # C or D implies X or V
E + F       => !V       # E and F implies not V
A + B       <=> C       # A and B if and only if C
A + B       <=> !C      # A and B if and only if not C

# Initial facts
= ABG

# Queries
?GVX
```

## Implementation

### Project files structure

```
README.md
/src
    Node.py # With Connector and Atom nodes
    Tree.py #
```

### Data structure

A **tree** represents a set of rules. It is composed of nodes divided in two types : `ConnectorNode` and `AtomNode`. They are linked with `NodeLink` instances.

#### The node class

Both of `ConnectorNode` and `AtomNode` share the `Node` class. Each node instance can have **many children** (saved in`node_instance.children` ). A child can have a negative relation to its parent, for example in `!A = B`. The `NodeLink` class is used to represent this relation between two nodes. This process is abstracted and you can follow the example below.

A child represents the left part of the equation. So **if one a child is true, its parent is true**.

```python
# !A => B

node_a = AtomNode('A') # AtomNode shares Node properties and definitions
node_b = AtomNode('B')
node_b.append_child(node_a, Sign.NEGATIVE)

# The NodeLink structure is created for you
print(node_b.children) # [NodeLink(node_a, Sign.NEGATIVE)]
```

Each **nodes** must be represented uniquely, meaning that we **must never have any duplication**. A `(node)` is considered the same as `!(node)`.

For example you will never find two `A` atoms, but also never find two times the same exact `ConnectorNode` instance  *(more detail for what connectors are after)*. This is really important for cases where an OR is placed in the conclusion side. For example with `A | B => C ; D => A | B`. If we know `D` is true, we must consider the `(A | B)` as true without knowing A or B.

```python
AtomNode('A') # Only 1 instance for the whole tree
AtomNode('B') # Only 1 instance for the whole tree

# Only one '&' ConnectorNode for:
(A & B)
!(A & B)

# Different '&' ConnectorNode for:
(A & B)
(!A & B)
```

#### The atom class

An `AtomNode` represents one fact. It's representation is an uppercase character.

```python
AtomNode('A')
```

#### The connector class

A `ConnectorNode` is used to represent one operator in the `ConnectorType` set  ( one of `& | ^`). The elements used for this connector are saved in the `connector_nodes` property.

```python
# Example: Create the (A + !B) ConnectorNode

connector_ab = ConnectorNode(ConnectorType.AND)
node_a = AtomNode('A')
node_b = AtomNode('B')

connector_ab.append_operand(node_a, Sign.POSITIVE)
connector_ab.append_operand(node_b, Sign.NEGATIVE)

print(connector_ab.connector_nodes) # [NodeLink(node_a, Sign.POSITIVE), NodeLink(node_b, Sign.NEGATIVE)]
```

#### The tree class

The `Tree` class keeps an `AND` operator connected to each of the Atoms in the `root`property. So that we have one tree for the whole set of rules.

#### Example

```python
# Example: (A | !B) <=> (C & D)

atom_a = AtomNode('A')
atom_b = AtomNode('B')
atom_c = AtomNode('C')
atom_d = AtomNode('D')

a_or_b = ConnectorNode(ConnectorType.OR)
a_or_b.append_operand(atom_a, Sign.POSITIVE)
a_or_b.append_operand(atom_b, Sign.NEGATIVE)

c_or_d = ConnectorNode(ConnectorType.AND)
c_or_d.append_operand(atom_c, Sign.POSITIVE)
c_or_d.append_operand(atom_d, Sign.POSITIVE)

a_or_b.append_child(c_or_d)
c_or_d.append_child(a_or_b)

# We connect all the nodes to the tree
tree = Tree()
tree.add_atom(atom_a)
tree.add_atom(atom_b)
tree.add_atom(atom_c)
tree.add_atom(atom_d)
```

### Special cases

#### Equivalence

In the case of an equivalence, both nodes will be parent and child.

```python
# Example: Creates the A <=> B
node_a = AtomNode('A')
node_b = AtomNode('B')
node_a.append_child(node_b, Sign.POSITIVE)
node_b.append_child(node_a, Sign.POSITIVE)
```

#### OR, AND, XOR in conclusions

When an operator is on the conclusion side, the child is placed **directly on the operator instance**.

```python
# Example: Creates the A => B + C

node_a = AtomNode('A')
node_b = AtomNode('B')
node_c = AtomNode('C')

connector_bc = ConnectorNode(ConnectorType.AND)
connector_bc.append_operand(node_b, Sign.POSITIVE)
connector_bc.append_operand(node_c, Sign.POSITIVE)

connector_bc.append_child(node_a)
```

#### Negatives in conclusion

***TODO NOT HANDLED YET***

We need to handle non simplifiable cases like `A => !B + C`

TODO (a | !a) is always true

TODO (a & !a) impossible

TODO (a XOR !a) always true, (a XOR a) always false

TODO Since a child is equivalent to a OR Two childs a or !a always true

```python
(A & B) => C
(!A & B)=> C # should detect impossible (or maybe it's valid ????)

# Maybe we can check that by saying that at the same level, the same letter must have same sign

(A & B) | (!A & B) => C # Same problem

```

TODO A => !A

TODO A | B => !B | C # should be  valid  I guess (!B  Becomes false so its (A | B) => C))
