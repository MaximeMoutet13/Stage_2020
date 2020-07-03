import unittest

from tbs.binary_hypergraph._algo1_functions import s_0, random_subset
from tbs.binary_hypergraph._mixed_tree import BinaryMixedTree
from tbs.graph import MixedGraph, DIRECTED_EDGE, UNDIRECTED_EDGE


class TestEdgeChoice(unittest.TestCase):
    def test_one_edge(self):
        g = BinaryMixedTree(MixedGraph({1, 2}, [(1, 2)]))

        value = g.edge_choice()
        expected = frozenset([frozenset([1]), frozenset([2])])

        self.assertEqual(expected, value)

    def test_one_undirected(self):
        g = BinaryMixedTree(MixedGraph({0, 1, 2, 3, 4}, [(2, 3)]))
        g.update(DIRECTED_EDGE,
                 [(frozenset([2]), frozenset([0])), (frozenset([3]), frozenset([1])), (frozenset([3]), frozenset([4]))],
                 node_creation=False)

        value = g.edge_choice()
        expected = frozenset([frozenset([3]), frozenset([2])])

        self.assertEqual(expected, value)

    def test_one_edge_available(self):
        g = BinaryMixedTree(MixedGraph({0, 1, 2, 3}, [(1, 2), (0, 1)]))
        g.add_directed(frozenset([3]), frozenset([2]))

        value = g.edge_choice()
        expected = frozenset([frozenset([1]), frozenset([0])])

        self.assertEqual(value, expected)

    def test_no_edge(self):
        g = BinaryMixedTree(MixedGraph({1}))
        with self.assertRaises(ValueError):
            g.edge_choice()

    def test_no_edge_available(self):
        g = BinaryMixedTree(MixedGraph({0, 1, 2, 3, 4}, [(0, 1), (1, 2)]))
        g.add_directed(frozenset([4]), frozenset([0]))
        g.add_directed(frozenset([3]), frozenset([2]))
        with self.assertRaises(ValueError):
            g.edge_choice()

    def test_multiple_edges_available(self):
        g = BinaryMixedTree(MixedGraph({0, 1, 2, 3}, [(0, 1), (0, 2), (2, 3)]))
        value = g.edge_choice()
        self.assertTrue(value in g.edges[0])


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


class TestLoop(unittest.TestCase):
    def test_move_undirected_from_to_emptyset(self):
        g = BinaryMixedTree(MixedGraph({1, 2, 3}, [(2, 3), (3, 1)]))
        empty_set = set()
        g.move_undirected_from_to(3, 1, empty_set)

        expected = BinaryMixedTree(MixedGraph({1, 2, 3}, [(2, 3), (3, 1)]))

        self.assertEqual(expected, g)

    def test_move_undirected(self):
        g = BinaryMixedTree(MixedGraph({0, 1, 2, 3, 4}, [(2, 4)]))
        g.add(frozenset([2, 3]))
        g.update(DIRECTED_EDGE, [(frozenset([2]), frozenset([0])), (frozenset([3]), frozenset([1])),
                                 (frozenset([2]), frozenset([2, 3])), (frozenset([3]), frozenset([2, 3]))],
                 node_creation=False)
        g.move_undirected_from_to(frozenset([2]), frozenset([2, 3]), {frozenset([4])})

        expected = BinaryMixedTree(MixedGraph({0, 1, 2, 3, 4}))
        expected.add(frozenset([2, 3]))
        expected.update(DIRECTED_EDGE, [(frozenset([2]), frozenset([0])), (frozenset([3]), frozenset([1])),
                                        (frozenset([2]), frozenset([2, 3])), (frozenset([3]), frozenset([2, 3]))],
                        node_creation=False)
        expected.add_undirected(frozenset([4]), frozenset([2, 3]))

        self.assertEqual(g, expected)


class TestBasicTreeConstruction(unittest.TestCase):
    def test_one_undirected(self):
        g = BinaryMixedTree(MixedGraph({0, 1, 2}, [(0, 1)]))
        g.add_directed(frozenset([1]), frozenset([2]))

        value_graph, value_map = g.basic_tree_construction(s_0(g))
        expected_graph = BinaryMixedTree(MixedGraph({2}))
        expected_graph.add(frozenset([0, 1]))
        expected_graph.add_undirected(frozenset([2]), frozenset([0, 1]))
        expected_map = {frozenset([0]): {frozenset([0])}, frozenset([1]): {frozenset([1])},
                        frozenset([2]): {frozenset([2])}, frozenset([0, 1]): {frozenset([0]), frozenset([1])}}

        self.assertEqual(expected_graph, value_graph)
        self.assertEqual(expected_map, value_map)

    def test_tree_sequence(self):
        g = BinaryMixedTree(MixedGraph({0, 1}, [(0, 1)]))
        value = g.tree_sequence_construction()

        g2 = BinaryMixedTree(MixedGraph())
        g2.add(frozenset([0, 1]))

        expected = [
            (g, s_0(g)),
            (g2, {
                frozenset([1]): {frozenset([1])},
                frozenset([0]): {frozenset([0])},
                frozenset([0, 1]): {frozenset([0]), frozenset([1])}
            }
             )
        ]

        self.assertEqual(value, expected)
