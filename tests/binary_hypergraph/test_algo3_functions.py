import unittest

from tbs.binary_hypergraph import supremum, minimum, delta_z_subset_algo3, edge_choice_for_algo3, \
    edges_in_homogeneous_subset, BasicTreeConstruction, HyperGraph, BinaryMixedTree, MixedGraph, s_0


class TestSets(unittest.TestCase):
    def test_supremum_binary_little_hypergraph(self):
        s = frozenset(
            [frozenset([frozenset([0]), frozenset([1])]), frozenset([frozenset([1])]), frozenset([frozenset([0])
                                                                                                  ])])
        x, y = frozenset([0]), frozenset([1])

        value = supremum({x}, {y}, s)
        expected = {frozenset([0]), frozenset([1])}

        self.assertEqual(value, expected)

    def test_supremum(self):
        s = frozenset([
            frozenset([frozenset([0])]),
            frozenset([frozenset([1])]),
            frozenset([frozenset([2])]),
            frozenset([frozenset([3])]),
            frozenset([frozenset([0]), frozenset([1])]),
            frozenset([frozenset([2]), frozenset([3])]),
            frozenset([frozenset([0]), frozenset([1]), frozenset([3])]),
            frozenset([frozenset([0]), frozenset([1]), frozenset([2]), frozenset([3])])
        ])

        value = supremum({frozenset([0]), frozenset([1])}, {frozenset([3])}, s)
        expected = {frozenset([0]), frozenset([1]), frozenset([3])}

        self.assertEqual(value, expected)

    def test_minimum(self):
        s = frozenset(
            [frozenset([frozenset([0]), frozenset([1])]), frozenset([frozenset([1])]), frozenset([frozenset([0])
                                                                                                  ])])
        sets = [frozenset([0]), frozenset([1])]

        value = minimum(sets)
        expected = frozenset([0])

        self.assertEqual(value, expected)

    def test_minimum_2(self):
        s = frozenset([
            frozenset([frozenset([0])]),
            frozenset([frozenset([1])]),
            frozenset([frozenset([2])]),
            frozenset([frozenset([3])]),
            frozenset([frozenset([0]), frozenset([1])]),
            frozenset([frozenset([2]), frozenset([3])]),
            frozenset([frozenset([0]), frozenset([1]), frozenset([3])]),
            frozenset([frozenset([0]), frozenset([1]), frozenset([2]), frozenset([3])])
        ])

        sets = [frozenset([frozenset([0]), frozenset([1]), frozenset([2])]),
                frozenset([frozenset([2]), frozenset([3])])]

        value = minimum(sets)
        expected = frozenset([frozenset([0]), frozenset([1]), frozenset([2])])

        self.assertEqual(expected, value)


