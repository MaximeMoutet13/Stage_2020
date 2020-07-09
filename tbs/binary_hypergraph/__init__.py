"""Stage Maxime Moutet

.. currentmodule:: tbs.stage_maxime

Based on the paper: C. Châtel, F. Brucker and P. Préa, Binary set systems and totally balanced hypergraphs

Module content
--------------

"""

from ._mixed_tree import BinaryMixedTree, MixedGraph, DIRECTED_EDGE, UNDIRECTED_EDGE
from ._hypergraph import HyperGraph
from ._algo1_functions import s_0, random_subset, directed_neighborhood_random_tree_edges, edge_choice_for_algo1
from ._algo3_functions import minimum, supremum, edge_choice_for_algo3, edges_in_homogeneous_subset
from ._basic_tree_construction_algo1 import basic_tree_construction, tree_sequence_construction
from ._basic_tree_construction_algo3 import basic_tree_construction_algo3

__author__ = "maxime"

__all__ = ['BinaryMixedTree', 'HyperGraph', 'MixedGraph']
