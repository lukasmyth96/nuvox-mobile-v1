from typing import List

from tqdm import tqdm

from definition import TRACE_ALGORITHM_SUBMISSION_PATH, NUVOX_WEBSITE_URL
from nuvox_algorithm.core import Swipe
from nuvox_algorithm.utils.io_funcs import write_json_file
from nuvox_algorithm.trace_algorithm.utils import load_test_set
from nuvox_algorithm.trace_algorithm import TraceAlgorithm


def main_generate_competition_submission(swipes: List[Swipe],
                                         trace_algorithm: TraceAlgorithm,
                                         output_path: str) -> List[dict]:
    """Performs predictions on list of Swipes, saves predictions to
    JSON file and also returns them."""
    predictions = []
    for swipe in tqdm(swipes):

        kis_to_predicted_proba = trace_algorithm.predict_intended_kis(trace=swipe.trace)

        predictions.append(
            {
                "id": swipe.id,
                "prediction": kis_to_predicted_proba
            }
        )

    write_json_file(file_path=output_path, data=predictions)

    return predictions


if __name__ == '__main__':
    """
    This script uses your trace algorithm to perform predictions for the
    competition test set and saves them to a 'submission.json' file which
    you can then upload on the nuvox website.
    """
    # Load dataset of Swipes from data dump JSON file.
    _swipes = load_test_set()

    # Instantiate your TraceAlgorithm here.
    _trace_algorithm = TraceAlgorithm(rdp_threshold=0.01, angle_threshold=0.55)

    main_generate_competition_submission(
        swipes=_swipes,
        trace_algorithm=_trace_algorithm,
        output_path=TRACE_ALGORITHM_SUBMISSION_PATH
    )

    print(f'Submission file saved to {TRACE_ALGORITHM_SUBMISSION_PATH}')
    print(f'You can upload this submission file on the nuvox website to '
          f'enter the trace algorithm competition:\n {NUVOX_WEBSITE_URL}')
