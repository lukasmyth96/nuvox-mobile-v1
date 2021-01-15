import os
from typing import List, Optional

from definition import TRACE_ALGORITHM_DATASET_PATH
from nuvox_algorithm.core import Keyboard, nuvox_keys
from nuvox_algorithm.utils.io_funcs import read_json_file
from nuvox_algorithm.trace_algorithm.swipe import Swipe, TracePoint
from nuvox_algorithm.trace_algorithm.utils import download_trace_algorithm_dataset


def load_dataset(remove_inaccurate_swipes: Optional[bool] = True) -> List[Swipe]:
    """Parses JSON file containing dump of Swipe table and
    returns a list of Swipe objects."""
    keyboard = Keyboard(keys=nuvox_keys)

    if not os.path.exists(TRACE_ALGORITHM_DATASET_PATH):
        download_trace_algorithm_dataset()

    json_data = read_json_file(TRACE_ALGORITHM_DATASET_PATH)
    swipes = []
    for swipe_dict in json_data:
        fields = swipe_dict['fields']
        swipe = Swipe(
            id=swipe_dict['pk'],
            user_id=fields['user'],
            device_type=fields['device_type'],
            trace=[TracePoint(**trace_point) for trace_point in fields['trace']],
            target_text=fields['target_text'],
            target_kis=keyboard.text_to_kis(text=fields['target_text'], skip_invalid_chars=True),
            trace_matches_text=fields['trace_matches_text']
        )

        swipes.append(swipe)

    if remove_inaccurate_swipes:
        swipes = [swipe for swipe in swipes if swipe.trace_matches_text]

    return swipes
