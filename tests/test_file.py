
def test_and():
    if __name__ == "__main__":
        try:
            with open('./tests/examples/good_files/and.txt') as f:
                content = f.readlines()
        except:
            print('Error opening file for reading')
            raise

        parser = ExpertParser(content)
        tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("C") is True
    assert tree.resolve_query("F") is False

def test_and_in_conclusions():
    if __name__ == "__main__":
        try:
            with open('./tests/examples/good_files/and_in_conclusions.txt') as f:
                content = f.readlines()
        except:
            print('Error opening file for reading')
            raise

        parser = ExpertParser(content)
        tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("F") is True
    assert tree.resolve_query("C") is True
    assert tree.resolve_query("D") is True
    assert tree.resolve_query("U") is True

def test_comments():
    if __name__ == "__main__":
        try:
            with open('./tests/examples/good_files/comments.txt') as f:
                content = f.readlines()
        except:
            print('Error opening file for reading')
            raise

        parser = ExpertParser(content)
        tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("C") is True
    assert tree.resolve_query("D") is True
    assert tree.resolve_query("F") is True

def test_double_implies():
    if __name__ == "__main__":
        try:
            with open('./tests/examples/good_files/double_implies.txt') as f:
                content = f.readlines()
        except:
            print('Error opening file for reading')
            raise

        parser = ExpertParser(content)
        tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("F") is True
    assert tree.resolve_query("C") is True
    assert tree.resolve_query("D") is True

def test_mix():
    if __name__ == "__main__":
        try:
            with open('./tests/examples/good_files/mix.txt') as f:
                content = f.readlines()
        except:
            print('Error opening file for reading')
            raise

        parser = ExpertParser(content)
        tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("G") is True
    assert tree.resolve_query("T") is False
    assert tree.resolve_query("X") is False

def test_mix2():
    if __name__ == "__main__":
        try:
            with open('./tests/examples/good_files/mix2.txt') as f:
                content = f.readlines()
        except:
            print('Error opening file for reading')
            raise

        parser = ExpertParser(content)
        tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("C") is True

def test_multiple_initial_facts():
    if __name__ == "__main__":
        try:
            with open('./tests/examples/good_files/multiple_initial_facts.txt') as f:
                content = f.readlines()
        except:
            print('Error opening file for reading')
            raise

        parser = ExpertParser(content)
        tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("E") is True
    assert tree.resolve_query("F") is True

def test_multiple_no_initial_facts1():
    if __name__ == "__main__":
        try:
            with open('./tests/examples/good_files/no_initial_facts1.txt') as f:
                content = f.readlines()
        except:
            print('Error opening file for reading')
            raise

        parser = ExpertParser(content)
        tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("C") is False

def test_multiple_no_initial_facts2():
    if __name__ == "__main__":
        try:
            with open('./tests/examples/good_files/no_initial_facts2.txt') as f:
                content = f.readlines()
        except:
            print('Error opening file for reading')
            raise

        parser = ExpertParser(content)
        tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("C") is False

def test_not():
    if __name__ == "__main__":
        try:
            with open('./tests/examples/good_files/not.txt') as f:
                content = f.readlines()
        except:
            print('Error opening file for reading')
            raise

        parser = ExpertParser(content)
        tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("B") is False
    assert tree.resolve_query("D") is True

def test_or():
    if __name__ == "__main__":
        try:
            with open('./tests/examples/good_files/or.txt') as f:
                content = f.readlines()
        except:
            print('Error opening file for reading')
            raise

        parser = ExpertParser(content)
        tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("C") is True
    assert tree.resolve_query("F") is True

def test_parenthesis():
    if __name__ == "__main__":
        try:
            with open('./tests/examples/good_files/parenthesis.txt') as f:
                content = f.readlines()
        except:
            print('Error opening file for reading')
            raise

        parser = ExpertParser(content)
        tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("C") is True
    assert tree.resolve_query("D") is False
    assert tree.resolve_query("W") is False
    assert tree.resolve_query("G") is True
    assert tree.resolve_query("F") is True
    assert tree.resolve_query("Z") is True

def test_xor():
    if __name__ == "__main__":
        try:
            with open('./tests/examples/good_files/xor.txt') as f:
                content = f.readlines()
        except:
            print('Error opening file for reading')
            raise

        parser = ExpertParser(content)
        tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("C") is False
    assert tree.resolve_query("F") is True
    assert tree.resolve_query("I") is True
    assert tree.resolve_query("L") is False

def test_test_and1():
    if __name__ == "__main__":
        try:
            with open('./tests/examples/correction/test_and1.txt') as f:
                content = f.readlines()
        except:
            print('Error opening file for reading')
            raise

        parser = ExpertParser(content)
        tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("A") is True
    assert tree.resolve_query("G") is True
    assert tree.resolve_query("K") is True
    assert tree.resolve_query("P") is True

def test_test_and2():
    if __name__ == "__main__":
        try:
            with open('./tests/examples/correction/test_and2') as f:
                content = f.readlines()
        except:
            print('Error opening file for reading')
            raise

        parser = ExpertParser(content)
        tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("A") is True
    assert tree.resolve_query("G") is True
    assert tree.resolve_query("K") is True
    assert tree.resolve_query("P") is True

def test_test_and1():
    if __name__ == "__main__":
        try:
            with open('./tests/examples/correction/test_and1.txt') as f:
                content = f.readlines()
        except:
            print('Error opening file for reading')
            raise

        parser = ExpertParser(content)
        tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("A") is True
    assert tree.resolve_query("G") is True
    assert tree.resolve_query("K") is True
    assert tree.resolve_query("P") is True