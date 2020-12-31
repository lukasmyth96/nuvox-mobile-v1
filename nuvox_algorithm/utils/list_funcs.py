from typing import Iterable, List

from itertools import tee


def sequential_pairs(iterable: Iterable):
    """Returns ordered pairs of adjacent items in iterable -
    i.e. s -> (s0, s1), (s1, s2)..."""
    i, j = tee(iterable)
    next(j, None)
    return zip(i, j)


def filter_adjacent_duplicates(a_list: List):
    return [i for i, j in sequential_pairs(a_list + [not a_list[-1]]) if i != j]
