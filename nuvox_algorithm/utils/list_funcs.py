from typing import Iterable, List, Any, Tuple

import itertools


def sequential_pairs(iterable: Iterable) -> List[Tuple[Any, Any]]:
    """Returns ordered pairs of adjacent items in iterable -
    i.e. s -> (s0, s1), (s1, s2)..."""
    i, j = itertools.tee(iterable)
    next(j, None)
    return list(zip(i, j))


def filter_adjacent_duplicates(a_list: list) -> list:
    if a_list:
        return [i for i, j in sequential_pairs(a_list + [not a_list[-1]]) if i != j]
    else:
        return a_list


def filter_duplicates(a_list: list) -> list:
    """Filters duplicates whilst preserving order."""
    filtered_list = []
    for item in a_list:
        if item not in filtered_list:
            filtered_list.append(item)
    return filtered_list


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
