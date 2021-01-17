from tqdm import tqdm

from definition import TRACE_ALGORITHM_SUBMISSION_PATH
from nuvox_algorithm.utils.io_funcs import write_json_file
from nuvox_algorithm.trace_algorithm.utils import _load_dataset
from nuvox_algorithm.trace_algorithm.trace_algorithm import TraceAlgorithm


if __name__ == '__main__':
    """
    This script uses your trace algorithm to perform predictions for the
    competition test set and saves them to a 'submission.json' file which
    you can then upload on the nuvox website.
    """
    # Load dataset of Swipes from data dump JSON file.
    swipes = _load_dataset(remove_inaccurate_swipes=True)

    # Instantiate your TraceAlgorithm here.
    trace_algorithm = TraceAlgorithm()

    predictions = []
    for swipe in tqdm(swipes):

        kis_to_predicted_proba = trace_algorithm.predict_intended_kis(trace=swipe.trace)

        predictions.append(
            {
                "id": swipe.id,
                "prediction": kis_to_predicted_proba
            }
        )

    write_json_file(file_path=TRACE_ALGORITHM_SUBMISSION_PATH, data=predictions)
    print(f'Predictions saved to {TRACE_ALGORITHM_SUBMISSION_PATH}')
