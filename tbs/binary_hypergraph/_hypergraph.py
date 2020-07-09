from tbs.graph import Graph, connected_parts


class HyperGraph:
    """Class for hypergraph where an hyperedge is a subset of the vertices set.
    """

    def __init__(self, vertices=frozenset(), hyper_edges=frozenset()):
        self._vertices = frozenset()
        self._hyper_edges = frozenset()

        for x in vertices:
            self.add(x)

        for edge in hyper_edges:
            self.add_edge(edge)

    @property
    def vertices(self):
        """Vertex set."""

        return self._vertices

    @property
    def hyper_edges(self):
        return self._hyper_edges

    def add(self, x):
        """Add vertex *x*.

        Args:
            x(hashable): new vertex to add.
        Raises:
            ValueError: if *x* is already a vertex.
        """

        if x in self.vertices:
            raise ValueError("Already a vertex")

        self._vertices = self._vertices.union([x])

    def add_edge(self, edge):
        if edge in self.hyper_edges:
            raise ValueError("Already a hyperedge")
        self._hyper_edges = self._hyper_edges.union([edge])

    def remove(self, x):
        """Remove vertex *x*.

        Args:
            x: a vertex

        Raises:
            :exc:`ValueError` if *x* is not a vertex.
        """

        if x not in self.vertices:
            raise ValueError("Not a vertex")

        self._vertices = self._vertices.difference([x])

        for edge in self.hyper_edges:
            edge.difference({x})

    def difference(self, edges):
        """Remove edges.

        Each edge in *edges* is removed from the graph.

        Args:
            edges(iterable): Each edge is a pair `(x, y)` where *x* != *y* are vertices (in *vertices* or not).

        Returns:
            self (for possible chaining).
        """

        for x in edges:
            if not x.issubset(self.vertices):
                continue

            if x in self.hyper_edges:
                self.hyper_edges.difference(x)

        return self

    def __nonzero__(self):
        """False if no vertex."""

        if self._vertices:
            return True
        return False

    def __eq__(self, g):
        """Same vertices, same egdes and same attribute for each edge."""

        return self.vertices == g.vertices and self.hyper_edges == g.hyper_edges

    def __ne__(self, g):
        """not ==."""

        return not self == g

    def __contains__(self, vertex):
        """is a vertex"""

        return vertex in self.vertices

    def restriction(self, vertices_set):
        tb_graph_restrict_to_set = HyperGraph(vertices_set)

        for hyper_edge in self.hyper_edges:
            if frozenset(hyper_edge.intersection(vertices_set)) in tb_graph_restrict_to_set.hyper_edges:
                continue
            elif frozenset() == frozenset(hyper_edge.intersection(vertices_set)):
                continue
            else:
                tb_graph_restrict_to_set.add_edge(frozenset(hyper_edge.intersection(vertices_set)))

        return tb_graph_restrict_to_set

    def support_tree(self):
        v = self.vertices
        h_edges = list(self.hyper_edges)

        h_edges.sort(key=lambda x: len(x))
        support_tree = Graph()

        for x in v:
            support_tree.add(x)

        for h_edge in h_edges:
            kruskal = list(connected_parts(support_tree, vertex_subset=h_edge))
            if len(kruskal) == 1:
                continue
            else:
                for i in range(len(kruskal) - 1):
                    support_tree.update([(next(iter(kruskal[i])), next(iter(kruskal[i + 1])))],
                                        node_creation=False)

        return support_tree

    def hypergraph_restriction(self, vertices_set):
        tb_graph_restrict_to_set = HyperGraph(vertices=vertices_set)

        for hyper_edge in self.hyper_edges:
            tb_graph_restrict_to_set.add_edge(hyper_edge.intersection(vertices_set))

        return tb_graph_restrict_to_set
