import uuid
from dataclasses import dataclass, field
from typing import Callable, List


@dataclass
class EventListener:
    id: str = field(init=False)
    element_id: int
    type: str
    args: List[str]
    handler: Callable
    throttle: float

    def __post_init__(self) -> None:
        self.id = str(uuid.uuid4())
