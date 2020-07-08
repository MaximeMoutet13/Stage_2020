import unittest

from tbs.binary_hypergraph._algo1_functions import s_0, random_subset, supremum, minimum
from tbs.binary_hypergraph._mixed_tree import BinaryMixedTree
from tbs.graph import MixedGraph, DIRECTED_EDGE, UNDIRECTED_EDGE


class TestSubset(unittest.TestCase):
    def test_empty_subset(self):
        s = set()
        s2 = random_subset(s)
        self.assertEqual(s2, set())

    def test_issubset(self):
        s = {1, 3, 5, 23, 547}
        s2 = random_subset(s)
        self.assertTrue(s2.issubset(s))

    def test_supremum_binary_little_hypergraph(self):
        s = frozenset(
            [frozenset([frozenset([0]), frozenset([1])]), frozenset([frozenset([1])]), frozenset([frozenset([0])
                                                                                                  ])])
        x, y = frozenset([0]), frozenset([1])

        value = supremum({x}, {y}, s)
        expected = {frozenset([0]), frozenset([1])}

        self.assertEqual(value, expected)

    def test_supremum(self):
        s = frozenset([
            frozenset([frozenset([0])]),
            frozenset([frozenset([1])]),
            frozenset([frozenset([2])]),
            frozenset([frozenset([3])]),
            frozenset([frozenset([0]), frozenset([1])]),
            frozenset([frozenset([2]), frozenset([3])]),
            frozenset([frozenset([0]), frozenset([1]), frozenset([3])]),
            frozenset([frozenset([0]), frozenset([1]), frozenset([2]), frozenset([3])])
        ])

        value = supremum({frozenset([0]), frozenset([1])}, {frozenset([3])}, s)
        expected = {frozenset([0]), frozenset([1]), frozenset([3])}

        self.assertEqual(value, expected)

    def test_minimum_empty(self):
        s = frozenset(
            [frozenset([frozenset([0]), frozenset([1])]), frozenset([frozenset([1])]), frozenset([frozenset([0])
                                                                                                  ])])
        sets = [frozenset([0]), frozenset([1])]

        value = minimum(sets, s)
        expected = set()

        self.assertEqual(value, expected)

    def test_minimum(self):
        s = frozenset([
            frozenset([frozenset([0])]),
            frozenset([frozenset([1])]),
            frozenset([frozenset([2])]),
            frozenset([frozenset([3])]),
            frozenset([frozenset([0]), frozenset([1])]),
            frozenset([frozenset([2]), frozenset([3])]),
            frozenset([frozenset([0]), frozenset([1]), frozenset([3])]),
            frozenset([frozenset([0]), frozenset([1]), frozenset([2]), frozenset([3])])
        ])

        sets = [frozenset([frozenset([0]), frozenset([1]), frozenset([2])]),
                frozenset([frozenset([2]), frozenset([3])])]

        value = minimum(sets, s)
        expected = frozenset([frozenset([2])])

        self.assertEqual(expected, value)
