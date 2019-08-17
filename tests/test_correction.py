from expert_system.Tree import NPITree
from expert_system.parser.Parser import ExpertParser

def test_and():
    try:
        with open('./tests/_examples/good_files/and.txt') as f:
            content = f.readlines()
    except:
        print('Error opening file for reading')
        raise

    parser = ExpertParser(content)
    tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("C") is True
    assert tree.resolve_query("F") is False

def test_and_in_conclusions():
    try:
        with open('./tests/_examples/good_files/and_in_conclusions.txt') as f:
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
    try:
        with open('./tests/_examples/good_files/comments.txt') as f:
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
    try:
        with open('./tests/_examples/good_files/double_implies.txt') as f:
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
    try:
        with open('./tests/_examples/good_files/mix.txt') as f:
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
    try:
        with open('./tests/_examples/good_files/mix2.txt') as f:
            content = f.readlines()
    except:
        print('Error opening file for reading')
        raise

    parser = ExpertParser(content)
    tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("C") is True

def test_multiple_initial_facts():
    try:
        with open('./tests/_examples/good_files/multiple_initial_facts.txt') as f:
            content = f.readlines()
    except:
        print('Error opening file for reading')
        raise

    parser = ExpertParser(content)
    tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("E") is True
    assert tree.resolve_query("F") is False

def test_multiple_initial_facts2():
    try:
        with open('./tests/_examples/good_files/multiple_initial_facts2.txt') as f:
            content = f.readlines()
    except:
        print('Error opening file for reading')
        raise

    parser = ExpertParser(content)
    tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("E") is False
    assert tree.resolve_query("F") is False

def test_multiple_initial_facts3():
    try:
        with open('./tests/_examples/good_files/multiple_initial_facts3.txt') as f:
            content = f.readlines()
    except:
        print('Error opening file for reading')
        raise

    parser = ExpertParser(content)
    tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("E") is False
    assert tree.resolve_query("F") is False

def test_multiple_initial_facts4():
    try:
        with open('./tests/_examples/good_files/multiple_initial_facts4.txt') as f:
            content = f.readlines()
    except:
        print('Error opening file for reading')
        raise

    parser = ExpertParser(content)
    tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("E") is False
    assert tree.resolve_query("F") is True

def test_multiple_initial_facts5():
    try:
        with open('./tests/_examples/good_files/multiple_initial_facts5.txt') as f:
            content = f.readlines()
    except:
        print('Error opening file for reading')
        raise

    parser = ExpertParser(content)
    tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("E") is False
    assert tree.resolve_query("F") is False

def test_multiple_initial_facts6():
    try:
        with open('./tests/_examples/good_files/multiple_initial_facts6.txt') as f:
            content = f.readlines()
    except:
        print('Error opening file for reading')
        raise

    parser = ExpertParser(content)
    tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("E") is True
    assert tree.resolve_query("F") is True

def test_multiple_no_initial_facts1():
    try:
        with open('./tests/_examples/good_files/no_initial_facts1.txt') as f:
            content = f.readlines()
    except:
        print('Error opening file for reading')
        raise

    parser = ExpertParser(content)
    tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("C") is False

def test_multiple_no_initial_facts2():
    try:
        with open('./tests/_examples/good_files/no_initial_facts2.txt') as f:
            content = f.readlines()
    except:
        print('Error opening file for reading')
        raise

    parser = ExpertParser(content)
    tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("C") is False

def test_not():
    try:
        with open('./tests/_examples/good_files/not.txt') as f:
            content = f.readlines()
    except:
        print('Error opening file for reading')
        raise

    parser = ExpertParser(content)
    tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("B") is False
    assert tree.resolve_query("D") is True

def test_or():
    try:
        with open('./tests/_examples/good_files/or.txt') as f:
            content = f.readlines()
    except:
        print('Error opening file for reading')
        raise

    parser = ExpertParser(content)
    tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("C") is True
    assert tree.resolve_query("F") is True

