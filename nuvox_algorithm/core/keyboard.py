from typing import List, Dict, Optional

from .key import Key


class Keyboard:

    def __init__(self, keys: List[Key]):
        self.keys = keys
        self.key_id_to_chars: Dict[str, List[str]] = {key.id: key.chars for key in keys}
        self.char_to_key_id: Dict[str, str] = {char: key.id for key in keys for char in key.chars}

    def text_to_key_id_sequence(self,
                                text: str,
                                skip_invalid_chars: Optional[bool] = False
                                ) -> str:
        """Returns list of key ids for the keys involved in swiping a given
        word.

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

            if (not key_id_sequence) or (key_id_sequence and key_id != key_id_sequence[-1]):
                key_id_sequence.append(key_id)

        key_id_sequence = ''.join(key_id_sequence)

        return key_id_sequence
