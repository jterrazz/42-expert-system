from anytree import Node, RenderTree
from anytree.exporter import DotExporter
from .parser.Rule import OPERATORS, ImplicationType

LST_Implication = {ImplicationType.EQUAL :'<=>', ImplicationType.IMPLY :'=>'}

class ShowTree:
    def __init__(self, rules):
        self.rules = rules

    def create_part_tree(self, NPI_part, part, Implication, rule_index):
        stack = []
        i = 0
        for x in NPI_part:
            if x == '!':
                i += 1
                pop = stack.pop()
                connector_not = Node(x + 'not' + part + str(i) + str(rule_index), display_name=x)
                pop.parent = connector_not
                stack.append(connector_not)
            elif x in OPERATORS:
                i += 1
                pop0 = stack.pop()
                pop1 = stack.pop()
                connector = Node(x + part + str(i) + str(rule_index), display_name=x)
                pop0.parent, pop1.parent = connector, connector
                stack.append(connector)
            else:
                stack.append(Node(x, display_name=x))
        pop = stack.pop()
        pop.parent = Implication

    def create_full_tree(self):
        root = Node('root', display_name='root')
        for key, val in enumerate(self.rules):
            imp = Node(LST_Implication[val.type] + str(key), parent=root, display_name=LST_Implication[val.type])
            self.create_part_tree(val.npi_left, 'left', imp, key)
            self.create_part_tree(val.npi_right, 'right', imp, key)

        # create image
        DotExporter(root,
                nodeattrfunc=lambda node: 'label="{}"'.format(node.display_name)).to_picture("graph.png")