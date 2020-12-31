from dataclasses import dataclass
from typing import List


@dataclass
class Key:
    id: str
    chars: List[str]  # characters contained in key.
    x0: float  # x coordinate of top left corner.
    y0: float  # y coordinate of top left corner.
    x1: float  # x coordinate of bottom right corner.
    y1: float  # y coordinate of bottom right corner.

    def __post_init__(self):
        assert 0.0 <= self.x0 <= self.x1 <= 1.0
        assert 0.0 <= self.y0 <= self.y1 <= 1.0
