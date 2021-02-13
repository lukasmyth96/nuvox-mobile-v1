import os
from typing import List, Optional

from definition import TRACE_ALGORITHM_DATASET_TRAIN_PATH, TRACE_ALGORITHM_DATASET_TEST_PATH
from nuvox_algorithm.core import nuvox_keyboard, Swipe, TracePoint
from nuvox_algorithm.utils.io_funcs import read_json_file
from nuvox_algorithm.trace_algorithm.utils.download_dataset import (
    download_trace_algorithm_train_set,
    download_trace_algorithm_test_set
)


def load_train_set(force_download: Optional[bool] = False) -> List[Swipe]:
    """Loads competition training set from local JSON file
    and returns list of convenient Swipe objects.

    Notes
    ------
    - Data will be downloaded from GDrive if not already downloaded or
    if 'force_download' is True.
    """
    if force_download or not os.path.exists(TRACE_ALGORITHM_DATASET_TRAIN_PATH):
        download_trace_algorithm_train_set()

    return _load_dataset(file_path=TRACE_ALGORITHM_DATASET_TRAIN_PATH)


def load_test_set(force_download: Optional[bool] = False) -> List[Swipe]:
    """Loads competition test set from local JSON file
    and returns list of convenient Swipe objects.

    Notes
    ------
    - Data will be downloaded from GDrive if not already downloaded or
    if 'force_download' is True.
    - 'target_text' field of will be 'None' for all test set items.
    """
    if force_download or not os.path.exists(TRACE_ALGORITHM_DATASET_TEST_PATH):
        download_trace_algorithm_test_set()

    return _load_dataset(file_path=TRACE_ALGORITHM_DATASET_TEST_PATH)


def _load_dataset(file_path: str) -> List[Swipe]:
    """Parses JSON file containing dataset of Swipes and returns
    list of convenient Swipe objects."""

    json_data = read_json_file(file_path)
    swipes = []
    for swipe_dict in json_data:
        swipe = Swipe(
            id=swipe_dict['id'],
            user_id=swipe_dict['user_id'],
            device_type=swipe_dict['device_type'],
            trace=[TracePoint(**trace_point, key_id=nuvox_keyboard.key_at_point(trace_point['x'], trace_point['y']).id)
                   for trace_point in swipe_dict['trace']],
            target_text=swipe_dict['target_text'],
            target_kis=nuvox_keyboard.text_to_kis(text=swipe_dict['target_text'], skip_invalid_chars=True)
            if swipe_dict['target_text'] else None,
        )

        swipes.append(swipe)

    return swipes
