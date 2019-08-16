import sys

from expert_system.parser.Parser import ExpertParser
from expert_system.Tree import NPITree

if __name__ == "__main__":
    try:
        with open(sys.argv[1]) as f:
            content = f.readlines(1000)
    except Exception as e:
        print("{}".format(e))
        sys.exit(1)

    parser = ExpertParser(content)
    tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    for query in parser.queries:
        print(f"Resolve {query}", tree.resolve_query(query))
