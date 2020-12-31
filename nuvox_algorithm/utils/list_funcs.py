from typing import Iterable, List, Any

import itertools


def sequential_pairs(iterable: Iterable):
    """Returns ordered pairs of adjacent items in iterable -
    i.e. s -> (s0, s1), (s1, s2)..."""
    i, j = itertools.tee(iterable)
    next(j, None)
    return zip(i, j)


def filter_adjacent_duplicates(a_list: List):
    return [i for i, j in sequential_pairs(a_list + [not a_list[-1]]) if i != j]


def all_subsequences(a_list: List) -> List[List[Any]]:
    """Returns all sub-sequences of a list.

    Examples
    --------
    - [1, 2, 1] --> [[1], [2], [1], [1, 2], [1, 1], [2, 1], [1, 2, 1]]
    """
    subsequences = []
    for subsequence_length in range(1, len(a_list) + 1):
        subsequences += [list(subsequence) for subsequence in (itertools.combinations(a_list, subsequence_length))]
    return subsequences
