from factories.tree import TreeFactory


def test_direct_atoms():
    tree_ab = TreeFactory.get_ab()
    tree_ab.add_fact("A", True)
    tree_ab.add_fact("B", True)
    assert tree_ab.resolve_atom("A") is True
    assert tree_ab.resolve_atom("B") is True


def test_one_to_one_relations_0():
    tree_ab = TreeFactory.get_ab()
    tree_ab.add_fact("A", True)
    assert tree_ab.resolve_atom("A") is True
    assert tree_ab.resolve_atom("B") is True


def test_one_to_one_relations_1():
    tree_ab = TreeFactory.get_ab()
    tree_ab.add_fact("A", None)
    assert tree_ab.resolve_atom("A") is None
    assert tree_ab.resolve_atom("B") is None


def test_one_to_one_relations_2():
    tree_ab = TreeFactory.get_ab()
    tree_ab.add_fact("A", False)
    assert tree_ab.resolve_atom("A") is False
    assert tree_ab.resolve_atom("B") is False


def test_and_relations_true():
    tree = TreeFactory.get_and_abc()
    tree.add_fact("A", True)
    tree.add_fact("B", True)
    tree.add_fact("C", True)
    assert tree.resolve_atom("D") is True


def test_and_relations_false_0():
    tree = TreeFactory.get_and_abc()
    tree.add_fact("A", True)
    tree.add_fact("B", False)
    tree.add_fact("C", True)
    assert tree.resolve_atom("D") is False


def test_and_relations_false_1():
    tree = TreeFactory.get_and_abc()
    tree.add_fact("A", False)
    tree.add_fact("B", None)
    tree.add_fact("C", False)
    assert tree.resolve_atom("D") is False


def test_and_relations_none():
    tree = TreeFactory.get_and_abc()
    tree.add_fact("A", True)
    tree.add_fact("B", None)
    tree.add_fact("C", True)
    assert tree.resolve_atom("D") is None


def test_or_relations_true_0():
    tree = TreeFactory.get_or_ab()
    tree.add_fact("A", False)
    tree.add_fact("B", True)
    assert tree.resolve_atom("C") is True


def test_or_relations_true_1():
    tree = TreeFactory.get_or_abc()
    tree.add_fact("A", False)
    tree.add_fact("B", True)
    tree.add_fact("C", None)
    assert tree.resolve_atom("D") is True


def test_or_relations_false():
    tree = TreeFactory.get_or_abc()
    tree.add_fact("A", False)
    tree.add_fact("B", False)
    tree.add_fact("C", False)
    assert tree.resolve_atom("D") is False


def test_or_relations_none_0():
    tree = TreeFactory.get_or_abc()
    tree.add_fact("A", False)
    tree.add_fact("B", None)
    tree.add_fact("C", None)
    assert tree.resolve_atom("D") is None


def test_or_relations_none_1():
    tree = TreeFactory.get_or_ab()
    tree.add_fact("A", None)
    tree.add_fact("B", False)
    assert tree.resolve_atom("D") is None


def test_xor_relations_true_0():
    tree = TreeFactory.get_xor_abc()
    tree.add_fact("A", True)
    tree.add_fact("B", False)
    tree.add_fact("C", False)
    assert tree.resolve_atom("D") is True


def test_xor_relations_true_1():
    tree = TreeFactory.get_xor_abc()
    tree.add_fact("A", True)
    tree.add_fact("B", True)
    tree.add_fact("C", True)
    assert tree.resolve_atom("D") is True


def test_xor_relations_false_0():
    tree = TreeFactory.get_xor_abc()
    tree.add_fact("A", True)
    tree.add_fact("B", False)
    tree.add_fact("C", True)
    assert tree.resolve_atom("D") is False


'''
A ^ B ^ C => D
'''
def test_xor_relations_false_1():
    tree = TreeFactory.get_xor_abc()
    tree.add_fact("A", True)
    tree.add_fact("B", None)
    tree.add_fact("C", False)
    assert tree.resolve_atom("D") is None


