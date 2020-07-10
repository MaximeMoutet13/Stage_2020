import unittest

from tbs.binary_hypergraph import edge_choice_for_algo3, edges_in_homogeneous_subset, s_0
from tbs.binary_hypergraph import BinaryMixedTree, MixedGraph, HyperGraph, DIRECTED_EDGE

class TestAlgo3(unittest.TestCase):
    def test(self):
        g = HyperGraph(frozenset([frozenset([x]) for x in range(1, 6)]))
        g.add_edge(frozenset([frozenset([1]), frozenset([2])]))
        g.add_edge(frozenset([frozenset([2]), frozenset([3])]))
        g.add_edge(frozenset([frozenset([4]), frozenset([5])]))
        g.add_edge(frozenset([frozenset([2]), frozenset([3]), frozenset([4]), frozenset([5])]))
        g.add_edge(frozenset([frozenset([1]), frozenset([2]), frozenset([3]), frozenset([4]), frozenset([5])]))

        t = BinaryMixedTree(MixedGraph({0, 1, 2, 3, 4}, [(2, 4)]))
        t.add(frozenset([2, 3]))
        t.update(DIRECTED_EDGE, [(frozenset([2]), frozenset([0])), (frozenset([3]), frozenset([1])),
                                 (frozenset([2]), frozenset([2, 3])), (frozenset([3]), frozenset([2, 3]))],
                 node_creation=False)
        maps = s_0(t)

        # print(basic_tree_construction_algo3(t, maps, g))
