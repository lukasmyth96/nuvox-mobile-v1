from typing import Optional

from nuvox_algorithm.utils.list_funcs import sequential_pairs

# A dictionary mapping a corner-corner key ID pair
# to the ID of the key that is in the middle of
# those corner keys. For example '13': '2' means
# key 2 is between keys 1 and 3.
corner_corner_to_middle = {
    '13': '2',
    '31': '2',
    '17': '4',
    '71': '4',
    '39': '6',
    '93': '6',
    '79': '8',
    '97': '8'
}


def get_corner_to_corner_variants(kis, n: Optional[int] = 0):
    """This function is used to make up for the fact that by
    solely using turning points in the path to determine which
    keys were intended, you cannot know whether or not the user
    intended the middle key when the transition from one corner
    key to an opposite (non-diagonal) corner key. For example,
    if we detect turning points at key '1' followed by a straight
    line to key '3' - we cannot know whether the user also intended
    key '2' in the middle.

    This function takes a KIS (e.g. '13') and returns a list containing
    all variations of that KIS where for each corner-to-corner transition
    there is one variant that does and one that does not include the middle
    key between them.

    Notes
    --------
    - The function is called recursively.

    Examples
    ---------
    - '167' --> ['167'] - no variations because '167' contains no transitions
    from one corner to an opposite corner.
    - '13' --> ['13', '123'] - contains the two variations where middle key 2
    is/isn't present.
    """
    c = 0
    for idx, (k1, k2) in enumerate(sequential_pairs(kis)):
        middle_key = corner_corner_to_middle.get(f'{k1}{k2}')
        if middle_key is not None:
            if c == n:
                kis_with_middle_key = f'{kis[:idx + 1]}{middle_key}{kis[idx + 1:]}'
                return [*get_corner_to_corner_variants(kis, n + 1), *get_corner_to_corner_variants(kis_with_middle_key, n)]
            else:
                c += 1
    return [kis]