def test_parenthesis():
    try:
        with open('./tests/_examples/good_files/parenthesis.txt') as f:
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
    try:
        with open('./tests/_examples/good_files/xor.txt') as f:
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
    try:
        with open('./tests/_correction/test_and1') as f:
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
    try:
        with open('./tests/_correction/test_and2') as f:
            content = f.readlines()
    except:
        print('Error opening file for reading')
        raise

    parser = ExpertParser(content)
    tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("A") is True
    assert tree.resolve_query("G") is True
    assert tree.resolve_query("K") is False
    assert tree.resolve_query("P") is True

def test_test_or1():
    try:
        with open('./tests/_correction/test_or1') as f:
            content = f.readlines()
    except:
        print('Error opening file for reading')
        raise

    parser = ExpertParser(content)
    tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("A") is False

def test_test_or2():
    try:
        with open('./tests/_correction/test_or2') as f:
            content = f.readlines()
    except:
        print('Error opening file for reading')
        raise

    parser = ExpertParser(content)
    tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("A") is True

def test_test_or3():
    try:
        with open('./tests/_correction/test_or3') as f:
            content = f.readlines()
    except:
        print('Error opening file for reading')
        raise

    parser = ExpertParser(content)
    tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("A") is True

def test_test_or4():
    try:
        with open('./tests/_correction/test_or4') as f:
            content = f.readlines()
    except:
        print('Error opening file for reading')
        raise

    parser = ExpertParser(content)
    tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("A") is True

def test_test_paran1():
    try:
        with open('./tests/_correction/test_paran1') as f:
            content = f.readlines()
    except:
        print('Error opening file for reading')
        raise

    parser = ExpertParser(content)
    tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("E") is False

def test_test_paran2():
    try:
        with open('./tests/_correction/test_paran2') as f:
            content = f.readlines()
    except:
        print('Error opening file for reading')
        raise

    parser = ExpertParser(content)
    tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("E") is True

def test_test_paran3():
    try:
        with open('./tests/_correction/test_paran3') as f:
            content = f.readlines()
    except:
        print('Error opening file for reading')
        raise

    parser = ExpertParser(content)
    tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("E") is False

def test_test_paran4():
    try:
        with open('./tests/_correction/test_paran4') as f:
            content = f.readlines()
    except:
        print('Error opening file for reading')
        raise

    parser = ExpertParser(content)
    tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("E") is False

def test_test_paran5():
    try:
        with open('./tests/_correction/test_paran5') as f:
            content = f.readlines()
    except:
        print('Error opening file for reading')
        raise

    parser = ExpertParser(content)
    tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("E") is True

def test_test_paran6():
    try:
        with open('./tests/_correction/test_paran6') as f:
            content = f.readlines()
    except:
        print('Error opening file for reading')
        raise

    parser = ExpertParser(content)
    tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("E") is True

def test_test_paran7():
    try:
        with open('./tests/_correction/test_paran7') as f:
            content = f.readlines()
    except:
        print('Error opening file for reading')
        raise

    parser = ExpertParser(content)
    tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("E") is False

def test_test_paran8():
    try:
        with open('./tests/_correction/test_paran8') as f:
            content = f.readlines()
    except:
        print('Error opening file for reading')
        raise

    parser = ExpertParser(content)
    tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("E") is False

def test_test_paran9():
    try:
        with open('./tests/_correction/test_paran9') as f:
            content = f.readlines()
    except:
        print('Error opening file for reading')
        raise

    parser = ExpertParser(content)
    tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("E") is False

def test_test_paran10():
    try:
        with open('./tests/_correction/test_paran10') as f:
            content = f.readlines()
    except:
        print('Error opening file for reading')
        raise

    parser = ExpertParser(content)
    tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("E") is True

