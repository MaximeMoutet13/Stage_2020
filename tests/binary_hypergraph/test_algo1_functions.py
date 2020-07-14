import unittest

from tbs.binary_hypergraph._algo1_functions import random_subset, edge_choice_for_algo1
from tbs.binary_hypergraph import BinaryMixedTree, BasicTreeConstruction, MixedGraph, DIRECTED_EDGE


class TestEdgeChoice1(unittest.TestCase):
    def test_one_edge(self):
        g = BinaryMixedTree(MixedGraph({1, 2}, [(1, 2)]))

        value = edge_choice_for_algo1(BasicTreeConstruction(g))
        expected = frozenset([frozenset([1]), frozenset([2])])

        self.assertEqual(expected, value)

    def test_one_undirected(self):
        g = BinaryMixedTree(MixedGraph({0, 1, 2, 3, 4}, [(2, 3)]))
        g.update(DIRECTED_EDGE,
                 [(frozenset([2]), frozenset([0])), (frozenset([3]), frozenset([1])), (frozenset([3]), frozenset([4]))],
                 node_creation=False)

        value = edge_choice_for_algo1(BasicTreeConstruction(g))
        expected = frozenset([frozenset([3]), frozenset([2])])

        self.assertEqual(expected, value)

    def test_one_edge_available(self):
        g = BinaryMixedTree(MixedGraph({0, 1, 2, 3}, [(1, 2), (0, 1)]))
        g.add_directed(frozenset([3]), frozenset([2]))

        value = edge_choice_for_algo1(BasicTreeConstruction(g))
        expected = frozenset([frozenset([1]), frozenset([0])])

        self.assertEqual(value, expected)

    def test_no_edge(self):
        g = BinaryMixedTree(MixedGraph({1}))
        with self.assertRaises(ValueError):
            edge_choice_for_algo1(BasicTreeConstruction(g))

    def test_no_edge_available(self):
        g = BinaryMixedTree(MixedGraph({0, 1, 2, 3, 4}, [(0, 1), (1, 2)]))
        g.add_directed(frozenset([4]), frozenset([0]))
        g.add_directed(frozenset([3]), frozenset([2]))
        with self.assertRaises(ValueError):
            edge_choice_for_algo1(BasicTreeConstruction(g))

    def test_multiple_edges_available(self):
        g = BinaryMixedTree(MixedGraph({0, 1, 2, 3}, [(0, 1), (0, 2), (2, 3)]))
        value = edge_choice_for_algo1(BasicTreeConstruction(g))
        self.assertTrue(value in g.edges[0])


class TestSubset(unittest.TestCase):
    def test_empty_subset(self):
        s = set()
        s2 = random_subset(s)
        self.assertEqual(s2, set())

    def test_issubset(self):
        s = {1, 3, 5, 23, 547}
        s2 = random_subset(s)
        self.assertTrue(s2.issubset(s))
