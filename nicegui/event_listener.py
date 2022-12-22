from dataclasses import dataclass
from typing import Callable, List


@dataclass
class EventListener:
    element_id: int
    type: str
    args: List[str]
    handler: Callable
    throttle: float
