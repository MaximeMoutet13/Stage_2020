"""Stage Maxime Moutet

.. currentmodule:: tbs.stage_maxime

Based on the paper: C. Châtel, F. Brucker and P. Préa, Binary set systems and totally balanced hypergraphs
This module needs the module graph.

Module content
--------------

"""

from ._mixed_tree import BinaryMixedTree, MixedGraph, DIRECTED_EDGE, UNDIRECTED_EDGE
from ._hypergraph import HyperGraph
from ._algo1_functions import s_0
from ._strategies import strategy_algo1, strategy_algo3
from ._basic_tree_construction import BasicTreeConstruction

__author__ = "maxime"

__all__ = ['BinaryMixedTree', 'HyperGraph', 'BasicTreeConstruction',
           'MixedGraph', 'UNDIRECTED_EDGE', 'DIRECTED_EDGE',
           's_0', 'strategy_algo1', 'strategy_algo3']
