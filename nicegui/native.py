from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class Native:
    start_args: Dict[str, Any] = field(default_factory=dict)
    window_args: Dict[str, Any] = field(default_factory=dict)