def test_medium_true_0():
    tree = TreeFactory.get_medium_0()
    tree.add_fact("A", True)
    assert tree.resolve_atom("D") is True


def test_medium_true_1():
    tree = TreeFactory.get_medium_0()
    tree.add_fact("B", True)
    assert tree.resolve_atom("D") is True


def test_medium_true_2():
    tree = TreeFactory.get_medium_0()
    tree.add_fact("B", True)
    tree.add_fact("A", False)
    assert tree.resolve_atom("D") is True


def test_medium_true_3():
    tree = TreeFactory.get_medium_0()
    tree.add_fact("B", None)
    tree.add_fact("C", None)
    tree.add_fact("A", True)
    assert tree.resolve_atom("D") is True


def test_medium_false_0():
    tree = TreeFactory.get_medium_0()
    tree.add_fact("A", False)
    tree.add_fact("B", False)
    assert tree.resolve_atom("D") is False


def test_medium_none_0():
    tree = TreeFactory.get_medium_0()
    tree.add_fact("B", False)
    tree.add_fact("C", False)
    assert tree.resolve_atom("D") is None


def test_medium_none_1():
    tree = TreeFactory.get_medium_0()
    tree.add_fact("A", False)
    tree.add_fact("C", False)
    tree.add_fact("B", None)
    assert tree.resolve_atom("D") is None


def test_hard_true_0():
    tree = TreeFactory.get_hard_0()
    tree.add_fact("D", True)
    assert tree.resolve_atom("C") is True


def test_hard_true_1():
    tree = TreeFactory.get_hard_0()
    tree.add_fact("A", True)
    tree.add_fact("B", True)
    assert tree.resolve_atom("C") is True


def test_hard_false_0():
    tree = TreeFactory.get_hard_0()
    tree.add_fact("A", False)
    assert tree.resolve_atom("C") is None


def test_hard_false_1():
    tree = TreeFactory.get_hard_0()
    tree.add_fact("D", False)
    assert tree.resolve_atom("C") is None


def test_hard_none_0():
    tree = TreeFactory.get_hard_0()
    tree.add_fact("A", True)
    tree.add_fact("B", True)
    assert tree.resolve_atom("D") is None


def test_hard_deduction_none_0():
    tree = TreeFactory.get_hard_deduction_1()
    tree.add_fact("D", True)
    assert tree.resolve_atom("A") is True # NOT SURE
    assert tree.resolve_atom("B") is True # NOT SURE


def test_hard_deduction_none_1():
    tree = TreeFactory.get_hard_deduction_1()
    tree.add_fact("D", False)
    assert tree.resolve_atom("A") is None
    assert tree.resolve_atom("B") is None


"""  D => (A | B) Avec D Vrai et A faux """
def test_hard_deduction_true():
    tree = TreeFactory.get_hard_deduction_2()
    tree.add_fact("D", True)
    tree.add_fact("A", False)
    assert tree.resolve_atom("B") is True

"""  D => (A | B) Avec D Vrai et A True """
def test_hard_deduction_true():
    tree = TreeFactory.get_hard_deduction_2()
    tree.add_fact("D", True)
    tree.add_fact("A", True)
    assert tree.resolve_atom("B") is None


""" D => (A ^ B) Avec 2 connu """
def test_hard_xor_0():
    tree = TreeFactory.get_hard_xor()
    tree.add_fact("D", True)
    tree.add_fact("A", False)
    assert tree.resolve_atom("B") is True


""" D => (A ^ B ^ C) with D True , C False => Indef """
def test_hard_xor_abc():
    tree = TreeFactory.get_hard_xor_abc()
    tree.add_fact("D", True)
    tree.add_fact("C", False)
    assert tree.resolve_atom("B") is None
    assert tree.resolve_atom("A") is None


""" D => (A ^ B ^ C) with D True , A true => All to Indef """
def test_hard_xor_abc_1():
    tree = TreeFactory.get_hard_xor_abc()
    tree.add_fact("D", True)
    tree.add_fact("A", True)
    assert tree.resolve_atom("B") is None
    assert tree.resolve_atom("C") is None
