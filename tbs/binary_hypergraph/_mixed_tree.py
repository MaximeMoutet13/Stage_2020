__author__ = 'cchatel', 'fbrucker', 'mmoutet'

import random

from tbs.graph import MixedGraph, UNDIRECTED_EDGE, DIRECTED_EDGE
from tbs.graph import Graph
from tbs.binary_hypergraph._algo1_functions import s_0, random_subset, directed_neighborhood_random_tree


class BinaryMixedTree(MixedGraph):
    def __init__(self, tree):
        super().__init__()
        for vertex in tree:
            self.add(frozenset({vertex}))
        for vertex in tree:
            for neighbour in tree(vertex):
                self.update(UNDIRECTED_EDGE, [(frozenset({vertex}), frozenset({neighbour}))])

    def copy(self):
        copy = BinaryMixedTree({})
        for vertex in self.vertices:
            copy.add(vertex)

        undirected, directed = self.edges
        copy.update(UNDIRECTED_EDGE, undirected)
        copy.update(DIRECTED_EDGE, directed)
        return copy

    def add_undirected(self, x, y):
        self.update(UNDIRECTED_EDGE, [(x, y)])

    def add_directed(self, x, y):
        self.update(DIRECTED_EDGE, [(x, y)])

    def add_union(self, x, y):
        xy = x.union(y)

        self.difference([(x, y)])
        self.add(xy)

        self.update(DIRECTED_EDGE, [(x, xy), (y, xy)])

        return xy

    def move_undirected_from_to(self, x, y, edges=None):
        if edges is None:
            edges = set(self(x, undirected=True, begin=False, end=False))

        for z in edges:
            self.difference([(x, z)])
            self.update(UNDIRECTED_EDGE, [(y, z)])

    def edge_choice(self):
        verify_line2 = []
        undirected, directed = self.edges
        for edge in undirected:
            xy = list(edge)
            if self(xy[0], undirected=False, begin=False, end=True) == frozenset() and self(xy[1],
                                                                                            undirected=False,
                                                                                            begin=False,
                                                                                            end=True) == frozenset():
                verify_line2.append(frozenset(xy))

        if len(verify_line2) == 0:
            raise ValueError("Non consistent mixed tree")
        else:
            k = random.randint(0, len(verify_line2) - 1)
            return verify_line2[k]

    def basic_tree_construction(self, map):
        """ Algorithm 1: Returns a mixed tree T_i+1 and a map S_i+1 constructed from a mixed tree T_i and a map S_i.
        We assume here that the tree `self` is *consistent*.

        Args:
            map (dict): function r:X ->2^X where `X` is the set of vertices of the mixed tree `self`

        Returns:
            next_mixed_tree (BinaryMixedTree): the next mixed tree
            next_map (dict): its associated map

        Raises:
            ValueError: if the condition of line 2 can't be satisfied (which means the mixed tree isn't consistent)
        """
        next_mixed_tree = self.copy()
        next_map = dict(map)

        x, y = next_mixed_tree.edge_choice()
        v_xy = next_mixed_tree.add_union(x, y)
        next_map[v_xy] = next_map[x].union(next_map[y])

        for z in {x, y}:
            delta_z = next_mixed_tree(z, undirected=True, begin=False, end=False, closed=False)
            delta_z_random_subset = random_subset(delta_z)
            next_mixed_tree.move_undirected_from_to(z, v_xy, delta_z_random_subset)

            if delta_z == delta_z_random_subset:
                random_delta_z_tree = directed_neighborhood_random_tree(next_mixed_tree, z)
                next_mixed_tree.update(UNDIRECTED_EDGE, random_delta_z_tree.edges, node_creation=False)
                next_mixed_tree.remove(z)

        return next_mixed_tree, next_map

    def tree_sequence_construction(self):
        """Algorithm 2: Create a sequence of mixed trees with associated maps.
        The hypergraph H = (V_0 , U_0≤i≤p {S_i(v): v ∈ V_i}) is a binary hypergraph
        where V_i is the set of vertices of the i^th mixed_tree and S_i its associated map

        Returns:
            seq (list): a sequence ((T_0, S_0), ..., (T_i, S_i)...) of mixed trees and there map
        """
        initial_map = s_0(self)
        seq = [(self, initial_map)]
        mixed_tree, map = self, initial_map

        while len(mixed_tree) > 1:
            mixed_tree, map = mixed_tree.basic_tree_construction(map)
            seq.append((mixed_tree, map))

        return seq
