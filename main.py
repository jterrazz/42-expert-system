import sys
import argparse

# from expert_system.Prompt import ExpertPrompt
from expert_system.parser.Parser import ExpertParser
from expert_system.Tree import NPITree
# from expert_system.ShowTree import ShowTree


def resolve_lines(lines):
    parser = ExpertParser(lines)

    # create tree image
    # ShowTree(parser.structured_rules, parser.facts, parser.queries).create_image()

    tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    for query in parser.queries:
        print(f"Resolve {query}", tree.resolve_query(query))


if __name__ == "__main__":

    # Parser
    flag = argparse.ArgumentParser(description='ExpertSystem @ 42')
    flag.add_argument("-m", choices=['mode_shell', 'mode_interactive'], default='mode_shell', help="show mode")
    flag.add_argument("-d", action='store_true', help="display graph system")
    flag.add_argument("-r", action='store_true', help="display rules system")
    flag.add_argument("-i", action='store_true', help="create graph system")
    flag.add_argument("-hist", action='store_true', help="display historique system")
    flag.add_argument("input", help="input system")
    flag.parse_args()
    args = flag.parse_args()

    try:
        with open(sys.argv[1]) as f: # TODO protect argv
            file_lines = f.readlines(1000) # TODO Maybe we should actually do more than 1000
        resolve_lines(file_lines)

    except (Exception, BaseException) as e:
        print("{}".format(e))
        sys.exit(1)

    # flag mode
    if args.m == 'mode_shell':
        print('mode Shell')
    elif args.m == 'mode_interactive':
        print('mode interactive')
    else:
        print('mode Shell')

    parser = ExpertParser(file_lines)
    # flag display graph
    if args.d:
        ShowTree(parser.structured_rules, parser.facts, parser.queries).display_tree_in_shell()

    # flag display rules
    if args.r:
        ShowTree(parser.structured_rules, parser.facts, parser.queries).display_rules()

    # ExpertSystem().cmdloop()
