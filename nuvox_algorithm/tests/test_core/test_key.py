import copy

import pytest

from nuvox_algorithm.core import Key


@pytest.fixture(scope='function')
def key_1() -> Key:
    return Key(
        id='1',
        chars=['a', 'b', 'c'],
        x0=0.0,
        y0=0.0,
        x1=0.5,
        y1=0.5
    )


def test_key_init_fails_if_coordinates_invalid(key_1: Key):
    """Test that AssertionError is raised if any
    key coordinates are not in range (0, 1)."""
    valid_key_dict = key_1.__dict__
    for key in ('x0', 'y0', 'x1', 'y1'):
        for value in (-0.1, 1.1):
            invalid_key_dict = copy.deepcopy(valid_key_dict)
            invalid_key_dict.__setitem__(key, value)
            with pytest.raises(AssertionError):
                Key(**invalid_key_dict)


@pytest.mark.parametrize(
    'x, y, expected', [
        (0.25, 0.25, True),
        (-0.25, 0.25, False),
        (0.25, -0.25, False),
        (0.75, 0.25, False),
        (0.25, 0.75, False)
    ]
)
def test_key_contains(key_1: Key,
                      x: float,
                      y: float,
                      expected: bool):
    """Test that 'contains' method of Key
    returns True if key contains point else False."""
    assert key_1.contains(x, y) is expected


def test_key_intersects(key_1):
    """Test that 'intersects' method of Key
    returns True if key intersects another
    else False."""

    # Two keys that overlap in x and y.
    key_2 = copy.deepcopy(key_1)
    assert key_1.intersects(key_2) is True
    assert key_2.intersects(key_1) is True

    # Two keys that overlap in y but not x.
    key_3 = copy.deepcopy(key_1)
    key_3.x0, key_3.x1 = 0.5, 1.0
    assert key_1.intersects(key_3) is False
    assert key_3.intersects(key_1) is False

    # Two keys that overlap in x but not y.
    key_4 = copy.deepcopy(key_1)
    key_4.y0, key_4.y1 = 0.5, 1.0
    assert key_1.intersects(key_4) is False
    assert key_4.intersects(key_1) is False
