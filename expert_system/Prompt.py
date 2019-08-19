import cmd

from .util.Color import Color

# from termcolor import colored
from expert_system.parser.Parser import ESParser
from expert_system import Tree
# from main import resolve_lines


class ESPrompt(cmd.Cmd):
    def __init__(self, lines):
        super(ESPrompt, self).__init__()
        self.lines = []
        self.prompt = f'{ Color.PURPLE }<ExpertSystem> { Color.END }'
        self.set_lines(lines)

    def set_lines(self, lines):
        self.lines = [f for f in filter(None, [l.replace("\n", "") for l in lines])]

    # TODO Check all are implemented

    @staticmethod
    def do_h(line):
        print('\n'.join(['h                : Display help commands',
                         'solve <id|None>  : Solve the queries',
                         'show             : Show rules, facts and queries',
                         'show_rules       : Show facts',
                         'show_facts       : Show facts',
                         'show_queries     : Show queries',
                         'add_rule <rule>  : Add a new rule',
                         'add_fact <X>     : Add a new fact',
                         'add_query <X>    : Add a new query',
                         'del_rule <id>    : Delete a fact',
                         'del_fact <X>     : Delete a fact',
                         'del_query <X>    : Delete a query',
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

    def do_open(self, path):
        try:
            with open(path) as f:
                lines = f.readlines()
                ESParser(lines)
                self.set_lines(lines)
            print(f"File { path } was successfully open")
        except Exception as e:
            print(e)

    @staticmethod
    def help_open():
        print('\n'.join(['open <path> - The file must be formatted to the expected format (More in the README.md)']))

    # Display functions

    def do_show(self, line):
        for i, line in enumerate(self.lines):
            if line[0] != "=" and line[0] != "?":
                print(f"Rule { i }: { line }")
            else:
                print(line)

    def do_show_rules(self, line):
        for i, line in enumerate(self.lines):
            if line[0] != "=" and line[0] != "?":
                print(f"Rule {i}: {line}")

    def do_show_facts(self, line):
        for line in self.lines:
            if line[0] == "=":
                print(line)

    def do_show_queries(self, line):
        for line in self.lines:
            if line[0] == "?":
                print(line)

    # Add functions

    def do_add_rule(self, rule):
        if rule is None:
            print("<rule> argument required")
            return

        self.lines.insert(0, rule)
        try:
            ESParser(self.lines)
            print(f"{rule} was successfully added")
        except (Exception, BaseException) as e:
            print(f"Error adding the rule {rule}: { e }")
            self.lines.pop(0)

    def do_add_fact(self, fact):
        if fact is None:
            print("<fact> argument required")
            return

        for i, line in enumerate(self.lines):
            if line[0] == "=":
                if fact not in line:
                    self.lines[i] = line[:1] + fact + line[1:]
                try:
                    ESParser(self.lines)
                    print(f"{ fact } was successfully added")
                except:
                    print(f"Error adding the fact { fact }")
                    self.lines[i] = line
                return

    @staticmethod
    def help_add_fact():
        print('add_fact <X> - With X being a single uppercase letter')

    def do_add_query(self, query):
        if query is None:
            print("<query> argument required")
            return

        for i, line in enumerate(self.lines):
            if line[0] == "?":
                if query not in line:
                    self.lines[i] = line[:1] + query + line[1:]
                try:
                    ESParser(self.lines)
                    print(f"{ query } was successfully added")
                except:
                    print(f"Error adding the query { query }")
                    self.lines[i] = line
                return

    @staticmethod
    def help_add_query():
        print('add_query <X> - With X being a single uppercase letter')



    def do_del_facts(self, facts):
        print("hi,", facts)

    def help_del_facts(self):
        print('\n'.join(['del_facts [facts]',
                           'del facts, ex: del_facts DB',
                           ]))

    # Function add queries


    # Function del queries
    def do_del_queries(self, queries):
        print("hi,", queries)

    def help_del_queries(self):
        print('\n'.join(['del_queries [queries]',
                           'del queries, ex: del_queies DB',
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
