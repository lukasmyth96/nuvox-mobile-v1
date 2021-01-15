import itertools
from typing import List, Dict, Optional

from nuvox_algorithm.utils.list_funcs import filter_adjacent_duplicates
from .key import Key


class Keyboard:

    def __init__(self, keys: List[Key]):
        """Class encapsulating the keyboard. Layout of keyboard is defined
        by passing a list of Key objects, each of which specifies its location
        and contents.

        Notes
        ------
        - See nuvox_algorithm/core/nuvox_keyboard contains an instance of this class
        that corresponds to the actual 9-key nuvox keyboard layout.
        """
        self.keys = keys
        self.key_id_to_chars: Dict[str, List[str]] = {key.id: key.chars for key in keys}
        self.char_to_key_id: Dict[str, str] = {char: key.id for key in keys for char in key.chars}
        self._check_for_overlapping_keys()

    def text_to_kis(self,
                    text: str,
                    skip_invalid_chars: Optional[bool] = False
                    ) -> str:
        """Returns key-id-sequence (KIS) for a given text.

        Notes
        --------
        - If skip_invalid_chars is True then characters not contained in
        the keyboard will be skipped, else a KeyError will be raised.

        Examples
        ---------
        - 'hello' --> '3246' (note that only one '4' appears for two l's.

        Raises
        ---------
        KeyError
            If no key exists for a given character.
        """
        key_id_sequence = []
        for char in list(text):
            char = char.lower()
            try:
                key_id = self.char_to_key_id[char]
            except KeyError:
                if skip_invalid_chars:
                    continue
                else:
                    raise KeyError(f'Found no key containing char: {char}. '
                                   f'Pass skip_invalid_chars=True to skip invalid chars.')

            key_id_sequence.append(key_id)

        key_id_sequence = filter_adjacent_duplicates(key_id_sequence)
        key_id_sequence = ''.join(key_id_sequence)

        return key_id_sequence

    def trace_to_kis(self, trace: List[Dict[str, float]]) -> str:
        """Returns key-id-sequence for a given trace.

        Examples
        --------
        [{'x': 0.15, 'y': 0.23, 't': 0.12}, ...] --> '3246'

        Raises
        --------
        ValueError
            If a no key exists for a point in the trace.
        """
        key_id_sequence = []
        for trace_point in trace:
            x, y = trace_point['x'], trace_point['y']
            key = self.key_at_point(x, y)
            if key is None:
                raise ValueError(f'No key at point ({x},{y})')
            key_id_sequence.append(key.id)

        key_id_sequence = filter_adjacent_duplicates(key_id_sequence)
        key_id_sequence = ''.join(key_id_sequence)

        return key_id_sequence

    def key_at_point(self, x: float, y: float):
        """Returns Key at a given x, y coordinate or None if no such key exists."""
        return next((key for key in self.keys if key.contains(x, y)), None)

    def _check_for_overlapping_keys(self):
        """Raises ValueError if any pair of keys overlap."""
        for key_a, key_b in itertools.combinations(self.keys, 2):
            if key_a.intersects(key_b):
                raise ValueError('Keys: {} and {} overlap'.format(key_a.id, key_b.id))
