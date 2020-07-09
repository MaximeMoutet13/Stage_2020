__author__ = 'cchatel', 'fbrucker', 'mmoutet'


from tbs.graph import MixedGraph, UNDIRECTED_EDGE, DIRECTED_EDGE, Graph, connected_parts


class BinaryMixedTree(MixedGraph):
    """Class for mixed trees (trees with directed and undirected edges).
    """
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

    def restriction(self, vertices_set):
        if not vertices_set.issubset(self.vertices):
            raise ValueError("Can't restrict the tree to a set which isn't included in the vertices set")

        restricted_tree = BinaryMixedTree(MixedGraph())
        for x in vertices_set:
            restricted_tree.add(x)

        undirected, directed = self.edges

        for x, y in undirected:
            if x in vertices_set and y in vertices_set:
                restricted_tree.add_undirected(x, y)

        for x, y in directed:
            if x in vertices_set and y in vertices_set:
                restricted_tree.add_directed(x, y)

        return restricted_tree

    def underlying_undirected_graph(self):
        undirected, directed = self.edges
        self.update(UNDIRECTED_EDGE, directed, node_creation=False)
        g = Graph.from_graph(self)
        return g

    def homogeneous_subset(self, first_iter=True):
        if first_iter:
            h = self.copy()
        else:
            h = self

        undirected, directed = h.edges

        if len(directed) == 0:
            return h.vertices

        else:
            xy = next(iter(directed))
            x, y = xy
            h.difference([xy])
            connected_1, connected_2 = connected_parts(h.underlying_undirected_graph())

            if connected_1.intersection([y]) != frozenset():
                for v in connected_1:
                    h.remove(v)
            else:
                for v in connected_2:
                    h.remove(v)

            return h.homogeneous_subset(first_iter=False)
