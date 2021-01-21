import os
from typing import List, Optional

from definition import TRACE_ALGORITHM_DATASET_TRAIN_PATH, TRACE_ALGORITHM_DATASET_TEST_PATH
from nuvox_algorithm.core import nuvox_keyboard
from nuvox_algorithm.utils.io_funcs import read_json_file
from nuvox_algorithm.trace_algorithm.swipe import Swipe, TracePoint
from nuvox_algorithm.trace_algorithm.utils.download_dataset import (
    download_trace_algorithm_train_set,
    download_trace_algorithm_test_set
)


def load_train_set() -> List[Swipe]:
    if not os.path.exists(TRACE_ALGORITHM_DATASET_TRAIN_PATH):
        download_trace_algorithm_train_set()

    return _load_dataset(file_path=TRACE_ALGORITHM_DATASET_TRAIN_PATH)


def load_test_set() -> List[Swipe]:
    if not os.path.exists(TRACE_ALGORITHM_DATASET_TEST_PATH):
        download_trace_algorithm_test_set()

    return _load_dataset(file_path=TRACE_ALGORITHM_DATASET_TEST_PATH)


def _load_dataset(file_path: str) -> List[Swipe]:
    """Parses JSON file containing dataset of Swipes and returns
    list of convenient Swipe objects."""

    json_data = read_json_file(file_path)
    swipes = []
    for swipe_dict in json_data:
        fields = swipe_dict['fields']
        swipe = Swipe(
            id=swipe_dict['id'],
            user_id=fields['user_er'],
            device_type=fields['device_type'],
            trace=[TracePoint(**trace_point, key_id=nuvox_keyboard.key_at_point(trace_point['x'], trace_point['y']).id)
                   for trace_point in fields['trace']],
            target_text=fields['target_text'],
            target_kis=nuvox_keyboard.text_to_kis(text=fields['target_text'], skip_invalid_chars=True) if fields['target_text'] else None,
        )

        swipes.append(swipe)

    return swipes
