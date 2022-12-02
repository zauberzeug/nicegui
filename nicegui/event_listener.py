from dataclasses import dataclass
from typing import Callable, List


@dataclass
class EventListener:
    element_id: str
    type: str
    args: List[str]
    handler: Callable
    throttle: float
