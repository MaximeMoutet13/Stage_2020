import unittest

from tbs.binary_hypergraph import BinaryMixedTree
from tbs.graph import MixedGraph, DIRECTED_EDGE, UNDIRECTED_EDGE, Graph


class TestUnion(unittest.TestCase):
    def test_init_one_edge(self):
        g = BinaryMixedTree(MixedGraph({1, 2}, [(1, 2)]))
        v_xy = g.add_union(frozenset([1]), frozenset([2]))

        expected = BinaryMixedTree(MixedGraph({1, 2}))
        expected.add(frozenset([1, 2]))
        expected.add_directed(frozenset([1]), frozenset([1, 2]))
        expected.add_directed(frozenset([2]), frozenset([1, 2]))

        self.assertEqual(g, expected)
        self.assertEqual(v_xy, frozenset([1, 2]))

    def test_init_one_undirected(self):
        g = BinaryMixedTree(MixedGraph({0, 1, 2, 3, 4}, [(2, 3)]))
        g.update(DIRECTED_EDGE,
                 [(frozenset([2]), frozenset([0])), (frozenset([3]), frozenset([1])), (frozenset([3]), frozenset([4]))],
                 node_creation=False)
        v_xy = g.add_union(frozenset([2]), frozenset([3]))

        expected = BinaryMixedTree(MixedGraph({0, 1, 2, 3, 4}))
        expected.add(frozenset([2, 3]))
        expected.update(DIRECTED_EDGE, [(frozenset([2]), frozenset([0])), (frozenset([3]), frozenset([1])),
                                        (frozenset([3]), frozenset([4])), (frozenset([2]), frozenset([2, 3])),
                                        (frozenset([3]), frozenset([2, 3]))], node_creation=False)

        self.assertEqual(g, expected)
        self.assertEqual(v_xy, frozenset([2, 3]))


class TestRestriction(unittest.TestCase):
    def test_restrict(self):
        g = BinaryMixedTree(MixedGraph({0, 1, 2, 3}, [(0, 1), (1, 2)]))
        g.add_directed(frozenset([1]), frozenset([3]))

        h = g.restriction(frozenset([frozenset([0]), frozenset([1]), frozenset([2])]))

        self.assertEqual(h, BinaryMixedTree(MixedGraph({0, 1, 2}, [(0, 1), (1, 2)])))

    def test_restrict_error(self):
        g = BinaryMixedTree(MixedGraph({0, 1, 2, 3}, [(0, 1), (1, 2)]))
        g.add_directed(frozenset([1]), frozenset([3]))

        with self.assertRaises(ValueError):
            g.restriction(frozenset([frozenset([4])]))


class TestHomogeneousSubset(unittest.TestCase):
    def test_one_vertex_homogeneous_subset(self):
        g = BinaryMixedTree(MixedGraph({0}))

        value = g.homogeneous_subset()
        expected = {frozenset([0])}

        self.assertEqual(value, expected)

    def test_simple_homogeneous_subset(self):
        g = BinaryMixedTree(MixedGraph({0, 1, 2}, [(0, 2)]))
        g.add_directed(frozenset([0]), frozenset([1]))

        value = g.homogeneous_subset()
        expected = {frozenset([0]), frozenset([2])}

        self.assertEqual(value, expected)

    def test_homogeneous_subset(self):
        g = BinaryMixedTree(MixedGraph({0, 1, 2, 3, 4, 5}, [(0, 1), (1, 2), (3, 4), (4, 5)]))
        g.add_directed(frozenset([2]), frozenset([3]))

        value = g.homogeneous_subset()
        expected = {frozenset([0]), frozenset([1]), frozenset([2])}

        self.assertEqual(value, expected)

    def test_homogeneous_subset_2(self):
        g = BinaryMixedTree(MixedGraph({0, 1, 2, 3, 4, 5}, [(1, 2), (2, 3), (3, 4), (4, 5)]))
        g.add_directed(frozenset([0]), frozenset([1]))

        value = g.homogeneous_subset()
        expected = {frozenset([0])}

        self.assertEqual(value, expected)


class TestMixedTree(unittest.TestCase):
    def test_undirected_tree(self):
        g = BinaryMixedTree(MixedGraph({0, 1, 2, 3}, [(0, 1), (1, 2)]))
        g.add_directed(frozenset([2]), frozenset([3]))

        h = g.underlying_undirected_graph()

        self.assertEqual(h, Graph.from_edges(
            [(frozenset([0]), frozenset([1])), (frozenset([1]), frozenset([2])), (frozenset([2]), frozenset([3]))]))
