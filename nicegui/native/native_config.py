from dataclasses import dataclass, field
from typing import Any

from .native import WindowProxy


@dataclass(kw_only=True, slots=True)
class NativeConfig:
    start_args: dict[str, Any] = field(default_factory=dict)
    window_args: dict[str, Any] = field(default_factory=dict)
    settings: dict[str, Any] = field(default_factory=dict)
    main_window: WindowProxy | None = None
