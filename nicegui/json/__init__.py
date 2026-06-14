"""
Custom json module. Provides dumps and loads implementations
wrapping the orjson package. If the orjson package is not available,
the standard Python json module is used.

This custom module is required in order to override the json-module used
in socketio.AsyncServer, which expects a module as parameter
to override Python's default json module.
"""

from typing import TYPE_CHECKING

try:
    from .orjson_wrapper import dumps, loads
except ImportError:
    from .builtin_wrapper import dumps, loads  # type: ignore

if TYPE_CHECKING:
    from .response import NiceGUIJSONResponse


__all__ = [
    'NiceGUIJSONResponse',
    'dumps',
    'loads',
]


def __getattr__(name: str) -> object:
    if name == 'NiceGUIJSONResponse':  # deferred so that `import nicegui.json` does not pull in FastAPI
        from .response import NiceGUIJSONResponse  # pylint: disable=import-outside-toplevel
        globals()[name] = NiceGUIJSONResponse
        return NiceGUIJSONResponse
    raise AttributeError(f'module {__name__!r} has no attribute {name!r}')
