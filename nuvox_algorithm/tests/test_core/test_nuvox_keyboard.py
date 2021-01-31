import itertools
from string import ascii_lowercase

import numpy as np
import pytest

from nuvox_algorithm.core import nuvox_keyboard, Key

"""
This file contains tests for the 'nuvox_keyboard' object which is an
instance of the nuvox_algorithm.core.Keyboard class with the 9-key
nuvox keyboard layout. The tests here are only to ensure that the keyboard
is laid out as expected. See test_keyboard.py for unit tests of Keyboard.
"""


@pytest.mark.parametrize(
    'text, expected_kis', [
        ('hello', '3246'),
        ('world', '96742'),
        ('meet', '628'),
        ('nuvox', '6869'),

    ]
)
def test_nuvox_keyboard_text_to_kis(text: str, expected_kis: str):
    assert nuvox_keyboard.text_to_kis(text) == expected_kis


def test_nuvox_keys():
    """Test that keyboard contains 9 keys labelled 1-9 and
    that all letters of alphabet exist on keyboard."""
    assert len(nuvox_keyboard.keys) == 9
    assert {key.id for key in nuvox_keyboard.keys} == {str(i) for i in range(1, 10)}
    assert set(nuvox_keyboard.char_to_key_id) == set(ascii_lowercase)


def test_nuvox_keyboard_key_at_point():
    """Test that every point in the 1 * 1 grid corresponds
     to a key to ensure I haven't misplaced a key."""
    for x, y in itertools.product(np.arange(0, 1, 0.01), repeat=2):
        key = nuvox_keyboard.key_at_point(x, y)
        assert isinstance(key, Key)
        assert key in nuvox_keyboard.keys
