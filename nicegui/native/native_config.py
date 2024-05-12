from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from ..dataclasses import KWONLY_SLOTS
from .native import WindowProxy


@dataclass(**KWONLY_SLOTS)
class NativeConfig:
    start_args: Dict[str, Any] = field(default_factory=dict)
    window_args: Dict[str, Any] = field(default_factory=dict)
    settings: Dict[str, Any] = field(default_factory=dict)
    main_window: Optional[WindowProxy] = None
