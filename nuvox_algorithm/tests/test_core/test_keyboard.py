import re

import pytest

from nuvox_algorithm.core import Keyboard, Key


def test_keyboard_init(key_1: Key, key_2: Key):
    keyboard = Keyboard(keys=[key_1, key_2])
    assert keyboard.key_id_to_chars == {key_1.id: key_1.chars, key_2.id: key_2.chars}
    assert keyboard.char_to_key_id == {
        **{char: key_1.id for char in key_1.chars},
        **{char: key_2.id for char in key_2.chars}
    }


def test_keyboard_init_fails_if_overlapping_keys(key_1: Key):
    with pytest.raises(ValueError, match=re.escape('Keys: 1 and 1 overlap')):
        Keyboard(keys=[key_1, key_1])


def test_keyboard_key_at_point(key_1):
    keyboard = Keyboard(keys=[key_1])
    assert keyboard.key_at_point(x=0.1, y=0.1) == key_1
    assert keyboard.key_at_point(x=1, y=1) is None


@pytest.mark.parametrize(
    'text, expected_kis', [
        ('adg', '123'),
        ('gda', '321'),
        ('ag', '13'),
        ('abdegh', '123')
    ]
)
def test_keyboard_text_to_kis(key_1: Key,
                              key_2: Key,
                              key_3: Key,
                              text,
                              expected_kis):
    """Note for this text we set skip_invalid_chars=True."""
    keyboard = Keyboard(keys=[key_1, key_2, key_3])
    assert keyboard.text_to_kis(text) == expected_kis


def test_keyboard_text_to_kis_fails_if_invalid_character(key_1):
    keyboard = Keyboard(keys=[key_1])

    # Assert that KeyError is raised if text contains characters not on keyboard
    with pytest.raises(KeyError, match=r'Found no key containing char.*'):
        keyboard.text_to_kis(text='!some_of_these_characters_dont_exist_on_keyboard!')

    # Assert that exception is handled if 'skip_invalid_chars' is set to True.
    keyboard.text_to_kis(
        text='!some_of_these_characters_dont_exist_on_keyboard!',
        skip_invalid_chars=True
    )


@pytest.mark.parametrize(
    'trace, expected_kis', [
        (
            [
                {'x': 0.3, 'y': 0.1, 't': 0.1},
                {'x': 0.6, 'y': 0.1, 't': 0.2},
                {'x': 0.6, 'y': 0.1, 't': 0.2},
                {'x': 0.9, 'y': 0.1, 't': 0.3},
            ], '123'
        )
    ]
)
def test_keyboard_trace_to_kis(key_1: Key,
                               key_2: Key,
                               key_3: Key,
                               trace,
                               expected_kis):
    keyboard = Keyboard(keys=[key_1, key_2, key_3])

    assert keyboard.trace_to_kis(trace) == expected_kis
    # Assert that if trace is reversed then so is KIS.
    assert keyboard.trace_to_kis(trace[::-1]) == expected_kis[::-1]


def test_keyboard_trace_to_kis_fails_if_no_key_at_point(key_1):
    keyboard = Keyboard(keys=[key_1])

    invalid_trace = [{'x': 1.0, 'y': 1.0, 't': 0.1}]

    with pytest.raises(ValueError, match=re.escape('No key at point (1.0,1.0)')):
        assert keyboard.trace_to_kis(invalid_trace)