def test_test_same1():
    try:
        with open('./tests/_correction/test_same1') as f:
            content = f.readlines()
    except:
        print('Error opening file for reading')
        raise

    parser = ExpertParser(content)
    tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("A") is False

def test_test_same2():
    try:
        with open('./tests/_correction/test_same2') as f:
            content = f.readlines()
    except:
        print('Error opening file for reading')
        raise

    parser = ExpertParser(content)
    tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("A") is True

def test_test_same3():
    try:
        with open('./tests/_correction/test_same3') as f:
            content = f.readlines()
    except:
        print('Error opening file for reading')
        raise

    parser = ExpertParser(content)
    tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("A") is True

def test_test_same4():
    try:
        with open('./tests/_correction/test_same4') as f:
            content = f.readlines()
    except:
        print('Error opening file for reading')
        raise

    parser = ExpertParser(content)
    tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("A") is True

def test_test_xor1():
    try:
        with open('./tests/_correction/test_xor1') as f:
            content = f.readlines()
    except:
        print('Error opening file for reading')
        raise

    parser = ExpertParser(content)
    tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("A") is False

def test_test_xor2():
    try:
        with open('./tests/_correction/test_xor2') as f:
            content = f.readlines()
    except:
        print('Error opening file for reading')
        raise

    parser = ExpertParser(content)
    tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("A") is True

def test_test_xor3():
    try:
        with open('./tests/_correction/test_xor3') as f:
            content = f.readlines()
    except:
        print('Error opening file for reading')
        raise

    parser = ExpertParser(content)
    tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("A") is True

def test_test_xor4():
    try:
        with open('./tests/_correction/test_xor4') as f:
            content = f.readlines()
    except:
        print('Error opening file for reading')
        raise

    parser = ExpertParser(content)
    tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("A") is False

def test_test_neg1():
    try:
        with open('./tests/_correction/test_neg1') as f:
            content = f.readlines()
    except:
        print('Error opening file for reading')
        raise

    parser = ExpertParser(content)
    tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("A") is False

def test_test_neg2():
    try:
        with open('./tests/_correction/test_neg2') as f:
            content = f.readlines()
    except:
        print('Error opening file for reading')
        raise

    parser = ExpertParser(content)
    tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("A") is True

def test_test_neg3():
    try:
        with open('./tests/_correction/test_neg3') as f:
            content = f.readlines()
    except:
        print('Error opening file for reading')
        raise

    parser = ExpertParser(content)
    tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("A") is False

def test_test_neg4():
    try:
        with open('./tests/_correction/test_neg4') as f:
            content = f.readlines()
    except:
        print('Error opening file for reading')
        raise

    parser = ExpertParser(content)
    tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("A") is False

def test_test_neg5():
    try:
        with open('./tests/_correction/test_neg5') as f:
            content = f.readlines()
    except:
        print('Error opening file for reading')
        raise

    parser = ExpertParser(content)
    tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("A") is False

def test_test_slack1():
    try:
        with open('./tests/_examples/good_files/test_slack1') as f:
            content = f.readlines()
    except:
        print('Error opening file for reading')
        raise

    parser = ExpertParser(content)
    tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("A") is False

def test_test_slack2():
    try:
        with open('./tests/_examples/good_files/test_slack2') as f:
            content = f.readlines()
    except:
        print('Error opening file for reading')
        raise

    parser = ExpertParser(content)
    tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("A") is False

def test_test_slack3():
    try:
        with open('./tests/_examples/good_files/test_slack3') as f:
            content = f.readlines()
    except:
        print('Error opening file for reading')
        raise

    parser = ExpertParser(content)
    tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("C") is False

def test_test_slack4():
    try:
        with open('./tests/_examples/good_files/test_slack4') as f:
            content = f.readlines()
    except:
        print('Error opening file for reading')
        raise

    parser = ExpertParser(content)
    tree = NPITree(parser.structured_rules, parser.facts, parser.queries)
    assert tree.resolve_query("C") is False
