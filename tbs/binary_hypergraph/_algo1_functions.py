from random import randint

from tbs.graph import random_tree, MixedGraph


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


def supremum(map_x, map_y, tb_graph_edges):
    mark = True

    for edge in tb_graph_edges:
        if map_x.issubset(edge) and map_y.issubset(edge):
            if mark is True:
                sup = edge
                mark = False

            else:
                if edge.issubset(sup):
                    sup = edge

    return sup


def minimum(sets):
    minimum = sets[0]

    for x in sets[1:]:
        if x.issubset(minimum):
            minimum = x

    return minimum


def hypergraph_restriction(graph, vertices_set):
    tb_graph_restrict_to_set = set()

    for hyper_edge in graph:
        tb_graph_restrict_to_set.add(frozenset(hyper_edge.intersection(vertices_set)))

    return tb_graph_restrict_to_set


def support_tree(tb_graph):
    support_tree = BinaryMixedTree(MixedGraph())
    v = tb_graph.vertices
    h_edges = tb_graph.edges

    h_edges.sort(key=lambda x: len(x))

    for x in v:
        support_tree.add(x)

    for h_edge in h_edges:
        connected_parts = support_tree.kruskal()

        if h_edge in connected_parts:
            continue
        else:
            connected_parts.sort(key=lambda x: len(x.intersection(h_edge)))
            connected_vertices = connected_parts[0].intersection(h_edge)
            u = connected_vertices.pop()

            for vertex in h_edge.difference(connected_vertices):
                support_tree.add_undirected(vertex, u)

    return support_tree

if __name__ == '__main__':
    for i in range(1, 4):
        print(i)