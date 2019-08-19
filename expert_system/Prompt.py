import cmd

from .util.Color import Color
from expert_system.parser.Parser import ESParser
from expert_system import Tree


class ESPrompt(cmd.Cmd):
    def __init__(self, lines):
        super(ESPrompt, self).__init__()
        self.lines = []
        self.prompt = f'{ Color.PURPLE }<ExpertSystem> { Color.END }'
        self.set_lines(lines)

    def set_lines(self, lines):
        self.lines = [f for f in filter(None, [l.replace("\n", "").replace(" ", "").replace("\s", "") for l in lines])]

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

    # Delete functions

    def do_del_rule(self, rule_id):
        try:
            id = int(rule_id)
            if self.lines[id][0] != "=" and self.lines[id][0] != "!":
                self.lines.pop(id)
            else:
                print("Index is not valid")

        except Exception as e:
            print("Index is not valid")

    @staticmethod
    def help_del_rule():
        print('del_rule <X> - With X the id of the rule (type show to list the rules)')

    def do_del_fact(self, fact):
        if fact and fact.isupper():
            for i, line in enumerate(self.lines):
                if line[0] == "=":
                    self.lines[i] = line.replace(fact, "")

    @staticmethod
    def help_del_fact():
        print('del_fact <X> - With X being a single uppercase letter')

    def do_del_query(self, query):
        if query and query.isupper():
            for i, line in enumerate(self.lines):
                if line[0] == "?":
                    self.lines[i] = line.replace(query, "")

    @staticmethod
    def help_del_query():
        print('del_query <X> - With X being a single uppercase letter')

    @staticmethod
    def do_exit(line):
        return True

    @staticmethod
    def do_EOF(line):
        return True
