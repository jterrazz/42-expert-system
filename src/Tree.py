# Rename Tree class
from .Node import AtomNode, ConnectorNode, ConnectorType
from asciitree import LeftAligned
from collections import OrderedDict as OD

class Tree:
    def __init__(self):
        self.atoms = []
        self.root = ConnectorType(ConnectorType.AND)

        atom_a = AtomNode('A')
        atomB = AtomNode('B')
        atomC = AtomNode('C')
        atomD = AtomNode('D')
        atomE = AtomNode('E')

        connectorBC = ConnectorNode(ConnectorType.AND)
        connectorBC.append_child(atomB)
        connectorBC.append_child(atomC)

        atom_a.append_child(connectorBC)

        connectorDE = ConnectorNode(ConnectorType.OR)
        connectorDE.append_child(atomD)
        connectorDE.append_child(atomE)
        atomB.append_child(connectorDE)

        atomC.append_child(atomB)

        connectorBC2 = ConnectorNode(ConnectorType.AND)
        connectorBC2.append_child(atomC)
        connectorBC2.append_child(atomB)

        connectorBCorA = ConnectorNode(ConnectorType.OR)
        connectorBCorA.append_child(connectorBC2)
        connectorBCorA.append_child(atom_a)
        atomD.append_child(connectorBCorA)

    # def resolve(self):

    def print(self): # Replace the official print method
        self.printable_tree = {
            'TREEEEEEE': self.create_printable_node(self.root) # Replace name
        }

    @staticmethod
    def create_printable_node(parent):
        child_id = 0
        child = parent.children.first
        while (child):

            child_id += 1
            child = parent.children[child_id]

