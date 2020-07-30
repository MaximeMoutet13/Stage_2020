from ._algo1_functions import random_subset, edge_choice_for_algo1, directed_neighborhood_random_tree_edges
from ._basic_tree_construction import BasicTreeConstruction


class StratAlgo1(object):
    """Strategy for algorithm 1.
    This object is used as a strategy in ._basic_tree_construction.step to compute algorithm 1 and 2.
    """
    def __init__(self, algo=None):
        if algo is None:
            self.algo = BasicTreeConstruction()
        else:
            self.algo = algo

    def edge_choice(self):
        return edge_choice_for_algo1(self.algo)

    def delta_z_subset(self, delta_z, v_xy, z):
        return random_subset(delta_z)

    def neighborhood_tree(self, vertex):
        return directed_neighborhood_random_tree_edges(self.algo, vertex)
