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


def edge_choice_for_algo3(algo3):
    mixed_tree = algo3.mixed_tree
    maps = algo3.maps
    tb_hypergraph = algo3.tb_hypergraph

    homogeneous_set = mixed_tree.homogeneous_subset()
    edges_list = edges_in_homogeneous_subset(mixed_tree, homogeneous_set)

    sups = dict()
    for i, (x, y) in enumerate(edges_list):
        sup = supremum(maps[x], maps[y], tb_hypergraph.hyper_edges)

        if sup not in sups.keys():
            sups[sup] = {i}
        else:
            sups[sup].add(i)

    m = minimum(list(sups.keys()))

    return edges_list[sups[m].pop()]


def delta_z_subset_algo3(algo3, delta_z, v_xy, z):
    next_map = algo3.maps
    tb_hypergraph = algo3.tb_hypergraph

    delta_z_2 = set()
    for t in delta_z:
        if next_map[v_xy].issubset(supremum(next_map[z], next_map[t], tb_hypergraph.hyper_edges)):
            delta_z_2.add(t)

    return delta_z_2


def neighborhood_support_tree_edges(algo3, vertex):
    mixed_tree = algo3.mixed_tree
    map_S = algo3.maps
    tb_hypergraph = algo3.tb_hypergraph

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
        e_delta.union([frozenset([s[x], s[y]])])

    return e_delta
