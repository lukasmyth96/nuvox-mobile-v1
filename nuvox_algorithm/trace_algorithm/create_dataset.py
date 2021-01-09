from typing import List

from nuvox_algorithm.core import Keyboard
from nuvox_algorithm.utils.io_funcs import read_json_file
from nuvox_algorithm.trace_algorithm.swipe import Swipe, TracePoint


def create_dataset(data_dump_file_path: str,
                   keyboard: Keyboard,
                   remove_inaccurate_swipes: bool) -> List[Swipe]:
    """Parses JSON file containing dump of Swipe table and
    returns a list of Swipe objects."""

    json_data = read_json_file(data_dump_file_path)
    swipes = []
    for swipe_dict in json_data:
        fields = swipe_dict['fields']
        swipe = Swipe(
            id=swipe_dict['pk'],
            user_id=fields['user'],
            trace=[TracePoint(**trace_point) for trace_point in fields['trace']],
            target_text=fields['target_text'],
            target_kis=keyboard.text_to_kis(text=fields['target_text'], skip_invalid_chars=True),
            trace_matches_text=fields['trace_matches_text']
        )

        swipes.append(swipe)

    if remove_inaccurate_swipes:
        swipes = [swipe for swipe in swipes if swipe.trace_matches_text]

    return swipes


if __name__ == '__main__':
    """Example Usage."""
    from nuvox_algorithm.core import nuvox_key_list
    _keyboard = Keyboard(keys=nuvox_key_list)
    _data_dump_file_path = '/swipes.json'
    dataset = create_dataset(
        data_dump_file_path=_data_dump_file_path,
        keyboard=_keyboard,
        remove_inaccurate_swipes=True
    )
    print('stop here')