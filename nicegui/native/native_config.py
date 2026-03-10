from dataclasses import dataclass, field
from typing import Any

from ..events import Handler, NativeEventArguments
from .event_manager import event_manager
from .native import WindowProxy


@dataclass(kw_only=True, slots=True)
class NativeConfig:
    start_args: dict[str, Any] = field(default_factory=dict)
    window_args: dict[str, Any] = field(default_factory=dict)
    settings: dict[str, Any] = field(default_factory=dict)
    main_window: WindowProxy | None = None

    def on(self, event_type: str, handler: Handler[NativeEventArguments]) -> None:
        """Register a handler for a native window event.

        Supported events: shown, loaded, minimized, maximized, restored, resized, moved, closed.

        :param event_type: the event name
        :param handler: callback, may accept a NativeEventArguments parameter or no parameters
        """
        event_manager.on(event_type, handler)
