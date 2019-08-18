import pytest
from os import listdir
from os.path import isfile, join
from main import resolve_lines
from expert_system.parser.Parser import ExpertParser
from expert_system.Tree import NPITree

def get_all_files(path):
    return [f for f in listdir(path) if isfile(join(path, f))]

# Without the folder path
good_results = [
    ("and.txt", [True, False]),
    ("and_in_conclusions.txt", [True, True, True, True, True]),
    ("AND_LIST", [False]),
    ("AND_OR", [True]),
    ("BI_IF", [True]),
    ("comments.txt", [True, True, True]),
    ("double_implies.txt", [True, True, True]),
    ("easy_test.txt", [True, True, False]),
    # ("empty_init_test.txt", [True, True, True]),
    # ("HAfffff.txt", [True]),
    ("hard_imply_2.txt", [True]),
    # ("HARDDDDDER.txt", [True]),
    ("imply_and.txt", [True]),
    ("mix.txt", [True, False, False, True, True, False]),
    ("mix2.txt", [True]),
    ("multiple_initial_facts.txt", [True, False]),
    ("multiple_initial_facts2.txt", [False, False]),
    ("multiple_initial_facts3.txt", [False, False]),
    ("multiple_initial_facts4.txt", [False, True]),
    ("multiple_initial_facts5.txt", [False, False]),
    ("multiple_initial_facts6.txt", [True, True]),
    # ("NEGATION_SIMPLE_1", [False]),
    # ("NEGATION_SIMPLE_2", [False]),
    # ("NEGATION_SIMPLE_3", [False]),
    ("no_initial_facts1.txt", [False]),
    ("no_initial_facts2.txt", [False]),
    ("not.txt", [False, True]),
    ("or.txt", [True, True]),
    # ("parentheses_test.txt", [True, False, False, True, True, True]),
    ("parenthesis.txt", [True, False, False, True, True, True]),
    # ("test.txt", [True, False, False, True, True, True]),
    ("test_blyat.txt", [True]),
    ("test_blyat1.txt", [True]),
    # ("test_harrrrrd.txt", [True]),

    # >>> Add the others
    # ("test_intranet1", [None, None]),
    # ("test_intranet2", [None, None]),
    # ("test_intranet3", [None, None]),
    # ("test_intranet4", [None, None]),

    ("test_parents_priority.txt", [True]),
    ("test_parents_priority2.txt", [True]),
    ("test_not", [False]),
    ("test_slack1", [False]),
    ("test_slack2", [False]),
    ("test_slack3", [False]),
    ("test_slack4", [False]),
    ("xor.txt", [False, True, True, False]),
]

@pytest.mark.parametrize('input, expected', good_results)
def test_good_files(input, expected):
    with open("./tests/_examples/good_files/" + input) as f:
        file_lines = f.readlines(1000)
    parser = ExpertParser(file_lines)
    tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    i = 0
    for query in parser.queries:
        assert expected[i] == tree.resolve_query(query)
        i += 1


bad_files_path = "./tests/_examples/bad_files"
bad_files = [bad_files_path + f for f in get_all_files(bad_files_path)]


@pytest.mark.parametrize('input', bad_files)
def test_bad_files(input):
    try:
        with open(input) as f:
            file_lines = f.readlines(1000)
        resolve_lines(file_lines)
    except:
        pass
        return True
    raise BaseException(f"File { input } should trigger an error")
