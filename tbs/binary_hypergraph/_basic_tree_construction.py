from tbs.binary_hypergraph import BinaryMixedTree, HyperGraph, UNDIRECTED_EDGE, s_0


class BasicTreeConstruction(object):
    def __init__(self, mixed_tree=BinaryMixedTree, maps=dict, tb_hypergraph=HyperGraph):
        self.mixed_tree = mixed_tree
        self.maps = maps
        self.tb_hypergraph = tb_hypergraph

    def step(self, strategy):
        edge_choice, delta_z_subset, neighborhood_tree = strategy()

        next_mixed_tree = self.mixed_tree.copy()
        next_map = dict(self.maps)

        x, y = edge_choice(self)
        v_xy = next_mixed_tree.add_union(x, y)
        next_map[v_xy] = next_map[x].union(next_map[y])

        next_algo3 = BasicTreeConstruction(next_mixed_tree, next_map, self.tb_hypergraph)

        for z in {x, y}:
            delta_z = next_mixed_tree(z, undirected=True, begin=False, end=False, closed=False)
            delta_z_random_subset = delta_z_subset(next_algo3, delta_z, v_xy, z)
            next_mixed_tree.move_undirected_from_to(z, v_xy, delta_z_random_subset)

            if delta_z == delta_z_random_subset:
                random_delta_z_tree_edges = neighborhood_tree(next_mixed_tree, z)
                next_mixed_tree.update(UNDIRECTED_EDGE, random_delta_z_tree_edges, node_creation=False)
                next_mixed_tree.remove(z)

        return next_mixed_tree, next_map

    def tree_sequence(self, strategy):
        current_tree = self.mixed_tree
        current_map = s_0(current_tree)

        self.maps = current_map

        seq = [(current_tree, current_map)]

        while len(current_tree) > 1:
            current_tree, current_map = self.step(strategy)
            seq.append((current_tree, current_map))

        return seq
