from tbs.graph import Graph, connected_parts


class HyperGraph:
    """Class for hypergraphs where a hyperedge is a subset of the vertices set.
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
        """Add hyperedge *edge*.

        Args:
            edge(hashable): new hyperedge to add
        Raises:
            ValueError: if *edge* is already a hyperedge.
        """
        if edge in self.hyper_edges:
            raise ValueError("Already a hyperedge")
        self._hyper_edges = self._hyper_edges.union([edge])

    def __eq__(self, g):
        return self.vertices == g.vertices and self.hyper_edges == g.hyper_edges

    def __ne__(self, g):
        return not self == g

    def restriction(self, vertices_set):
        """Restrict a hypergraph to a given vertices set

        Args:
            vertices_set (frozenset)

        Returns:
            tb_graph_restrict_to_set (HyperGraph): the restricted hypergraph
        """
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
        """Construct the support tree of the hypergraph `self` (assume `self` is a *hypertree*)

        Returns (Graph): a graph which is a *support tree* of `self`
        """
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
