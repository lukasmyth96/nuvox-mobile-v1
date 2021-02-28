import pytest

from nuvox_algorithm.trace_algorithm.utils import get_corner_to_corner_variants


@pytest.mark.parametrize(
    'kis, expected_variants', [
        ('167', ['167']),  # contains not corner-to-corner
        ('13', ['13', '123']),
        ('139', ['139', '1369', '1239', '12369'])
    ]
)
def test_get_corner_to_corner_variants(kis, expected_variants):
    assert get_corner_to_corner_variants(kis) == expected_variants
