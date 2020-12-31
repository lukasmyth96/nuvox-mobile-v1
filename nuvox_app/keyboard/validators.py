from typing import List, Dict

from django.core.exceptions import ValidationError

from nuvox_algorithm.utils.list_funcs import all_subsequences
from nuvox_algorithm.core import Keyboard, nuvox_key_list


def validate_trace(trace: List[Dict[str, float]]):
    """Validate that trace is List[Dict[str, float]] where
    each trace point is a dict with keys 'x', 'y' and 't' that
    all map to float values."""
    if not trace:
        raise ValidationError('Field "trace" cannot be empty')

    if not isinstance(trace, list):
        raise ValidationError('Field "trace" must be a list')

    for trace_point in trace:
        validate_trace_point(trace_point)


def validate_trace_point(trace_point: Dict[str, float]):
    if not isinstance(trace_point, dict):
        raise ValidationError('Each trace point must be a dict')

    if not set(trace_point.keys()) == {'x', 'y', 't'}:
        raise ValidationError(f'Each trace point have keys x, y, t but found'
                              f'point with keys: {trace_point}')

    if not all([isinstance(val, float) for val in trace_point.values()]):
        raise ValidationError(f'Each trace point value must a float')


def validate_trace_matches_target_text(trace: List[Dict[str, float]],
                                       target_text: str):
    keyboard = Keyboard(keys=nuvox_key_list)
    trace_kis = keyboard.trace_to_kis(trace)
    target_text_kis = keyboard.text_to_kis(target_text, skip_invalid_chars=True)

