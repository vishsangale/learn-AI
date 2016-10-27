import maximum_clique


def test_clique1_empty_graph():
    g = maximum_clique.Graph('Filename1.dot')
    assert 0 == maximum_clique.maximum_clique(g)


def test_clique2_with_single_node():
    g = maximum_clique.Graph('Filename2.dot')
    assert 1 == maximum_clique.maximum_clique(g)


def test_clique3():
    g = maximum_clique.Graph('Filename3.dot')
    assert 4 == maximum_clique.maximum_clique(g)


def test_clique4():
    g = maximum_clique.Graph('Filename4.dot')
    assert 4 == maximum_clique.maximum_clique(g)


def test_clique5():
    g = maximum_clique.Graph('Filename5.dot')
    assert 3 == maximum_clique.maximum_clique(g)


def test_clique6():
    g = maximum_clique.Graph('Filename6.dot')
    assert 3 == maximum_clique.maximum_clique(g)
