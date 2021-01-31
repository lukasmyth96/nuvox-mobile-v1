from typing import List

from nuvox_algorithm.utils.list_funcs import all_subsequences


def all_char_subsequences(a_str: str) -> List[str]:
    """Returns all subsequences of characters in a string.

    Notes
    ------
    - This is not the same as all sub-strings because the
    returned list includes strings where the characters are
    not adjacent in the original string.
    - The only requirement on the subsequences of characters
    is that the characters are in the same order as they
    appear in the original string.

    Examples
    --------
    - 'aba' --> ['a', 'b', 'a', 'ab', 'aa', 'ba', 'aba']
    - 'abc' --> ['a', 'b', 'c', 'ab', 'ac', 'bc', 'abc']
    """
    return [''.join(char_subsequence) for char_subsequence in all_subsequences(list(a_str))]
