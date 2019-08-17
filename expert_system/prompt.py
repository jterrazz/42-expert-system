import cmd
# from termcolor import colored
from expert_system.parser.Parser import ExpertParser
from expert_system.Tree import NPITree

class ExpertSystem(cmd.Cmd):
    # cmd.Cmd.prompt = colored("ExpertSystem>> ", "cyan")

    # Function help general
    def do_help_all(self, line):
        if line:
            print("Error: command without arg")
        else:
            print('\n'.join(['help_all       : show all help command',
                             'resolve        : resolve system',
                             'show           : show all rules, facts and queries',
                             'show_facts     : show all facts',
                             'show_queries   : show all queries',
                             'add_facts      : add facts to system',
                             'add_queries    : add queries to system',
                             'del_facts      : delete one, or multiple facts',
                             'del_queries    : delete one, or multiple queries',
                             'exit           : Exit prompt',
                             'CTRL+D         : Quit prompt',
                             ]))

    def help_help_all(self):
        print('\n'.join(['help_all',
                           'help_all !!',
                           ]))

    # Function resolve system
    def do_resolve(self, line):
        if line:
            print("Error: command without arg")
        else:
            tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
            for query in parser.queries:
                print(f"Resolve {query}", tree.resolve_query(query))

    def help_show(self):
        print('\n'.join(['resolve',
                           'resolve !!',
                           ]))

    # Function open file
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