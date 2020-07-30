from random import randint

from tbs.graph import random_tree


def s_0(mixed_tree):
    """The map for the initial mixed tree, which is the identity function.

    Args:
        mixed_tree (BinaryMixedTree): a consistent mixed tree

    Returns:
        identity_func (dict)
    """
    identity_func = dict()

    for vertex in mixed_tree:
        identity_func[vertex] = {vertex}

    return identity_func


def random_subset(intial_set):
    subset = set()

    for element in intial_set:
        if randint(0, 1) == 1:
            subset.add(element)

    return subset


def edge_choice_for_algo1(algo3):
    mixed_tree = algo3.mixed_tree

    verify_line2 = []
    undirected, directed = mixed_tree.edges
    for edge in undirected:
        xy = list(edge)
        if mixed_tree(xy[0], undirected=False, begin=False, end=True) == frozenset() and mixed_tree(xy[1],
                                                                                                    undirected=False,
                                                                                                    begin=False,
                                                                                                    end=True) == frozenset():
            verify_line2.append(frozenset(xy))

    if len(verify_line2) == 0:
        raise ValueError("Non consistent mixed tree")
    else:
        k = randint(0, len(verify_line2) - 1)
        return verify_line2[k]


def directed_neighborhood_random_tree_edges(algo3, vertex):
    mixed_tree = algo3.mixed_tree
    delta_plus = mixed_tree(vertex, undirected=False, begin=True, end=False, closed=False)
    tree = random_tree(list(delta_plus))
    return tree.edges
