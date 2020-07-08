import unittest

from tbs.binary_hypergraph import s_0, random_subset, BinaryMixedTree
# from tbs.binary_hypergraph import BinaryMixedTree
from tbs.graph import MixedGraph, DIRECTED_EDGE, UNDIRECTED_EDGE


class TestEdgeChoice1(unittest.TestCase):
    def test_one_edge(self):
        g = BinaryMixedTree(MixedGraph({1, 2}, [(1, 2)]))

        value = g.edge_choice_for_algo1()
        expected = frozenset([frozenset([1]), frozenset([2])])

        self.assertEqual(expected, value)

    def test_one_undirected(self):
        g = BinaryMixedTree(MixedGraph({0, 1, 2, 3, 4}, [(2, 3)]))
        g.update(DIRECTED_EDGE,
                 [(frozenset([2]), frozenset([0])), (frozenset([3]), frozenset([1])), (frozenset([3]), frozenset([4]))],
                 node_creation=False)

        value = g.edge_choice_for_algo1()
        expected = frozenset([frozenset([3]), frozenset([2])])

        self.assertEqual(expected, value)

    def test_one_edge_available(self):
        g = BinaryMixedTree(MixedGraph({0, 1, 2, 3}, [(1, 2), (0, 1)]))
        g.add_directed(frozenset([3]), frozenset([2]))

        value = g.edge_choice_for_algo1()
        expected = frozenset([frozenset([1]), frozenset([0])])

        self.assertEqual(value, expected)

    def test_no_edge(self):
        g = BinaryMixedTree(MixedGraph({1}))
        with self.assertRaises(ValueError):
            g.edge_choice_for_algo1()

    def test_no_edge_available(self):
        g = BinaryMixedTree(MixedGraph({0, 1, 2, 3, 4}, [(0, 1), (1, 2)]))
        g.add_directed(frozenset([4]), frozenset([0]))
        g.add_directed(frozenset([3]), frozenset([2]))
        with self.assertRaises(ValueError):
            g.edge_choice_for_algo1()

    def test_multiple_edges_available(self):
        g = BinaryMixedTree(MixedGraph({0, 1, 2, 3}, [(0, 1), (0, 2), (2, 3)]))
        value = g.edge_choice_for_algo1()
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


class TestBasicTreeConstruction1(unittest.TestCase):
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


class TestKruskal(unittest.TestCase):
    def test_empty_grap(self):
        g = BinaryMixedTree(MixedGraph())

        value = g.kruskal()
        expected = set()

        self.assertEqual(value, expected)

    def test_simple_graph(self):
        g = BinaryMixedTree(MixedGraph({0, 1, 2}, [(0, 1), (1, 2)]))

        value = g.kruskal()
        expected = {frozenset([0, 1, 2])}

        self.assertEqual(value, expected)

    def test_directed_graph(self):
        g = BinaryMixedTree(MixedGraph({0, 1, 2}))
        g.update(DIRECTED_EDGE, [(frozenset([0]), frozenset([1])), (frozenset([1]), frozenset([2]))])

        value = g.kruskal()
        expected = {frozenset([0, 1, 2])}

        self.assertEqual(value, expected)

    def test_non_connected_graph(self):
        g = BinaryMixedTree(MixedGraph({0, 1, 2, 3}, [(0, 1), (2, 3)]))

        value = g.kruskal()
        expected = {frozenset([0, 1]), frozenset([2, 3])}

        self.assertEqual(value, expected)

    def test_mixed_non_connected_graph(self):
        g = BinaryMixedTree(MixedGraph({0, 1, 2, 3, 4, 5}, [(0, 1), (0, 3)]))
        g.update(DIRECTED_EDGE, [(frozenset([0]), frozenset([2])), (frozenset([4]), frozenset([5]))])

        value = g.kruskal()
        expected = {frozenset([0, 1, 2, 3]), frozenset([4, 5])}

        self.assertEqual(value, expected)


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


class TestEdgeChoice2(unittest.TestCase):
    def test_edges_in_homogeneous(self):
        g = BinaryMixedTree(MixedGraph({0, 1, 2, 3, 4, 5}, [(0, 1), (1, 2), (3, 4), (4, 5)]))
        g.add_directed(frozenset([2]), frozenset([3]))

        value = g.edges_in_homogeneous_subset(g.homogeneous_subset())
        expected = [frozenset([frozenset([0]), frozenset([1])]), frozenset([frozenset([1]), frozenset([2])])]

        self.assertEqual(value, expected)

    def test_edges_in_homogeneous_simple_graph(self):
        g = BinaryMixedTree(MixedGraph({0, 1}))
        g.add_directed(frozenset([0]), frozenset([1]))

        value = g.edges_in_homogeneous_subset(g.homogeneous_subset())
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

        value = g.edge_choice_for_algo3(map, h)
        expected = frozenset({frozenset([4]), frozenset([5])})

        self.assertEqual(expected, value)

