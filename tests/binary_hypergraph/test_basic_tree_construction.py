import unittest

from tbs.binary_hypergraph import s_0, BinaryMixedTree, MixedGraph, DIRECTED_EDGE, HyperGraph, \
    BasicTreeConstruction, StratAlgo1, StratAlgo3


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


class TestAlgo1(unittest.TestCase):
    def test_one_undirected(self):
        g = BinaryMixedTree(MixedGraph({0, 1, 2}, [(0, 1)]))
        g.add_directed(frozenset([1]), frozenset([2]))

        value_graph_2, value_map_2 = BasicTreeConstruction(g, s_0(g)).step(StratAlgo1())

        expected_graph = BinaryMixedTree(MixedGraph({2}))
        expected_graph.add(frozenset([0, 1]))
        expected_graph.add_undirected(frozenset([2]), frozenset([0, 1]))
        expected_map = {frozenset([0]): {frozenset([0])}, frozenset([1]): {frozenset([1])},
                        frozenset([2]): {frozenset([2])}, frozenset([0, 1]): {frozenset([0]), frozenset([1])}}

        self.assertEqual(value_graph_2, expected_graph)
        self.assertEqual(value_map_2, expected_map)

    def test_tree_sequence(self):
        g = BinaryMixedTree(MixedGraph({0, 1}, [(0, 1)]))

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
        value = BasicTreeConstruction(g, s_0(g)).tree_sequence(StratAlgo1())

        self.assertEqual(value, expected)


class TestAlgo3(unittest.TestCase):
    def test_hypergraph_1(self):
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

        maps = s_0(t)

        next_tree, next_map = BasicTreeConstruction(t, maps, h).step(StratAlgo3())

        self.assertEqual(
            {frozenset([1]): {frozenset([1])}, frozenset([2]): {frozenset([2])}, frozenset([3]): {frozenset([3])},
             frozenset([1, 3]): {frozenset([1]), frozenset([3])}}, next_map)
        expected_graph = BinaryMixedTree(MixedGraph({2}))
        expected_graph.add(frozenset([1, 3]))
        expected_graph.add_undirected(frozenset([2]), frozenset([1, 3]))

        self.assertEqual(expected_graph, next_tree)

    def test_hypergraph_2(self):
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

        t = BinaryMixedTree(MixedGraph({1, 2, 3, 4, 5, 6}, [(3, 6), (1, 5), (1, 3)]))
        t.add_directed(frozenset([1]), frozenset([2]))
        t.add_directed(frozenset([3]), frozenset([4]))

        next_tree, next_map = BasicTreeConstruction(t, s_0(t), g).step(StratAlgo3())

        self.assertEqual({frozenset([1]): {frozenset([1])},
                          frozenset([2]): {frozenset([2])},
                          frozenset([3]): {frozenset([3])},
                          frozenset([4]): {frozenset([4])},
                          frozenset([5]): {frozenset([5])},
                          frozenset([6]): {frozenset([6])},
                          frozenset([1, 3]): {frozenset([1]), frozenset([3])}
                          }, next_map)

        expected_tree = BinaryMixedTree(MixedGraph({2, 5, 3, 4, 6}, [(3, 6)]))
        expected_tree.add(frozenset([1, 3]))
        expected_tree.add_undirected(frozenset([1, 3]), frozenset([5]))
        expected_tree.add_undirected(frozenset([1, 3]), frozenset([2]))
        expected_tree.add_directed(frozenset([3]), frozenset([1, 3]))
        expected_tree.add_directed(frozenset([3]), frozenset([4]))

        self.assertEqual(expected_tree, next_tree)
