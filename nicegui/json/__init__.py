"""
Custom json module. Provides dumps and loads implementations
wrapping the orjson package. If the orjson package is not available,
the standard Python json module is used.

This custom module is required in order to override the json-module used
in socketio.AsyncServer, which expects a module as parameter
to override Python's default json module.
"""

try:
    from nicegui.json.orjson_wrapper import NiceGUIJSONResponse, dumps, loads
except ImportError:
    from nicegui.json.builtin_wrapper import NiceGUIJSONResponse, dumps, loads  # type: ignore


__all__ = [
    'NiceGUIJSONResponse',
    'dumps',
    'loads',
]
