import sys

# from expert_system.Prompt import ExpertPrompt
from expert_system.parser.Parser import ExpertParser
from expert_system.Tree import NPITree


def resolve_lines(lines):
    parser = ExpertParser(lines)
    tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    for query in parser.queries:
        print(f"Resolve {query}", tree.resolve_query(query))


if __name__ == "__main__":
    try:
        with open(sys.argv[1]) as f: # TODO protect argv
            file_lines = f.readlines(1000) # TODO Maybe we should actually do more than 1000
        resolve_lines(file_lines)

    except (Exception, BaseException) as e:
        print("{}".format(e))
        sys.exit(1)

    # ExpertSystem().cmdloop()
