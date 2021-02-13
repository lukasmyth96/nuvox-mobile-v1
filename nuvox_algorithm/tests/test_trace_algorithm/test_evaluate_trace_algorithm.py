from nuvox_algorithm.core import   Swipe, TracePoint
from nuvox_algorithm.trace_algorithm import TraceAlgorithm
from nuvox_algorithm.trace_algorithm.scripts.evaluate_trace_algorithm import main_evaluate_trace_algorithm, ranked_key_id_sequences


def test_ranked_key_id_sequences():
    kis_to_predicted_proba = {
        '123': 0.2,
        '456': 0.5,
        '789': 0.3
    }

    assert ranked_key_id_sequences(kis_to_predicted_proba) == ['456', '789', '123']


def test_main_evaluate_trace_algorithm():

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
    assert main_evaluate_trace_algorithm(
        swipes=swipes,
        trace_algorithm=trace_algorithm
    ) == (1.0, 1.0)

    trace_algorithm.predict_intended_kis = lambda trace: {'999': 1.0}
    assert main_evaluate_trace_algorithm(
        swipes=swipes,
        trace_algorithm=trace_algorithm
    ) == (0.0, 0.0)
