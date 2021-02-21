from dataclasses import dataclass
from typing import List, Optional


@dataclass
class TracePoint:
    """Data class for a single point within a Swipe trace."""
    x: float  # x∈(0, 1) is x coordinate relative to top-left of key pad.
    y: float  # y∈(0, 1) is y coordinate relative to top-left of key pad
    t: float  # t∈ℝ is the time (s) at which this point was recorded relative to start of swipe.
    key_id: Optional[str] = None  # ID (1-9) of key that this point belongs to on the keyboard.

    def __post_init__(self):
        assert 0.0 <= self.x <= 1.0
        assert 0.0 <= self.y <= 1.0

    def __repr__(self):
        return f'TracePoint(x={self.x:.2f}, y={self.y:.2f}, t={self.t:.2f}, key_id={self.key_id})'


@dataclass
class Swipe:
    """Data class for a single Swipe.

    Notes
    -------
    - 'target_text' and 'target_kis' fields will be 'None' for swipes in the test set.
    """
    id: int                         # ID of swipe in database.
    user_id: int                    # ID of user who generated swipe.
    device_type: str                # pc/mobile/tablet
    trace: List[TracePoint]         # List of TracePoint objects.
    target_text: Optional[str]      # Word user intended to swipe.
    target_kis: Optional[str]       # Target key-id-sequence e.g. if target_text='hello' then target_kis='3246'.

    def __repr__(self):
        return f'Swipe(target_text={self.target_text}, target_kis={self.target_kis})'
