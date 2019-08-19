import sys
import argparse

# from expert_system.Prompt import ExpertPrompt
from expert_system.parser.Parser import ExpertParser
from expert_system.Tree import NPITree
# from expert_system.ShowTree import ShowTree


def resolve_lines(lines):
    parser = ExpertParser(lines)

    # create tree image
    # ShowTree(parser.structured_rules).create_full_tree()

    tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    for query in parser.queries:
        print(f"Resolve {query}", tree.resolve_query(query))


if __name__ == "__main__":

    # Parser
    parser = argparse.ArgumentParser(description='ExpertSystem @ 42')
    parser.add_argument("-m", choices=['mode_shell', 'mode_interactive'], default='mode_shell', help="show mode")
    parser.add_argument("-d", action='store_true', help="display graph system")
    parser.add_argument("-hist", action='store_true', help="display historique system")
    parser.add_argument("input", help="input system")
    parser.parse_args()
    args = parser.parse_args()


    try:
        with open(sys.argv[1]) as f: # TODO protect argv
            file_lines = f.readlines(1000) # TODO Maybe we should actually do more than 1000
        resolve_lines(file_lines)

    except (Exception, BaseException) as e:
        print("{}".format(e))
        sys.exit(1)

    # ExpertSystem().cmdloop()
