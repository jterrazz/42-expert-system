from anytree import Node, RenderTree
from anytree.exporter import DotExporter
from .parser.Rule import OPERATORS, ImplicationType
from .config.Env import Env

LST_Implication = {ImplicationType.EQUAL: '<=>', ImplicationType.IMPLY: '=>'}


class ESPrinter:
    count = 0

    def __init__(self, rules, facts, queries):
        self.rules = rules
        self.facts = facts
        self.queries = queries
        self.graph = self.create_full_tree()

    @staticmethod
    def create_part_tree(NPI_part, Implication):
        stack = []
        i = 0
        for x in NPI_part:
            if x == '!':
                i += 1
                pop = stack.pop()
                connector_not = Node(str(ESPrinter.count), display_name=x)
                pop.parent = connector_not
                stack.append(connector_not)
            elif x in OPERATORS:
                i += 1
                pop0 = stack.pop()
                pop1 = stack.pop()
                if pop0.display_name in OPERATORS and pop0.display_name == x:
                    pop1.parent = pop0
                    stack.append(pop0)
                elif pop1.display_name in OPERATORS and pop1.display_name == x:
                    pop0.parent = pop1
                    stack.append(pop1)
                else:
                    connector = Node(str(ESPrinter.count), display_name=x)
                    pop0.parent, pop1.parent = connector, connector
                    stack.append(connector)
            else:
                stack.append(Node(x, display_name=x))
            ESPrinter.count += 1
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
        DotExporter(self.graph, nodeattrfunc=lambda node: 'label="{}"'.format(node.display_name)).to_picture("graph.png")

    def display_tree_in_shell(self):
        for pre, fill, node in RenderTree(self.graph):
            print("%s%s" % (pre, node.display_name))

    @staticmethod
    def infix_to_postfix(formula):
        stack = []  # only pop when the coming op has priority
        for ch in formula:
            if ch == '!':
                pop = stack.pop()
                stack.append('!' + pop)
            elif ch not in OPERATORS:
                stack.append(ch)
            else:
                pop0 = stack.pop()
                pop1 = stack.pop()
                stack.append('(' + pop1 + ' ' + ch + ' ' + pop0 + ')')
        return stack[0]

    def display_rules(self):
        for x in self.rules:
            print(self.infix_to_postfix(x.npi_left), LST_Implication[x.type], self.infix_to_postfix(x.npi_right))
        print('=', ''.join(self.facts), sep='')
        print('?', ''.join(self.queries), sep='')

    def create_array_rules_facts_queries(self):
        output = []
        for x in self.rules:
            output.append('# ' + self.infix_to_postfix(x.npi_left) + ' ' + LST_Implication[x.type] + ' ' + self.infix_to_postfix(x.npi_right))
        output.append('# =' + ''.join(self.facts))
        output.append('# ?' + ''.join(self.queries))
        return output

    @staticmethod
    def display_file_histroy(rules, queries):
        for elem in rules:
            for x in elem:
                if x in queries:
                    if queries[x] == 'True':
                        print(f'\x1b[92m{x}\x1b[0m', end='')
                    else:
                        print(f'\x1b[91m{x}\x1b[0m', end='')
                else:
                    print(x, end='')
            print()
        print()

    def parser_file_history(self):
        try:
            with open(Env.LOG_PATH) as f:
                lines = f.readlines()

            lines = [x.strip() for x in lines]
            queries = {}
            rules = []
            i = 1
            for x in lines:
                if x[0] != '#' and x[0] != ';':
                    tmp = list(filter(None, x.split(',')))
                    for elem in tmp:
                        queries[elem.split('=')[0]] = elem.split('=')[1]
                elif x[0] == '#':
                    rules.append(x.replace('# ', ''))
                else:
                    print('History(', str(i), ')', sep='')
                    print('-------')
                    self.display_file_histroy(rules, queries)
                    queries = {}
                    rules = []
                    i += 1

        except:
            print("Error printing the history")
            raise


