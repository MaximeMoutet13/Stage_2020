import unittest

from tbs.binary_hypergraph import BinaryMixedTree
from tbs.graph import MixedGraph, DIRECTED_EDGE, connected_parts


class TestKruskal(unittest.TestCase):
    def test_empty_grap(self):
        g = BinaryMixedTree(MixedGraph())
        g = g.underlying_undirected_graph()
        value = connected_parts(g)
        expected = set()

        self.assertEqual(value, expected)

    def test_one_vertex_graph(self):
        g = BinaryMixedTree(MixedGraph({0}))
        g = g.underlying_undirected_graph()

        value2 = connected_parts(g)
        expected = frozenset([frozenset([frozenset([0])])])
        self.assertEqual(value2, expected)

    def test_connected_subset(self):
        g = BinaryMixedTree(MixedGraph({0, 1, 2}, [(0, 1), (1, 2)]))
        g = g.underlying_undirected_graph()

        expected = frozenset([frozenset([frozenset([1]), frozenset([2])])])
        value = connected_parts(g, vertex_subset=frozenset([frozenset([1]), frozenset([2])]))

        self.assertEqual(expected, value)

    def test_non_connected_subset(self):
        g = BinaryMixedTree(MixedGraph({0, 1, 2}, [(0, 1), (1, 2)]))
        g = g.underlying_undirected_graph()

        expected = frozenset([frozenset([frozenset([0])]), frozenset([frozenset([2])])])
        value = connected_parts(g, vertex_subset=frozenset([frozenset([0]), frozenset([2])]))

        self.assertEqual(value, expected)

    def test_simple_graph(self):
        g = BinaryMixedTree(MixedGraph({0, 1, 2}, [(0, 1), (1, 2)]))
        g = g.underlying_undirected_graph()

        expected = frozenset([frozenset([frozenset([0]), frozenset([1]), frozenset([2])])])
        value = connected_parts(g)

        self.assertEqual(expected, value)

    def test_bigger_graph(self):
        g = BinaryMixedTree(MixedGraph({0, 1, 2, 3, 4, 5, 6}, [(2, 3), (3, 4), (4, 0), (4, 5), (4, 6), (6, 1)]))
        g = g.underlying_undirected_graph()

        expected = {frozenset([frozenset([0]), frozenset([1]), frozenset([2]), frozenset([3]), frozenset([4]),
                               frozenset([5]), frozenset([6])])}
        value = connected_parts(g)

        self.assertEqual(expected, value)

    def test_directed_graph(self):
        g = BinaryMixedTree(MixedGraph({0, 1, 2}))
        g.update(DIRECTED_EDGE, [(frozenset([0]), frozenset([1])), (frozenset([1]), frozenset([2]))])
        g = g.underlying_undirected_graph()

        expected = {frozenset([frozenset([0]), frozenset([1]), frozenset([2])])}
        value = connected_parts(g)

        self.assertEqual(value, expected)

    def test_non_connected_graph(self):
        g = BinaryMixedTree(MixedGraph({0, 1, 2, 3, 4}, [(0, 1), (2, 3)]))
        g = g.underlying_undirected_graph()

        expected = {frozenset([frozenset([0]), frozenset([1])]), frozenset([frozenset([2]), frozenset([3])]),
                    frozenset([frozenset([4])])}
        value = connected_parts(g)

        self.assertEqual(value, expected)

    def test_mixed_non_connected_graph(self):
        g = BinaryMixedTree(MixedGraph({0, 1, 2, 3, 4, 5}, [(0, 1), (0, 3)]))
        g.update(DIRECTED_EDGE, [(frozenset([0]), frozenset([2])), (frozenset([4]), frozenset([5]))])
        g = g.underlying_undirected_graph()

        expected = {frozenset([frozenset([0]), frozenset([1]), frozenset([2]), frozenset([3])]),
                    frozenset([frozenset([4]), frozenset([5])])}
        value = connected_parts(g)

        self.assertEqual(value, expected)
