from factories.tree import TreeFactory


def test_direct_atoms():
    tree_ab = TreeFactory.get_ab()
    tree_ab.set_atom_state("A", True)
    tree_ab.set_atom_state("B", True)
    assert tree_ab.resolve_query("A") is True
    assert tree_ab.resolve_query("B") is True


def test_one_to_one_relations_0():
    tree_ab = TreeFactory.get_ab()
    tree_ab.set_atom_state("A", True)
    assert tree_ab.resolve_query("A") is True
    assert tree_ab.resolve_query("B") is True


def test_one_to_one_relations_1():
    tree_ab = TreeFactory.get_ab()
    tree_ab.set_atom_state("A", None)
    assert tree_ab.resolve_query("A") is None
    assert tree_ab.resolve_query("B") is None


def test_one_to_one_relations_2():
    tree_ab = TreeFactory.get_ab()
    tree_ab.set_atom_state("A", False)
    assert tree_ab.resolve_query("A") is False
    assert tree_ab.resolve_query("B") is False


def test_and_relations_true():
    tree = TreeFactory.get_and_abc()
    tree.set_atom_state("A", True)
    tree.set_atom_state("B", True)
    tree.set_atom_state("C", True)
    assert tree.resolve_query("D") is True


def test_and_relations_false_0():
    tree = TreeFactory.get_and_abc()
    tree.set_atom_state("A", True)
    tree.set_atom_state("B", False)
    tree.set_atom_state("C", True)
    assert tree.resolve_query("D") is False


def test_and_relations_false_1():
    tree = TreeFactory.get_and_abc()
    tree.set_atom_state("A", False)
    tree.set_atom_state("B", None)
    tree.set_atom_state("C", False)
    assert tree.resolve_query("D") is False


def test_and_relations_none():
    tree = TreeFactory.get_and_abc()
    tree.set_atom_state("A", True)
    tree.set_atom_state("B", None)
    tree.set_atom_state("C", True)
    assert tree.resolve_query("D") is None


def test_or_relations_true_0():
    tree = TreeFactory.get_or_ab()
    tree.set_atom_state("A", False)
    tree.set_atom_state("B", True)
    assert tree.resolve_query("C") is True


def test_or_relations_true_1():
    tree = TreeFactory.get_or_abc()
    tree.set_atom_state("A", False)
    tree.set_atom_state("B", True)
    tree.set_atom_state("C", None)
    assert tree.resolve_query("D") is True


def test_or_relations_false():
    tree = TreeFactory.get_or_abc()
    tree.set_atom_state("A", False)
    tree.set_atom_state("B", False)
    tree.set_atom_state("C", False)
    assert tree.resolve_query("D") is False


def test_or_relations_none_0():
    tree = TreeFactory.get_or_abc()
    tree.set_atom_state("A", False)
    tree.set_atom_state("B", None)
    tree.set_atom_state("C", None)
    assert tree.resolve_query("D") is None


def test_or_relations_none_1():
    tree = TreeFactory.get_or_ab()
    tree.set_atom_state("A", None)
    tree.set_atom_state("B", False)
    assert tree.resolve_query("D") is None


def test_xor_relations_true_0():
    tree = TreeFactory.get_xor_abc()
    tree.set_atom_state("A", True)
    tree.set_atom_state("B", False)
    tree.set_atom_state("C", False)
    assert tree.resolve_query("D") is True


def test_xor_relations_true_1():
    tree = TreeFactory.get_xor_abc()
    tree.set_atom_state("A", True)
    tree.set_atom_state("B", True)
    tree.set_atom_state("C", True)
    assert tree.resolve_query("D") is True


def test_xor_relations_false_0():
    tree = TreeFactory.get_xor_abc()
    tree.set_atom_state("A", True)
    tree.set_atom_state("B", False)
    tree.set_atom_state("C", True)
    assert tree.resolve_query("D") is False


'''
A ^ B ^ C => D
'''
def test_xor_relations_false_1():
    tree = TreeFactory.get_xor_abc()
    tree.set_atom_state("A", True)
    tree.set_atom_state("B", None)
    tree.set_atom_state("C", False)
    assert tree.resolve_query("D") is None


def test_medium_true_0():
    tree = TreeFactory.get_medium_0()
    tree.set_atom_state("A", True)
    assert tree.resolve_query("D") is True


def test_medium_true_1():
    tree = TreeFactory.get_medium_0()
    tree.set_atom_state("B", True)
    assert tree.resolve_query("D") is True


def test_medium_true_2():
    tree = TreeFactory.get_medium_0()
    tree.set_atom_state("B", True)
    tree.set_atom_state("A", False)
    assert tree.resolve_query("D") is True


