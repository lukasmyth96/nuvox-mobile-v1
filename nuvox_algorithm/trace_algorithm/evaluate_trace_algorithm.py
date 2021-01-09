from typing import Dict, List

import numpy as np

from nuvox_algorithm.core import Keyboard, nuvox_key_list
from nuvox_algorithm.trace_algorithm.create_dataset import create_dataset
from nuvox_algorithm.trace_algorithm.trace_algorithm import TraceAlgorithm


def ranked_key_id_sequences(kis_to_predicted_proba: Dict[str, float]) -> List[str]:
    """Returns list of KIS's ranked by predicted probability."""
    return [kis for kis, prob in sorted(kis_to_predicted_proba.items(), key=lambda item: item[1], reverse=True)]


if __name__ == '__main__':

    # Load Swipes from data dump JSON file.
    keyboard = Keyboard(keys=nuvox_key_list)
    swipes = create_dataset(
        data_dump_file_path='/home/luka/PycharmProjects/nuvox-mobile/nuvox_app/swipes.json',
        keyboard=keyboard,
        remove_inaccurate_swipes=True
    )

    # Instantiate your TraceAlgorithm
    trace_algorithm = TraceAlgorithm()

    # Metrics
    top1_acc_list = []  # list of bools indicating whether top prediction for each swipe was correct.
    top3_acc_list = []  # list of bools indicating whether true KIS was in top-3 predictions for each swipe.

    for swipe in swipes:

        kis_to_predicted_proba = trace_algorithm.predict_intended_kis(trace=swipe.trace)
        ranked_kis = ranked_key_id_sequences(kis_to_predicted_proba)
        top1_acc_list.append(swipe.target_kis == ranked_kis[0])
        top3_acc_list.append(swipe.target_kis in ranked_kis[:3])

    top1_acc = np.mean(top1_acc_list)
    top3_acc = np.mean(top3_acc_list)

    print(f'\nEvaluation Complete: top-1 accuracy: {top1_acc:.2%} - top-3 accuracy: {top3_acc:.2%}')
