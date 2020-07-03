from random import randint

from tbs.graph import random_tree


def s_0(mixed_tree):
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


def directed_neighborhood_random_tree(mixed_tree, vertex):
    delta_plus = mixed_tree(vertex, undirected=False, begin=True, end=False, closed=False)
    tree = random_tree(list(delta_plus))
    return tree
