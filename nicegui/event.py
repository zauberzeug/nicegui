from dataclasses import dataclass
from typing import Callable, List


@dataclass
class Event:
    element_id: str
    type: str
    args: List[str]
    handler: Callable
