import unittest

from tbs.binary_hypergraph._algo1_functions import s_0, random_subset
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
