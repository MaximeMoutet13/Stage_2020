import unittest

from tbs.binary_hypergraph import HyperGraph
from tbs.graph import MixedGraph, connected_parts


class TestHyperGraph(unittest.TestCase):
    def test_add_vertices_edges(self):
        h = HyperGraph()
        for i in range(1, 5):
            h.add(frozenset([i]))
        for i in range(1, 4):
            edge = frozenset([frozenset([i]), frozenset([i + 1])])
            h.add_edge(edge)

        self.assertEqual(h.vertices, frozenset([
            frozenset([1]), frozenset([2]), frozenset([3]), frozenset([4])]))
        self.assertEqual(h.hyper_edges, frozenset([
            frozenset([frozenset([1]), frozenset([2])]),
            frozenset([frozenset([2]), frozenset([3])]),
            frozenset([frozenset([3]), frozenset([4])])
        ]))

    def test_restriction(self):
        h = HyperGraph(frozenset([1, 2, 3, 4, 5]))
        h.add_edge(frozenset(
            frozenset([frozenset([1]), frozenset([2])])))
        h.add_edge(
            frozenset([frozenset([2]), frozenset([3])]))
        h.add_edge(
            frozenset([frozenset([3]), frozenset([4])]))

        restrict_set = frozenset([frozenset([1]), frozenset([2]), frozenset([5])])

        restricted_graph = h.restriction(restrict_set)

        self.assertEqual(restricted_graph.vertices, restrict_set)
        self.assertEqual(restricted_graph.hyper_edges, frozenset([
            frozenset([frozenset([1]), frozenset([2])]),
            frozenset([frozenset([2])])
        ]))

    def test_support_tree_2_vertices_graph(self):
        g = HyperGraph(frozenset([frozenset([1]), frozenset([2])]),
                       frozenset([frozenset([frozenset([1]), frozenset([2])])]))

        self.assertEqual(g.support_tree(),
                         MixedGraph({frozenset([1]), frozenset([2])}, [(frozenset([1]), frozenset([2]))]))

    def test_support_tree(self):
        g = HyperGraph(frozenset([frozenset([x]) for x in range(1, 6)]))
        g.add_edge(frozenset([frozenset([1]), frozenset([2])]))
        g.add_edge(frozenset([frozenset([2]), frozenset([3])]))
        g.add_edge(frozenset([frozenset([4]), frozenset([5])]))
        g.add_edge(frozenset([frozenset([2]), frozenset([3]), frozenset([4]), frozenset([5])]))
        g.add_edge(frozenset([frozenset([1]), frozenset([2]), frozenset([3]), frozenset([4]), frozenset([5])]))

        supp_tree = g.support_tree()

        for x in g.hyper_edges:
            self.assertTrue(len(connected_parts(supp_tree, vertex_subset=x)) == 1)

    def test_support_tree_2(self):
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

        supp_tree = g.support_tree()

        for x in g.hyper_edges:
            self.assertTrue(len(connected_parts(supp_tree, vertex_subset=x)) == 1)
