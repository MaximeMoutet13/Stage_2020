from tbs.binary_hypergraph import s_0, random_subset, directed_neighborhood_random_tree_edges, BinaryMixedTree, \
    edge_choice_for_algo1
from tbs.graph import UNDIRECTED_EDGE


def basic_tree_construction(mixed_tree, map_S):
    """ Algorithm 1: Returns a mixed tree T_i+1 and a map S_i+1 constructed from a mixed tree T_i and a map S_i.
    We assume here that the tree `self` is *consistent*.

    Args:
        mixed_tree (BinaryMixedTree): a consistent mixed tree
        map_S (dict): function r:X ->2^X where `X` is the set of vertices of the mixed tree `self`

    Returns:
        next_mixed_tree (BinaryMixedTree): the next mixed tree
        next_map (dict): its associated map

    Raises:
        ValueError: if the condition of line 2 can't be satisfied (which means the mixed tree isn't consistent)
    """
    next_mixed_tree = mixed_tree.copy()
    next_map = dict(map_S)

    x, y = edge_choice_for_algo1(next_mixed_tree)
    v_xy = next_mixed_tree.add_union(x, y)
    next_map[v_xy] = next_map[x].union(next_map[y])

    for z in {x, y}:
        delta_z = next_mixed_tree(z, undirected=True, begin=False, end=False, closed=False)

        delta_z_random_subset = random_subset(delta_z)

        next_mixed_tree.move_undirected_from_to(z, v_xy, delta_z_random_subset)

        if delta_z == delta_z_random_subset:
            random_delta_z_tree_edges = directed_neighborhood_random_tree_edges(next_mixed_tree, z)
            next_mixed_tree.update(UNDIRECTED_EDGE, random_delta_z_tree_edges, node_creation=False)
            next_mixed_tree.remove(z)

    return next_mixed_tree, next_map


def tree_sequence_construction(mixed_tree):
    """Algorithm 2: Create a sequence of mixed trees with associated maps.
    The hypergraph H = (V_0 , U_0≤i≤p {S_i(v): v ∈ V_i}) is a binary hypergraph
    where V_i is the set of vertices of the i^th mixed_tree and S_i its associated map

    Args:
        mixed_tree (BinaryMixedTree): a consistent tree (with no directed edges)

    Returns:
        seq (list): a sequence ((T_0, S_0), ..., (T_i, S_i)...) of mixed trees and there map
    """

    initial_map = s_0(mixed_tree)
    seq = [(mixed_tree, initial_map)]
    mixed_tree, map = mixed_tree, initial_map

    while len(mixed_tree) > 1:
        mixed_tree, map = basic_tree_construction(mixed_tree, map)
        seq.append((mixed_tree, map))

    return seq
