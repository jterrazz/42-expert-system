import sys
import argparse

from expert_system.Prompt import ExpertPrompt
from expert_system.parser.Parser import ExpertParser
from expert_system.Tree import NPITree
from expert_system.ShowTree import ShowTree


def resolve_lines(parser):
    # create tree image
    # ShowTree(parser.structured_rules, parser.facts, parser.queries).create_image()
    tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    result = {}
    for query in parser.queries:
        result[query] = tree.resolve_query(query)
        print(f"Resolve {query}", result[query])

    exp_sys = ShowTree(parser.structured_rules, parser.facts, parser.queries).create_array_rules_facts_queries()
    with open('Experthistory', 'a') as f:
        for query, val in result.items():
            f.write(query + '=' + str(val) + ',')
        f.write('\n')
        for x in exp_sys:
            f.write(x + '\n')


if __name__ == "__main__":

    # Parser
    flag = argparse.ArgumentParser(description='ExpertSystem @ Paris 42 School - Made by @abbensid and @jterrazz')
    flag.add_argument("-m", choices=['shell', 'interactive'], default='mode_shell', help="Interface mode")
    flag.add_argument("-d", action='store_true', help="Displays the graph")
    flag.add_argument("-r", action='store_true', help="Displays the rules")
    flag.add_argument("-i", action='store_true', help="create graph system")
    flag.add_argument("--history", action='store_true', help="Keep old states in memory")
    flag.add_argument("input", help="The file containing rules, facts and queries")
    args = flag.parse_args()

    try:
        with open(args.input) as f:
            lines = f.readlines() # TODO Maybe we should actually do more than 1000

        if args.m == "interactive":
            ExpertPrompt(lines).cmdloop()
        else:
            parser = ExpertParser(lines)
            if args and args.d:
                ShowTree(parser.structured_rules, parser.facts, parser.queries).display_tree_in_shell()
            if args and args.r:
                ShowTree(parser.structured_rules, parser.facts, parser.queries).display_rules()
            resolve_lines(parser)

    except (Exception, BaseException) as e:
        print("{}".format(e))
        sys.exit(1)