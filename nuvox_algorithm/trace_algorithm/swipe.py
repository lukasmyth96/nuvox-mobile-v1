from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Swipe:
    id: int                         # ID of swipe in database.
    user_id: int                    # ID of user who generated swipe.
    trace: List[Dict[str, float]]   # Sequence of x, y, t trace points.
    target_text: str                # Word user intended to swipe.
    target_kis: str                 # Target key-id-sequence.
    trace_matches_text: bool        # Whether trace sufficiently matches text.
