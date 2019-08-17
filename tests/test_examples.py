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
    ("comments.txt", [True, True, True]),

    # >>> Add the others
    ("test_intranet1", [None, None]),
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
