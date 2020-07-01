import numpy as np

import line_profiler

from tbs.stage_maxime import BinaryMixedTree, s_0
from tbs.graph import MixedGraph

func_test = BinaryMixedTree.basic_tree_construction


class BasicTreeConstruction:
    def __init__(self, mixed_tree, map):
        self.g = mixed_tree
        self.s = map

    def algo1(self):
        g = self.g
        s = self.s
        t = func_test(g, s)


def main(params, n_runs=4):
    for i in range(n_runs):
        print('Run', i)
        n = np.random.randint(0, n_runs - 1)
        res = BasicTreeConstruction(params[n][0], params[n][1])
        res.algo1()


if __name__ == '__main__':
    tree_1 = BinaryMixedTree(MixedGraph({0, 1, 2}, [(0, 1), (1, 2)]))

    tree_2 = BinaryMixedTree(MixedGraph({0, 1, 2, 3}, [(0, 2)]))
    tree_2.add_directed(frozenset([0]), frozenset([1]))
    tree_2.add_directed(frozenset([2]), frozenset([3]))

    tree_3 = BinaryMixedTree(MixedGraph({0, 1, 2, 3, 4, 5}, [(2, 3), (2, 1), (5, 4)]))
    tree_3.add_directed(frozenset([2]), frozenset([1]))
    tree_3.add_directed(frozenset([2]), frozenset([5]))

    tree_4 = BinaryMixedTree(
        MixedGraph({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10},
                   [(0, 1), (0, 4), (0, 5), (2, 9), (9, 10), (5, 9), (5, 8), (8, 7), (6, 7), (3, 7)]))

    my_params = [(tree_1, s_0(tree_1)), (tree_2, s_0(tree_2)), (tree_3, s_0(tree_3)), (tree_4, s_0(tree_4))]

    lp = line_profiler.LineProfiler()
    lp.add_function(func_test)
    lp_wrapper = lp(main)
    lp_wrapper(my_params)

    lp.print_stats(output_unit=1e-3)

    stats_file = 'profile_generation.lprof'
    lp.dump_stats(stats_file)
    print('Run the following command to display the results:')
    print('$ python -m line_profiler {}'.format(stats_file))
