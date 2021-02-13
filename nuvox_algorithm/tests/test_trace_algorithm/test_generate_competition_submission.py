from nuvox_algorithm.utils.io_funcs import read_json_file
from nuvox_algorithm.core import Swipe, TracePoint
from nuvox_algorithm.trace_algorithm import TraceAlgorithm
from nuvox_algorithm.trace_algorithm.scripts.generate_competition_submission import main_generate_competition_submission


def test_main_generate_competition_submission(tmpdir):

    output_path = str(tmpdir / 'submission.json')

    swipes = [
        Swipe(
            id=1,
            user_id=1,
            device_type='pc',
            trace=[
                TracePoint(x=0.1, y=0.1, t=0.1, key_id='1')
            ],
            target_text='hello',
            target_kis='3246'
        )
    ]

    trace_algorithm = TraceAlgorithm(rdp_threshold=0, angle_threshold=0)
    trace_algorithm.predict_intended_kis = lambda trace: {'3246': 1.0}

    main_generate_competition_submission(
        swipes=swipes,
        trace_algorithm=trace_algorithm,
        output_path=output_path
    )

    generated_submission = read_json_file(output_path)

    assert isinstance(generated_submission, list)
    assert len(generated_submission) == 1
    assert generated_submission[0] == {
        'id': 1,
        'prediction': {
            '3246': 1.0
        }
    }
