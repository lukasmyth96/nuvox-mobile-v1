from dataclasses import dataclass
from typing import List


@dataclass
class Key:
    id: str
    chars: List[str]
