import pytest

from nuvox_algorithm.utils.string_funcs import all_char_subsequences


@pytest.mark.parametrize(
    'input_string, expected_output_strings', [
        ('a', ['a']),
        ('ab', ['a', 'b', 'ab']),
        ('aba', ['a', 'b', 'a', 'ab', 'aa', 'ba', 'aba']),
        ('abc', ['a', 'b', 'c', 'ab', 'ac', 'bc', 'abc']),
    ]
)
def test_all_char_subsequences(input_string, expected_output_strings):
    assert all_char_subsequences(input_string) == expected_output_strings
