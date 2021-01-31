import pytest

from nuvox_algorithm.core import Key


@pytest.fixture(scope='function')
def key_1() -> Key:
    return Key(id='1', chars=['a', 'b', 'c'], x0=0/3, x1=1/3, y0=0/3, y1=1/3)


@pytest.fixture(scope='function')
def key_2() -> Key:
    return Key(id='2', chars=['d', 'e', 'f'], x0=1/3, x1=2/3, y0=0/3, y1=1/3)


@pytest.fixture(scope='function')
def key_3() -> Key:
    return Key(id='3', chars=['g', 'h', 'i'], x0=2/3, x1=3/3, y0=0/3, y1=1/3)
