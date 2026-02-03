from dataclasses import dataclass, field
from typing import Any

from ..dataclasses import KWONLY_SLOTS
from .native import WindowProxy


@dataclass(**KWONLY_SLOTS)
class NativeConfig:
    start_args: dict[str, Any] = field(default_factory=dict)
    window_args: dict[str, Any] = field(default_factory=dict)
    settings: dict[str, Any] = field(default_factory=dict)
    main_window: WindowProxy | None = None
