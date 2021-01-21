from typing import List

from django.core.exceptions import ValidationError
import numpy as np

from nuvox_algorithm.trace_algorithm.utils import load_test_set
from keyboard.models import DataCollectionSwipe, DatasetSplit


def validate_submission_predictions(predictions: List[dict]):
    """Validates submission predictions to ensure that:
    1. predictions fits expected format:
        [
            {
                "id": 1,
                "prediction": {
                    "123": 0.8,
                    "13": 0.2
                }
            }
        ]
    2. Each "id" actually corresponds to a row in the DataCollectionSwipe table.
    3. Each "id" corresponds to a swipe that has "dataset_split=test"
    4. the sum of predicted probabilities for a given swipe is 1.0 (within floating point tolerance).
    5. Each KIS is a valid string containing characters 1-9 only, no spaces and no adjacent duplicates.
    6. The set of swipe "id"s matches the set in the local 'test.json' file. This ensure that people
    submit predictions on the full test set.
    """
    if not isinstance(predictions, list):
        raise ValidationError('Predictions must be a list.')

    swipe_ids_in_submission = []
    for swipe_prediction_dict in predictions:

        try:
            swipe_id = swipe_prediction_dict['id']
            prediction = swipe_prediction_dict['prediction']
        except KeyError as exc:
            raise ValidationError(f'Required field "{exc.args[0]}" missing from one or more predictions.')

        if not isinstance(swipe_id, int):
            raise ValidationError(f'Field "id" must contain integer but found {type(swipe_id).__name__}: {swipe_id}')

        swipe_ids_in_submission.append(swipe_id)

        try:
            swipe = DataCollectionSwipe.objects.get(pk=swipe_id)
            if not swipe.dataset_split == DatasetSplit.TEST:
                raise ValidationError(f'Swipe with id {swipe_id} does not belong to test set')
        except DataCollectionSwipe.DoesNotExist:
            raise ValidationError(f'No swipe exists in database with id: {swipe_id}')

        if not isinstance(prediction, dict):
            raise ValidationError(
                f'Field "prediction" must be a dictionary but found {type(prediction).__name__}: {prediction}')

        sum_of_predicted_probs = sum([prob for prob in prediction.values()])
        if not np.isclose(sum_of_predicted_probs, 1.0, atol=1e-5):
            raise ValidationError(f'Predicted probabilities for each key-id-sequence must sum to 1.0 '
                                  f'but summed to {sum_of_predicted_probs:.5f} for swipe with id: {swipe_id}')

        for kis, predicted_prob in prediction.items():

            if not isinstance(kis, str):
                raise ValidationError(f'All keys for individual prediction objects must be a key-id-sequence string but'
                                      f'found key: "{kis}" of type: "{type(kis).__name__}" for swipe with id: {swipe_id}.')

            if not all([char in [str(i) for i in range(10)] for char in list(kis)]):
                raise ValidationError(
                    f'All keys for individual prediction objects must be a key-id-sequence containing only '
                    f'characters "1" - "9" but found key: "{kis}" for swipe with id: {swipe_id}.')

            if not isinstance(predicted_prob, float):
                raise ValidationError(f'All values for individual prediction objects must be a predicted probability'
                                      f' of type float but found value: {predicted_prob} of type {type(predicted_prob).__name__}'
                                      f' for swipe with id: {swipe_id}.')

    expected_test_swipes = load_test_set()
    if not set(swipe_ids_in_submission) == {swipe.id for swipe in expected_test_swipes}:
        raise ValidationError('The set of swipe ids in your submission does not match the expected'
                              'set of swipe ids in the test set!')
