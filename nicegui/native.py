from dataclasses import dataclass, field
from typing import Any, Dict

from .helpers import KWONLY_SLOTS


@dataclass(**KWONLY_SLOTS)
class Native:
    start_args: Dict[str, Any] = field(default_factory=dict)
    window_args: Dict[str, Any] = field(default_factory=dict)
