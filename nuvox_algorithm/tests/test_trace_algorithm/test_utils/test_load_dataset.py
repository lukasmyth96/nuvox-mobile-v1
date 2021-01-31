from unittest import mock

import pytest

from nuvox_algorithm.utils.io_funcs import write_json_file
from nuvox_algorithm.trace_algorithm.utils.load_dataset import load_train_set, load_test_set


@pytest.fixture(scope='function')
def train_set_file_path(tmpdir, train_swipe_dict):
    file_path = str(tmpdir / 'train.json')
    write_json_file(file_path, [train_swipe_dict])
    return file_path


@pytest.fixture(scope='function')
def test_set_file_path(tmpdir, test_swipe_dict):
    file_path = str(tmpdir / 'test.json')
    write_json_file(file_path, [test_swipe_dict])
    return file_path


def test_load_train_set(train_set_file_path):

    with mock.patch('nuvox_algorithm.trace_algorithm.utils.load_dataset.TRACE_ALGORITHM_DATASET_TRAIN_PATH', train_set_file_path):
        swipes = load_train_set()
        assert len(swipes) == 1
        swipe = swipes[0]
        assert swipe.id == 1
        assert swipe.user_id == 1
        assert swipe.device_type == 'pc'
        assert swipe.target_text == 'hello'
        assert swipe.target_kis == '3246'
        assert len(swipe.trace) == 1
        trace_point = swipe.trace[0]
        assert trace_point.t == 0.1
        assert trace_point.x == 0.2
        assert trace_point.y == 0.3


def test_load_train_set_with_force_download_true(train_set_file_path):
    mock_download_trace_algorithm_train_set = mock.Mock()
    with mock.patch('nuvox_algorithm.trace_algorithm.utils.load_dataset.TRACE_ALGORITHM_DATASET_TRAIN_PATH',train_set_file_path),\
         mock.patch('nuvox_algorithm.trace_algorithm.utils.load_dataset.download_trace_algorithm_train_set', mock_download_trace_algorithm_train_set):
        swipes = load_train_set(force_download=True)
        mock_download_trace_algorithm_train_set.assert_called_once()


def test_load_test_set(test_set_file_path):

    with mock.patch('nuvox_algorithm.trace_algorithm.utils.load_dataset.TRACE_ALGORITHM_DATASET_TEST_PATH', test_set_file_path):
        swipes = load_test_set()
        assert len(swipes) == 1
        swipe = swipes[0]
        assert swipe.id == 1
        assert swipe.user_id == 1
        assert swipe.device_type == 'pc'
        assert swipe.target_text is None
        assert swipe.target_kis is None
        assert len(swipe.trace) == 1
        trace_point = swipe.trace[0]
        assert trace_point.t == 0.1
        assert trace_point.x == 0.2
        assert trace_point.y == 0.3


def test_load_test_set_with_force_download_true(test_set_file_path):
    mock_download_trace_algorithm_test_set = mock.Mock()
    with mock.patch('nuvox_algorithm.trace_algorithm.utils.load_dataset.TRACE_ALGORITHM_DATASET_TEST_PATH',test_set_file_path),\
         mock.patch('nuvox_algorithm.trace_algorithm.utils.load_dataset.download_trace_algorithm_test_set', mock_download_trace_algorithm_test_set):
        swipes = load_test_set(force_download=True)
        mock_download_trace_algorithm_test_set.assert_called_once()
