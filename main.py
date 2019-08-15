import sys

from expert_system.parser.Parser import ExpertParser
from expert_system.Tree import NPITree

if __name__ == "__main__":
    try:
        with open(sys.argv[1]) as f:
            content = f.readlines()  # TODO Do we really need the 1000 limit ???
    except:
        print('Error opening file for reading')
        raise

    parser = ExpertParser(content)
    tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    for query in parser.queries:
        print(f"Resolve {query}", tree.resolve_query(query))
