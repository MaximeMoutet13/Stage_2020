from tbs.binary_hypergraph import BinaryMixedTree, HyperGraph, UNDIRECTED_EDGE, s_0, MixedGraph


class BasicTreeConstruction(object):
    """Class for the algorithms 1-4.
    """

    def __init__(self, mixed_tree=None, maps=None, tb_hypergraph=None):
        if mixed_tree is None:
            self.mixed_tree = BinaryMixedTree(MixedGraph())
        else:
            self.mixed_tree = mixed_tree

        if maps is None:
            self.maps = dict()
        else:
            self.maps = maps

        if tb_hypergraph is None:
            self.tb_hypergraph = HyperGraph()
        else:
            self.tb_hypergraph = tb_hypergraph

    def step(self, strategy):
        """ Returns a mixed tree T_i+1 and a map S_i+1 constructed from a mixed tree T_i and a map S_i.
                We assume here that the given tree `self.mixed_tree` is *consistent*. Depending on the given strategy,
                the algorithm 1 or 3 will be computed.

                Args:
                    strategy: a list of the functions needed, depending on which algorithm we want to execute (1 or 3)

                Returns:
                    next_mixed_tree (BinaryMixedTree): the next mixed tree
                    next_map (dict): its associated map

                Raises:
                    ValueError: if the condition of line 2 of algorithm 1 can't be satisfied (which means the mixed tree isn't consistent)
                """
        strategy.algo = self
        next_mixed_tree = self.mixed_tree.copy()
        next_map = dict(self.maps)

        x, y = strategy.edge_choice()
        v_xy = next_mixed_tree.add_union(x, y)
        next_map[v_xy] = next_map[x].union(next_map[y])

        next_algo3 = BasicTreeConstruction(next_mixed_tree, next_map, self.tb_hypergraph)
        strategy.algo = next_algo3

        for z in {x, y}:
            delta_z = next_mixed_tree(z, undirected=True, begin=False, end=False, closed=False)
            delta_z_random_subset = strategy.delta_z_subset(delta_z, v_xy, z)

            next_mixed_tree.move_undirected_from_to(z, v_xy, delta_z_random_subset)

            if delta_z == delta_z_random_subset:
                random_delta_z_tree_edges = strategy.neighborhood_tree(z)

                next_mixed_tree.update(UNDIRECTED_EDGE, random_delta_z_tree_edges, node_creation=False)
                next_mixed_tree.remove(z)

        return next_mixed_tree, next_map

    def tree_sequence(self, strategy):
        """Create a sequence of mixed trees with associated maps. Depending on the given strategy,
            the algorithm 2 or 4 will be computed. The given tree `self.mixed_tree` must be *consistent*
            and have only *undirected* edges.

            Args:
                strategy: a list of the functions needed, depending on which algorithm we want to execute (2 or 4)

            Returns:
                seq (list): a sequence ((T_0, S_0), ..., (T_i, S_i)...) of mixed trees and there maps
            """
        strategy.algo = self

        current_tree = self.mixed_tree
        current_map = s_0(current_tree)

        self.maps = current_map

        seq = [(current_tree, current_map)]

        while len(current_tree) > 1:
            current_tree, current_map = self.step(strategy)
            seq.append((current_tree, current_map))

        return seq
