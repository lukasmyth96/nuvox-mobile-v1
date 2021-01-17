from typing import List

from django.core.exceptions import ValidationError
import numpy as np


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
    2. the sum of predicted probabilities for a given swipe is 1.0 (within floating point tolerance).
    3. Each KIS is a valid string containing characters 1-9 only, no spaces and no adjacent duplicates.
    """
    if not isinstance(predictions, list):
        raise ValidationError('Predictions must be a list.')

    for swipe_prediction_dict in predictions:

        try:
            swipe_id = swipe_prediction_dict['id']
            prediction = swipe_prediction_dict['prediction']
        except KeyError as exc:
            raise ValidationError(f'Required field "{exc.args[0]}" missing from one or more predictions.')

        if not isinstance(swipe_id, int):
            raise ValidationError(f'Field "id" must contain integer but found {type(swipe_id).__name__}: {swipe_id}')

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
