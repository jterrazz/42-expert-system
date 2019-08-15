import sys

from expert_system.parsers.ExpertParser import ExpertParser
from expert_system.Tree import NPITree

if __name__ == "__main__":
    try:
        with open(sys.argv[1]) as f:
            content = f.readlines(1000) # TODO anyway to set no limits ???
    except: # TODO Except only for Reading errors
        print('Error opening file for reading ..!!')
    finally:
        parser = ExpertParser(content)

        tree = NPITree(parser.structured_rules, parser.facts, parser.queries)

        for query in parser.queries:
            print(f"Resolve {query}", tree.resolve_atom(query))
