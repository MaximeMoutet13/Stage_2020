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


def edges_in_homogeneous_subset(mixed_tree, A):
    undirected, directed = mixed_tree.edges
    out = []

    for x, y in undirected:
        if x in A:
            out.append(frozenset([x, y]))

    return out


def edge_choice_for_algo3(mixed_tree, maps, tb_hypergraph):
    homogeneous_set = mixed_tree.homogeneous_subset()
    edges_list = edges_in_homogeneous_subset(mixed_tree, homogeneous_set)

    sups = dict()
    for i, (x, y) in enumerate(edges_list):
        sup = supremum(maps[x], maps[y], tb_hypergraph)

        if sup not in sups.keys():
            sups[sup] = {i}
        else:
            sups[sup].add(i)

    m = minimum(list(sups.keys()))

    return edges_list[sups[m].pop()]


def neighborhood_support_tree_edges(mixed_tree, vertex, map_S, tb_hypergraph):
    A = set()
    delta_plus = mixed_tree(vertex, undirected=False, begin=True, end=False, closed=False)
    for t in delta_plus:
        A.update(map_S[t].difference(map_S[vertex]))

    neighborhood_support_tree = tb_hypergraph.restriction(A).support_tree()

    s = dict()
    for alpha in A:
        for u in delta_plus:
            if alpha in map_S[u]:
                s[alpha] = u
                continue

    e_delta = frozenset()
    for x, y in neighborhood_support_tree.edges:
        e_delta.union(frozenset([s[x], s[y]]))

    return e_delta


