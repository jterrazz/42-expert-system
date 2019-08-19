import cmd

from .util.Color import Color

# from termcolor import colored
from expert_system.parser.Parser import ESParser
from expert_system import Tree
# from main import resolve_lines


class ESPrompt(cmd.Cmd):
    def __init__(self, lines):
        super(ESPrompt, self).__init__()
        self.lines = lines
        self.prompt = f'{ Color.PURPLE }<ExpertSystem> { Color.END }'

    # TODO Check all are implemented

    @staticmethod
    def do_h(self, line):
        print('\n'.join(['h                : Display help commands',
                         'solve <id|None>  : Solve the queries',
                         'show             : Show rules, facts and queries',
                         'show_rules       : Show facts',
                         'show_facts       : Show facts',
                         'show_queries     : Show queries',
                         'add_rule         : Add a new rule',
                         'add_fact         : Add a new fact',
                         'add_query        : Add a new query',
                         'del_rule <id>    : Delete a fact',
                         'del_fact <id>    : Delete a fact',
                         'del_query <id>   : Delete a query',
                         'exit             : Exit',
                         'CTRL+D           : Exit',
                         ]))

    def do_solve(self, id):
        try:
            parser = ESParser(self.lines)
            queries = [id] if id else parser.queries
            tree = Tree.NPITree(parser.structured_rules, parser.facts, parser.queries)

            for query in queries:
                print(f"{query} resolved as", tree.resolve_query(query))
        except (Exception, BaseException) as e:
            print(e)
            pass

    def do_open(self, path):
        try:
            with open(path) as f:  # protect argv
                content = f.readlines(1000)
                print(content)

        except Exception as e:
            print("{}".format(e))

    def help_open(self):
        print('\n'.join(['open [path]',
                           'open file of rule, ex: open ../test_and',
                           ]))

    # Function show system
    def do_show(self, line):
        if line:
            print("Error: command without arg")
        else:
            print("show all")

    def help_show(self):
        print('\n'.join(['show_all',
                           'show all system',
                           ]))

    # Function addfacts
    def do_add_facts(self, facts):
        print("hi,", facts)

    def help_add_facts(self):
        print('\n'.join(['add_facts [facts]',
                           'add facts, ex: add_facts =ABD',
                           ]))

    # Function del facts
    def do_del_facts(self, facts):
        print("hi,", facts)

    def help_del_facts(self):
        print('\n'.join(['del_facts [facts]',
                           'del facts, ex: del_facts DB',
                           ]))
    # Function show facts
    def do_show_facts(self, line):
        if line:
            print("Error: command without arg")
        else:
            print("show_facts")

    def help_show_facts(self):
        print('\n'.join(['show_facts',
                           'show facts, ex: show_facts',
                           ]))

    # Function add queries
    def do_add_queries(self, queries):
        print("hi,", queries)

    def help_add_queries(self):
        print('\n'.join(['add_queries [queries]',
                           'add queries, ex: add_queies ?DBF',
                           ]))

    # Function del queries
    def do_del_queries(self, queries):
        print("hi,", queries)

    def help_del_queries(self):
        print('\n'.join(['del_queries [queries]',
                           'del queries, ex: del_queies DB',
                           ]))

    # Function show queries
    def do_show_queries(self, line):
        if line:
            print("Error: command without arg")
        else:
            print("show_queries")

    def help_show_queries(self):
        print('\n'.join(['show_queries',
                           'show queries, ex: show_queies',
                           ]))

    # Function Exit
    def help_exit(self):
        print('\n'.join(['exit',
                           'Exit prompt',
                           ]))

    def do_exit(self, line):
        return True

    # Function EOF
    def help_EOF(self):
        print('\n'.join(['CTRL+D',
                           'Exit prompt',
                           ]))

    def do_EOF(self, line):
        return True

    def postloop(self):
        print()
