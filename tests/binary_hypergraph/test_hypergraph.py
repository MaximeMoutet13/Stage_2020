import unittest

from tbs.binary_hypergraph import HyperGraph

class TestHyperGraph(unittest.TestCase):
    def test_add(self):
        h = HyperGraph()
        for i in range(5):
            h.add(frozenset([i]))
        for i in range(1, 4):
            edge = frozenset([frozenset([i]), frozenset([i + 1])])
            h.add_edge(edge)

        self.assertEqual(h, HyperGraph({
            frozenset([1]), frozenset([2]), frozenset([3]), frozenset([4]), frozenset([5])
        }, frozenset([
            frozenset([frozenset([1]), frozenset([2])]),
            frozenset([frozenset([2]), frozenset([3])]),
            frozenset([frozenset([3]), frozenset([4])]),
            frozenset([frozenset([4]), frozenset([5])])
        ])))
