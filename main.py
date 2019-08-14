import sys

from expert_system.parsers.ExpertParser import ExpertParser
from expert_system.Tree import NPITree


if __name__ == "__main__":
    try:
        with open(sys.argv[1]) as f:
            content = f.readlines(1000) # TODO anyway to set no limits ???
            parser = ExpertParser(content)

            # rules = parser.get_rules()
            # facts = parser.get_facts()
            rules = ""
            facts = ""

            tree = NPITree(rules, facts)
            # queries = parser.get_queries()
            queries = ["A"]

            for query in queries:
                tree.resolve_atom(query)

    except:
        print('Error opening file for reading ..!!')
