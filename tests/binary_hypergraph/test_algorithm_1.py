import unittest

from tbs.binary_hypergraph import s_0, BinaryMixedTree, basic_tree_construction, tree_sequence_construction
from tbs.graph import MixedGraph, DIRECTED_EDGE


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


class TestBasicTreeConstruction1(unittest.TestCase):
    def test_one_undirected(self):
        g = BinaryMixedTree(MixedGraph({0, 1, 2}, [(0, 1)]))
        g.add_directed(frozenset([1]), frozenset([2]))

        value_graph, value_map = basic_tree_construction(g, s_0(g))
        expected_graph = BinaryMixedTree(MixedGraph({2}))
        expected_graph.add(frozenset([0, 1]))
        expected_graph.add_undirected(frozenset([2]), frozenset([0, 1]))
        expected_map = {frozenset([0]): {frozenset([0])}, frozenset([1]): {frozenset([1])},
                        frozenset([2]): {frozenset([2])}, frozenset([0, 1]): {frozenset([0]), frozenset([1])}}

        self.assertEqual(expected_graph, value_graph)
        self.assertEqual(expected_map, value_map)

    def test_tree_sequence(self):
        g = BinaryMixedTree(MixedGraph({0, 1}, [(0, 1)]))
        value = tree_sequence_construction(g)

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
