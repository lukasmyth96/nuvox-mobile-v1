import pytest

from nuvox_algorithm.utils.list_funcs import (
    sequential_pairs,
    filter_adjacent_duplicates,
    all_subsequences,
)


@pytest.mark.parametrize(
    'sequence, expected_pairs', [
        ([1, 2, 3], [(1, 2), (2, 3)])
    ]
)
def test_sequential_pairs(sequence, expected_pairs):
    assert sequential_pairs(sequence) == expected_pairs


@pytest.mark.parametrize(
    'input_list, expected_output_list', [
        ([1, 2, 3], [1, 2, 3]),
        ([1, 1, 2, 2, 2, 3, 3], [1, 2, 3])
    ]
)
def test_filter_adjacent_duplicates(input_list, expected_output_list):
    assert filter_adjacent_duplicates(input_list) == expected_output_list


@pytest.mark.parametrize(
    'input_list, expected_output_list', [
        ([1], [[1]]),
        ([1, 2], [[1], [2], [1, 2]]),
        ([1, 2, 1], [[1], [2], [1], [1, 2], [1, 1], [2, 1], [1, 2, 1]])
    ]
)
def test_all_subsequences(input_list, expected_output_list):
    assert all_subsequences(input_list) == expected_output_list
