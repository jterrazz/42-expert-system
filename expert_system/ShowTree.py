from anytree import Node, RenderTree
from anytree.exporter import DotExporter
from .parser.Rule import OPERATORS, ImplicationType

LST_Implication = {ImplicationType.EQUAL :'<=>', ImplicationType.IMPLY :'=>'}

class ShowTree:
    count = 0
    def __init__(self, rules):
        self.rules = rules
        self.graph = self.create_full_tree()

    def create_part_tree(self, NPI_part, Implication):
        stack = []
        i = 0
        for x in NPI_part:
            if x == '!':
                i += 1
                pop = stack.pop()
                connector_not = Node(str(ShowTree.count), display_name=x)
                pop.parent = connector_not
                stack.append(connector_not)
            elif x in OPERATORS:
                i += 1
                pop0 = stack.pop()
                pop1 = stack.pop()
                connector = Node(str(ShowTree.count), display_name=x)
                pop0.parent, pop1.parent = connector, connector
                stack.append(connector)
            else:
                stack.append(Node(x, display_name=x))
            ShowTree.count += 1
        pop = stack.pop()
        pop.parent = Implication

    def create_full_tree(self):
        root = Node('root', display_name='root')
        for key, val in enumerate(self.rules):
            imp = Node(LST_Implication[val.type] + str(key), parent=root, display_name=LST_Implication[val.type])
            self.create_part_tree(val.npi_left, imp)
            self.create_part_tree(val.npi_right, imp)
        return root

    def create_image(self):
        # create image
        DotExporter(self.graph,
            nodeattrfunc=lambda node: 'label="{}"'.format(node.display_name)).to_picture("graph.png")

    def display_tree_in_shell(self):
        for pre, fill, node in RenderTree(self.graph):
            print("%s%s" % (pre, node.display_name))
