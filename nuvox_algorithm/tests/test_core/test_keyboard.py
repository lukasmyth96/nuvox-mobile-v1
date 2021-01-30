import copy

import pytest

from nuvox_algorithm.core import Keyboard, Key


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


def test_keyboard_init(key_1: Key):
    keyboard = Keyboard(keys=[key_1])
    assert keyboard.key_id_to_chars == {key_1.id: key_1.chars}
    assert keyboard.char_to_key_id == {char: key_1.id for char in key_1.chars}


def test_keyboard_init_fails_if_overlapping_keys(key_1: Key):
    key_2 = copy.deepcopy(key_1)
    with pytest.raises(ValueError):
        Keyboard(keys=[key_1, key_2])


def test_keyboard_key_at_point(key_1):
    keyboard = Keyboard(keys=[key_1])
    assert keyboard.key_at_point(x=0.25, y=0.25) == key_1
    assert keyboard.key_at_point(x=1, y=1) is None
