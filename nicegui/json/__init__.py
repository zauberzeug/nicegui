"""
Custom json module. Provides dumps and loads implementations
wrapping the orjson package. If the orjson package is not available,
the standard Python json module is used.

This custom module is required in order to override the json-module used
in socketio.AsyncServer, which expects a module as parameter
to override Python's default json module.
"""

from typing import TYPE_CHECKING

from .. import _lazy

try:
    from .orjson_wrapper import dumps, loads, render
except ImportError:
    from .builtin_wrapper import dumps, loads, render  # type: ignore

# deferred so that `import nicegui.json` does not pull in FastAPI
_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    'NiceGUIJSONResponse': ('.response', 'NiceGUIJSONResponse'),
}

if TYPE_CHECKING:
    from .response import NiceGUIJSONResponse


__all__ = [
    'NiceGUIJSONResponse',
    'dumps',
    'loads',
    'render',
]


def __getattr__(name: str) -> object:
    return _lazy.resolve(__name__, __name__, _LAZY_IMPORTS, name)
