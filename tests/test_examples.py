import pytest

@pytest.mark.parametrize('input', [" ", "a ", " a", " a "])
def test_bad_files(input):
    with pytest.raises(errors.MyFooError) as ex:
        random_method(input)