class TestEdgeChoice(unittest.TestCase):
    def test_edges_in_homogeneous(self):
        g = BinaryMixedTree(MixedGraph({0, 1, 2, 3, 4, 5}, [(0, 1), (1, 2), (3, 4), (4, 5)]))
        g.add_directed(frozenset([2]), frozenset([3]))

        value = edges_in_homogeneous_subset(g, g.homogeneous_subset())
        expected = [frozenset([frozenset([0]), frozenset([1])]), frozenset([frozenset([1]), frozenset([2])])]

        self.assertEqual(value, expected)

    def test_edges_in_homogeneous_simple_graph(self):
        g = BinaryMixedTree(MixedGraph({0, 1}))
        g.add_directed(frozenset([0]), frozenset([1]))

        value = edges_in_homogeneous_subset(g, g.homogeneous_subset())
        expected = []

        self.assertEqual(value, expected)

    def test_edge_choice_for_algo3(self):
        h = HyperGraph(
            frozenset([frozenset([1]), frozenset([2]), frozenset([3]), frozenset([4]), frozenset([5]), frozenset([6])]),
            frozenset([frozenset([frozenset([1])]),
                       frozenset([frozenset([2])]),
                       frozenset([frozenset([3])]),
                       frozenset([frozenset([4])]),
                       frozenset([frozenset([5])]),
                       frozenset([frozenset([6])]),
                       frozenset([frozenset([4]), frozenset([5])]),
                       frozenset([frozenset([5]), frozenset([6])]),
                       frozenset([frozenset([1]), frozenset([2]), frozenset([3]), frozenset([4]), frozenset([5]),
                                  frozenset([6])])]))

        g = BinaryMixedTree(MixedGraph({1, 2, 3, 4, 5, 6}, [(1, 2), (2, 4), (4, 3), (4, 5), (5, 6)]))
        map = s_0(g)

        value = edge_choice_for_algo3(BasicTreeConstruction(g, map, h))
        expected = frozenset({frozenset([4]), frozenset([5])})

        self.assertEqual(list(g.edges[0]), edges_in_homogeneous_subset(g, g.homogeneous_subset()))
        self.assertEqual(expected, value)

    def test_one_edge_available(self):
        h = HyperGraph(frozenset([frozenset([1]), frozenset([2]), frozenset([3])]),
                       frozenset([frozenset([frozenset([1])]),
                                  frozenset([frozenset([2])]),
                                  frozenset([frozenset([3])]),
                                  frozenset([frozenset([1]), frozenset([2])]),
                                  frozenset([frozenset([2]), frozenset([3])]),
                                  frozenset([frozenset([i + 1]) for i in range(3)])
                                  ]))
        t = BinaryMixedTree(MixedGraph({1, 2, 3}, [(1, 3)]))
        t.add_directed(frozenset([1]), frozenset([2]))

        self.assertEqual(edge_choice_for_algo3(BasicTreeConstruction(t, s_0(t), h)),
                         frozenset([frozenset([1]), frozenset([3])]))

    def test_edge_choice(self):
        g = HyperGraph(frozenset([frozenset([i]) for i in range(1, 7)]))
        for i in range(1, 7):
            g.add_edge(frozenset([frozenset([i])]))
        g.add_edge(frozenset([frozenset([i]) for i in range(1, 7)]))
        g.add_edge(frozenset([frozenset([1]), frozenset([2])]))
        g.add_edge(frozenset([frozenset([4]), frozenset([5])]))
        g.add_edge(frozenset([frozenset([5]), frozenset([6])]))
        g.add_edge(frozenset([frozenset([4]), frozenset([5]), frozenset([6])]))
        g.add_edge(frozenset([frozenset([3]), frozenset([4]), frozenset([5])]))
        g.add_edge(frozenset([frozenset([3]), frozenset([4]), frozenset([5]), frozenset([6])]))
        g.add_edge(frozenset([frozenset([1]), frozenset([2]), frozenset([3]), frozenset([4]), frozenset([5])]))

        t = BinaryMixedTree(MixedGraph({1, 2, 3, 4, 5, 6}, [(1, 3), (3, 6), (1, 5)]))
        t.add_directed(frozenset([1]), frozenset([2]))
        t.add_directed(frozenset([3]), frozenset([4]))

        self.assertEqual(edges_in_homogeneous_subset(t, t.homogeneous_subset()), list(t.edges[0]))

        value = edge_choice_for_algo3(BasicTreeConstruction(t, s_0(t), g))
        self.assertEqual(value, frozenset([frozenset([1]), frozenset([3])]))


class TestDeltaZSubset(unittest.TestCase):
    def test_empty_delta_z(self):
        h = HyperGraph(frozenset([frozenset([1]), frozenset([2]), frozenset([3])]),
                       frozenset([frozenset([frozenset([1])]),
                                  frozenset([frozenset([2])]),
                                  frozenset([frozenset([3])]),
                                  frozenset([frozenset([1]), frozenset([2])]),
                                  frozenset([frozenset([2]), frozenset([3])]),
                                  frozenset([frozenset([i + 1]) for i in range(3)])
                                  ]))
        t = BinaryMixedTree(MixedGraph({1, 2, 3}))
        t.add(frozenset([1, 3]))
        t.add_directed(frozenset([1]), frozenset([2]))

        self.assertEqual(
            delta_z_subset_algo3(BasicTreeConstruction(t, s_0(t), h), set(), frozenset([1, 3]), frozenset([1])), set())

    def test_delta_z(self):
        g = HyperGraph(frozenset([frozenset([i]) for i in range(1, 7)]))
        for i in range(1, 7):
            g.add_edge(frozenset([frozenset([i])]))
        g.add_edge(frozenset([frozenset([i]) for i in range(1, 7)]))
        g.add_edge(frozenset([frozenset([1]), frozenset([2])]))
        g.add_edge(frozenset([frozenset([4]), frozenset([5])]))
        g.add_edge(frozenset([frozenset([5]), frozenset([6])]))
        g.add_edge(frozenset([frozenset([4]), frozenset([5]), frozenset([6])]))
        g.add_edge(frozenset([frozenset([3]), frozenset([4]), frozenset([5])]))
        g.add_edge(frozenset([frozenset([3]), frozenset([4]), frozenset([5]), frozenset([6])]))
        g.add_edge(frozenset([frozenset([1]), frozenset([2]), frozenset([3]), frozenset([4]), frozenset([5])]))

        t = BinaryMixedTree(MixedGraph({1, 2, 3, 4, 5, 6}, [(3, 6), (1, 5)]))
        s = s_0(t)
        s[frozenset([1, 3])] = {frozenset([1]), frozenset([3])}
        t.add(frozenset([1, 3]))
        t.add_directed(frozenset([1]), frozenset([2]))
        t.add_directed(frozenset([3]), frozenset([4]))


        expected = {frozenset([5])}
        value = delta_z_subset_algo3(BasicTreeConstruction(t, s, g), frozenset([frozenset([5])]),
                                     frozenset([1, 3]), frozenset([1]))
        self.assertEqual(expected, value)