def test_medium_true_3():
    tree = TreeFactory.get_medium_0()
    tree.set_atom_state("B", None)
    tree.set_atom_state("C", None)
    tree.set_atom_state("A", True)
    assert tree.resolve_query("D") is True


def test_medium_false_0():
    tree = TreeFactory.get_medium_0()
    tree.set_atom_state("A", False)
    tree.set_atom_state("B", False)
    assert tree.resolve_query("D") is False


def test_medium_none_0():
    tree = TreeFactory.get_medium_0()
    tree.set_atom_state("B", False)
    tree.set_atom_state("C", False)
    assert tree.resolve_query("D") is None


def test_medium_none_1():
    tree = TreeFactory.get_medium_0()
    tree.set_atom_state("A", False)
    tree.set_atom_state("C", False)
    tree.set_atom_state("B", None)
    assert tree.resolve_query("D") is None


def test_hard_true_0():
    tree = TreeFactory.get_hard_0()
    tree.set_atom_state("D", True)
    assert tree.resolve_query("C") is True


def test_hard_true_1():
    tree = TreeFactory.get_hard_0()
    tree.set_atom_state("A", True)
    tree.set_atom_state("B", True)
    assert tree.resolve_query("C") is True


def test_hard_false_0():
    tree = TreeFactory.get_hard_0()
    tree.set_atom_state("A", False)
    assert tree.resolve_query("C") is None


def test_hard_false_1():
    tree = TreeFactory.get_hard_0()
    tree.set_atom_state("D", False)
    assert tree.resolve_query("C") is None


def test_hard_none_0():
    tree = TreeFactory.get_hard_0()
    tree.set_atom_state("A", True)
    tree.set_atom_state("B", True)
    assert tree.resolve_query("D") is None


def test_hard_deduction_none_0():
    tree = TreeFactory.get_hard_deduction_1()
    tree.set_atom_state("D", True)
    assert tree.resolve_query("A") is True # NOT SURE
    assert tree.resolve_query("B") is True # NOT SURE


def test_hard_deduction_none_1():
    tree = TreeFactory.get_hard_deduction_1()
    tree.set_atom_state("D", False)
    assert tree.resolve_query("A") is None
    assert tree.resolve_query("B") is None


"""  D => (A | B) Avec D Vrai et A faux """
def test_hard_deduction_true():
    tree = TreeFactory.get_hard_deduction_2()
    tree.set_atom_state("D", True)
    tree.set_atom_state("A", False)
    assert tree.resolve_query("B") is True

"""  D => (A | B) Avec D Vrai et A True """
def test_hard_deduction_true():
    tree = TreeFactory.get_hard_deduction_2()
    tree.set_atom_state("D", True)
    tree.set_atom_state("A", True)
    assert tree.resolve_query("B") is None


""" D => (A ^ B) Avec 2 connu """
def test_hard_xor_0():
    tree = TreeFactory.get_hard_xor()
    tree.set_atom_state("D", True)
    tree.set_atom_state("A", False)
    assert tree.resolve_query("B") is True


""" D => (A ^ B ^ C) with D True , C False => Indef """
def test_hard_xor_abc():
    tree = TreeFactory.get_hard_xor_abc()
    tree.set_atom_state("D", True)
    tree.set_atom_state("C", False)
    assert tree.resolve_query("B") is None
    assert tree.resolve_query("A") is None


""" D => (A ^ B ^ C) with D True , A true => All to Indef """
def test_hard_xor_abc_1():
    tree = TreeFactory.get_hard_xor_abc()
    tree.set_atom_state("D", True)
    tree.set_atom_state("A", True)
    assert tree.resolve_query("B") is None
    assert tree.resolve_query("C") is None


'''
(A | B) => C
D => (A & B)
'''
def test_hard_combi_0():
    tree = TreeFactory.get_hard_combi_0()
    tree.set_atom_state("D", True)
    assert tree.resolve_query("B") is True
    assert tree.resolve_query("C") is True


'''
(A | B) => C
D => (A | B)
'''
def test_hard_combi_1():
    tree = TreeFactory.get_hard_combi_1()
    tree.set_atom_state("D", True)
    assert tree.resolve_query("A") is None
    assert tree.resolve_query("B") is None
    assert tree.resolve_query("C") is True


'''
(A | B) => C
D => (A | B)
'''
def test_hard_combi_2():
    tree = TreeFactory.get_hard_combi_1()
    tree.set_atom_state("D", False)
    assert tree.resolve_query("A") is None
    assert tree.resolve_query("B") is None
    assert tree.resolve_query("C") is None

