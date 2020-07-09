import unittest

from tbs.binary_hypergraph import supremum, minimum, BinaryMixedTree, MixedGraph, s_0, edge_choice_for_algo3, \
    edges_in_homogeneous_subset


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
        h = {
            frozenset([frozenset([1])]),
            frozenset([frozenset([2])]),
            frozenset([frozenset([3])]),
            frozenset([frozenset([4])]),
            frozenset([frozenset([5])]),
            frozenset([frozenset([6])]),
            frozenset([frozenset([4]), frozenset([5])]),
            frozenset([frozenset([5]), frozenset([6])]),
            frozenset([frozenset([1]), frozenset([2]), frozenset([3]), frozenset([4]), frozenset([5]), frozenset([6])])
        }
        g = BinaryMixedTree(MixedGraph({1, 2, 3, 4, 5, 6}, [(1, 2), (2, 4), (4, 3), (4, 5), (5, 6)]))
        map = s_0(g)

        value = edge_choice_for_algo3(g, map, h)
        expected = frozenset({frozenset([4]), frozenset([5])})

        self.assertEqual(expected, value)
