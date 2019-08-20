import sys

from expert_system import Prompt, Tree, Print
from expert_system.parser.Parser import ESParser
from expert_system.config.Env import Env
from expert_system.config.Cmd import Cmd
from expert_system.util.Color import Color


def resolve_lines(parser):
    tree = Tree.NPITree(parser.structured_rules, parser.facts, parser.queries)
    results = {}
    for query in parser.queries:
        results[query] = tree.resolve_query(query)
        color = Color.GREEN if results[query] is True else Color.FAIL
        print(f"{ query } resolved as { color }{ results[query] }{ Color.END }")
    return results


def save_history(results):
    exp_sys = Print.ESPrinter(parser.structured_rules, parser.facts, parser.queries).create_array_rules_facts_queries()
    with open(Env.LOG_PATH, 'a') as f:
        for query, val in results.items():
            f.write(query + '=' + str(val) + ',')
        f.write('\n')
        for x in exp_sys:
            f.write(x + '\n')
        f.write(';' + '\n')
        Print.ESPrinter(parser.structured_rules, parser.facts, parser.queries).parser_file_history()


if __name__ == "__main__":
    args = Cmd.args

    try:
        with open(args.input) as f:
            lines = f.readlines()

        if args.mode == "interactive":
            Prompt.ESPrompt(lines).cmdloop()
        else:
            parser = ESParser(lines)
            if args and args.graph:
                print(f"{Color.PURPLE}[Tree representation 🌳]{Color.END}")
                Print.ESPrinter(parser.structured_rules, parser.facts, parser.queries).display_tree_in_shell()
                print("")
            if args and args.rules:
                print(f"{Color.PURPLE}[List of rules 📚]{Color.END} ")
                Print.ESPrinter(parser.structured_rules, parser.facts, parser.queries).display_rules()
                print("")

            res = resolve_lines(parser)

            if args and args.image:
                Print.ESPrinter(parser.structured_rules, parser.facts, parser.queries).create_image()
                print(f"{Color.PURPLE}Image { Env.IMG_PATH } create{Color.END} ")

            if args.history:
                save_history(res)

    except (Exception, BaseException) as e:
        print(e)
        sys.exit(1)
