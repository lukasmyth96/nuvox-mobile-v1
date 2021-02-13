import numpy as np

from nuvox_algorithm.trace_algorithm.utils.load_dataset import load_train_set
from nuvox_algorithm.trace_algorithm import TraceAlgorithm
from nuvox_algorithm.trace_algorithm.scripts.evaluate_trace_algorithm import main_evaluate_trace_algorithm



if __name__ == '__main__':
    """
    This script evaluates your trace algorithm on a dataset of collected swipes stored in
    a JSON file. Once complete it will print the top-1 and top-3 accuracy of your algorithm.

    Notes
    ------
    - If your trace algorithm uses a machine learning model then you should edit this script
    so that you do not evaluate on swipes that were used during training.
    """
    # Load dataset of Swipes from data dump JSON file.
    _swipes = load_train_set()

    rdp_threshold_range = (0.001, 0.005, 0.01, 0.05, 0.1)
    angle_threshold_range = [np.pi * a for a in np.arange(0, 0.5, 0.01)]

    current_best_acc = 0
    current_best_combo = None
    for rdp_threshold in rdp_threshold_range:
        for angle_threshold in angle_threshold_range:

            _trace_algorithm = TraceAlgorithm(rdp_threshold=rdp_threshold, angle_threshold=angle_threshold)
            _top1_acc, _top3_acc = main_evaluate_trace_algorithm(_swipes, _trace_algorithm)

            if _top1_acc > current_best_acc:
                current_best_acc = _top1_acc
                current_best_combo = (rdp_threshold, angle_threshold)

            print(f'\n rdp: {rdp_threshold:.3f} - angle: {angle_threshold:.3f} -  accuracy: {_top1_acc:.2%} ')

    print(f'Overall best is rdp: {current_best_combo[0]} - angle: {current_best_combo[1]} - acc: {current_best_acc:.2%}')
