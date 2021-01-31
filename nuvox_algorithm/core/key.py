from __future__ import annotations
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
        assert 0.0 <= self.x0 <= self.x1 <= 1.0, 'Invalid key coordinates'
        assert 0.0 <= self.y0 <= self.y1 <= 1.0, 'Invalid key coordinates'
        
    def contains(self, x: float, y: float) -> bool:
        """Returns True if (x, y) is within bounds of key."""
        return (self.x0 <= x <= self.x1) and (self.y0 <= y <= self.y1)

    def intersects(self, other: Key) -> bool:
        """Returns True if this key intersections the 'other' key."""
        return not ((self.x1 <= other.x0) or (self.x0 >= other.x1) or (self.y0 >= other.y1) or (self.y1 <= other.y0))
