from typing import List, Tuple

import numpy as np

from nuvox_algorithm.core import nuvox_keyboard
from nuvox_algorithm.trace_algorithm.scripts.evaluate_trace_algorithm import ranked_key_id_sequences
from keyboard.models import DataCollectionSwipe


def evaluate_submission(predictions: List[dict]) -> Tuple[float, float]:
    """Returns top1 and top3 accuracy for submission."""

    top1_acc_list = []  # list of bools indicating whether top prediction for each swipe was correct.
    top3_acc_list = []  # list of bools indicating whether true KIS was in top-3 predictions for each swipe.

    for prediction_dict in predictions:
        swipe_id = prediction_dict['id']
        kis_to_predicted_proba = prediction_dict['prediction']
        swipe = DataCollectionSwipe.objects.get(pk=swipe_id)  # TODO validate that id exists
        target_kis = nuvox_keyboard.text_to_kis(text=swipe.target_text, skip_invalid_chars=True)
        ranked_kis = ranked_key_id_sequences(kis_to_predicted_proba)
        top1_acc_list.append(target_kis == ranked_kis[0])
        top3_acc_list.append(target_kis in ranked_kis[:3])

    top1_acc = float(np.mean(top1_acc_list))
    top3_acc = float(np.mean(top3_acc_list))

    return top1_acc, top3_acc
