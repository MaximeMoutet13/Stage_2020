from tbs.binary_hypergraph import BinaryMixedTree, edge_choice_for_algo3, HyperGraph
from tbs.binary_hypergraph import minimum, supremum
from tbs.graph import UNDIRECTED_EDGE


def basic_tree_construction_algo3(consistent_mixed_tree, map_S, tb_hypergraph):
    """Compute the algorithm 3:

    Args:
        consistent_mixed_tree (BinaryMixedTree): a consistent mixed tree
        map_S (dict): the maps for the consistent mixed tree
        tb_hypergraph (HyperGraph): a totally balanced hypergraph
    """
    next_mixed_tree = consistent_mixed_tree.copy()
    next_map = dict(map_S)

    x, y = edge_choice_for_algo3(consistent_mixed_tree, next_map, tb_hypergraph)
    v_xy = next_mixed_tree.add_union(x, y)
    next_map[v_xy] = next_map[x].union(next_map[y])

    for z in {x, y}:
        delta_z = next_mixed_tree(z, undirected=True, begin=False, end=False, closed=False)

        delta_z_2 = set()
        for t in delta_z:
            if next_map[v_xy].issubset(supremum(map_S[z], map_S[t], tb_hypergraph.hyper_edges)):
                delta_z_2.add(t)

        next_mixed_tree.move_undirected_from_to(z, v_xy, delta_z_2)

        if delta_z_2 == delta_z:
            A = set()
            delta_plus = next_mixed_tree(z, undirected=False, begin=True, end=False, closed=False)
            for t in delta_plus:
                A.update(map_S[t].difference(map_S[z]))

            neighborhood_support_tree = tb_hypergraph.restriction(A).support_tree()
            next_mixed_tree.update(UNDIRECTED_EDGE, neighborhood_support_tree.edges[0], node_creation=False)
            next_mixed_tree.remove(z)

    return next_mixed_tree, next_map
