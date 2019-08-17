import pytest
from os import listdir
from os.path import isfile, join
from main import resolve_lines

def get_all_files(path):
    return [f for f in listdir(path) if isfile(join(path, f))]

# results = [
#     ()
# ]
#
# @pytest.mark.parametrize('input, expected', [(1, 0)])
# def test_bad_files(input, expected):


bad_files_path = "./tests/_examples/bad_files"
bad_files = [bad_files_path + f for f in get_all_files(bad_files_path)]
@pytest.mark.parametrize('input', bad_files)
def test_bad_files(input):
    try:
        with open(input) as f:  # TODO protect argv
            file_lines = f.readlines(1000)  # TODO Maybe we should actually do more than 1000
        resolve_lines(file_lines)
    except:
        pass
        return True
    raise BaseException(f"File { input } should trigger an error")
