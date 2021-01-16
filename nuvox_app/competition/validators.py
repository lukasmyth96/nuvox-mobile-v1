from typing import Dict

from django.core.exceptions import ValidationError
import numpy as np


def validate_submission_predictions(predictions: Dict[int, Dict[str, float]]):
    """Validates submission predictions to ensure that:
    1. 'predictions' is dict mapping swipe id (int) to a dict mapping KIS (str) to predicted probability (float).
    2. the sum of predicted probabilities for a given swipe is 1.0 (within floating point tolerance).
    3. Each KIS is a valid string containing characters 1-9 only, no spaces and no adjacent duplicates.
    """
    if not isinstance(predictions, dict):
        raise ValidationError('Predictions must be a dict.')

    for swipe_id, single_prediction_dict in predictions.items():

        if not isinstance(swipe_id, int):
            raise ValidationError(f'All keys of predictions dict must be an integer id of an individual swipe but found'
                                  f'key of type: {type(swipe_id)}.')

        if not isinstance(single_prediction_dict, dict):
            raise ValidationError(f'All values of predictions dict must be a dict but found value for swipe {swipe_id}'
                                  f'of type: {type(single_prediction_dict)}')

        sum_of_predicted_probs = sum([prob for prob in single_prediction_dict.values()])
        if not np.isclose(sum_of_predicted_probs, 1.0, atol=1e-5):
            raise ValidationError(f'Predicted probabilities for each key-id-sequence must sum to 1.0 '
                                  f'but summed to {sum_of_predicted_probs:.5f} for swipe with id: {swipe_id}')

        for kis, predicted_prob in single_prediction_dict.items():

            if not isinstance(kis, str):
                raise ValidationError(f'All keys for individual prediction dicts must be a key-id-sequence string but'
                                      f'found key for swipe: {swipe_id} of type: {type(kis)}.')

            if not all([char in [str(i) for i in range(10)] for char in list(kis)]):
                raise ValidationError(f'All keys for individual prediction dicts must be a key-id-sequence containing '
                                      f'characters from "1" - "9" but key: {kis} for swipe {swipe_id} contains invalid character.')

            if not isinstance(predicted_prob, float):
                raise ValidationError(f'All values for individual prediction dicts must be a float predicted probability'
                                      f'but found value for swipe: {swipe_id} of type: {type(predicted_prob)}.')
