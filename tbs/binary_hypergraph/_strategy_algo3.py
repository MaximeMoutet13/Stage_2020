from ._algo3_functions import edge_choice_for_algo3, neighborhood_support_tree_edges, delta_z_subset_algo3
from ._basic_tree_construction import BasicTreeConstruction


class StratAlgo3(object):
    """Strategy for algorithm 3.
        This object is used as a strategy in ._basic_tree_construction.step to compute algorithm 3 and 4.
        """
    def __init__(self, algo=None):
        if algo is None:
            self.algo = BasicTreeConstruction()
        else:
            self.algo = algo

    def edge_choice(self):
        return edge_choice_for_algo3(self.algo)

    def delta_z_subset(self, delta_z, v_xy, z):
        return delta_z_subset_algo3(self.algo, delta_z, v_xy, z)

    def neighborhood_tree(self, vertex):
        return neighborhood_support_tree_edges(self.algo, vertex)
