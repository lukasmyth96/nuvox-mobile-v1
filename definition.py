import os

REPO_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

NUVOX_WEBSITE_URL = 'http://nuvox-mobile-prod.eu-west-2.elasticbeanstalk.com/'

TRACE_ALGORITHM_DATASET_TRAIN_GDRIVE_ID = '1jvREy1rJzS-kSFMngFnX3Y1DLeWE6gHE'

TRACE_ALGORITHM_DATASET_TRAIN_PATH = os.path.join(REPO_ROOT_DIR, 'train.json')

TRACE_ALGORITHM_DATASET_TEST_GDRIVE_ID = '1mxETKmu9bH2cWNmQCspeN_xhft9voLJg'

TRACE_ALGORITHM_DATASET_TEST_PATH = os.path.join(REPO_ROOT_DIR, 'test.json')

TRACE_ALGORITHM_SUBMISSION_PATH = os.path.join(REPO_ROOT_DIR, 'submission.json')

LANGUAGE_MODEL_VOCAB_PATH = os.path.join(REPO_ROOT_DIR, 'nuvox_algorithm', 'language_model', 'cleaned_vocab.json')

KEYBOARD_IMAGE_PATH = os.path.join(REPO_ROOT_DIR, 'nuvox_app', 'keyboard', 'static', 'keyboard', 'assets', 'nuvox_keyboard_img.png')
