from tbs.binary_hypergraph._algo1_functions import edge_choice_for_algo1, delta_z_subset_algo1, directed_neighborhood_random_tree_edges
from tbs.binary_hypergraph._algo3_functions import edge_choice_for_algo3, delta_z_subset_algo3, neighborhood_support_tree_edges


def strategy_algo1():
    return edge_choice_for_algo1, delta_z_subset_algo1, directed_neighborhood_random_tree_edges


def strategy_algo3():
    return edge_choice_for_algo3, delta_z_subset_algo3, neighborhood_support_tree_edges
