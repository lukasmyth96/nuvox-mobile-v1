from dataclasses import dataclass
from typing import List


@dataclass
class TracePoint:
    x: float
    y: float
    t: float

    def __post_init__(self):
        assert 0.0 <= self.x <= 1.0
        assert 0.0 <= self.y <= 1.0

    def __repr__(self):
        return f'TracePoint(x={self.x:.2f}, y={self.y:.2f}, t={self.t:.2f})'


@dataclass
class Swipe:
    id: int                         # ID of swipe in database.
    user_id: int                    # ID of user who generated swipe.
    trace: List[TracePoint]         # List of TracePoint objects.
    target_text: str                # Word user intended to swipe.
    target_kis: str                 # Target key-id-sequence.
    trace_matches_text: bool        # Whether trace sufficiently matches text.

    def __repr__(self):
        return f'Swipe(target_text={self.target_text}, trace_matches_text={self.trace_matches_text})'
