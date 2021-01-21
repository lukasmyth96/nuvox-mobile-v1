import requests

from definition import (
    TRACE_ALGORITHM_DATASET_TRAIN_GDRIVE_ID,
    TRACE_ALGORITHM_DATASET_TEST_GDRIVE_ID,
    TRACE_ALGORITHM_DATASET_TRAIN_PATH,
    TRACE_ALGORITHM_DATASET_TEST_PATH
)


def download_trace_algorithm_train_set():
    """Downloads trace algorithm dataset training set (JSON file).

    Notes
    - File will be git ignored by default - do NOT attempt to commit it.
    """
    print('Downloading competition train set...')
    _download_file_from_google_drive(
        gdrive_id=TRACE_ALGORITHM_DATASET_TRAIN_GDRIVE_ID,
        destination=TRACE_ALGORITHM_DATASET_TRAIN_PATH
    )


def download_trace_algorithm_test_set():
    """Downloads trace algorithm dataset training set (JSON file).

    Notes
    - File will be git ignored by default - do NOT attempt to commit it.
    """
    print('Downloading competition test set...')
    _download_file_from_google_drive(
        gdrive_id=TRACE_ALGORITHM_DATASET_TEST_GDRIVE_ID,
        destination=TRACE_ALGORITHM_DATASET_TEST_PATH
    )


def _download_file_from_google_drive(gdrive_id: str, destination: str):
    """Downloads publicly accessible file from Google Drive
    and saves contents to destination path."""

    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params={'id': gdrive_id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': gdrive_id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None


def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
