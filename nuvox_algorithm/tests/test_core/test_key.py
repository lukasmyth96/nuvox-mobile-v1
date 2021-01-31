import copy
import re

import pytest

from nuvox_algorithm.core import Key


def test_key_init_fails_if_coordinates_invalid(key_1: Key):
    """Test that AssertionError is raised if any
    key coordinates are not in range (0, 1)."""
    valid_key_dict = key_1.__dict__
    for key in ('x0', 'y0', 'x1', 'y1'):
        for value in (-0.1, 1.1):
            invalid_key_dict = copy.deepcopy(valid_key_dict)
            invalid_key_dict.__setitem__(key, value)
            with pytest.raises(AssertionError, match=re.escape('Invalid key coordinates')):
                Key(**invalid_key_dict)


@pytest.mark.parametrize(
    'x, y, expected', [
        (0.1, 0.1, True),
        (-0.1, 0.1, False),
        (0.1, -0.1, False),
        (0.4, 0.1, False),
        (0.1, 0.4, False)
    ]
)
def test_key_contains(key_1: Key,
                      x: float,
                      y: float,
                      expected: bool):
    """Test that 'contains' method of Key
    returns True if key contains point else False."""
    assert key_1.contains(x, y) is expected


def test_key_intersects(key_1, key_2):
    """Test that 'intersects' method of Key
    returns True if key intersects another
    else False."""

    # Assert key_1 overlaps itself.
    assert key_1.intersects(key_1) is True

    # Assert keys 1 and 2 don't overlap.
    assert key_1.intersects(key_2) is False
    assert key_2.intersects(key_1) is False

    # Unless we move key 2 to left...
    key_2.x0 -= 0.1
    assert key_1.intersects(key_2) is True
