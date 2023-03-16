"""
Custom json module. Provides dumps and loads implementations
wrapping the orjson package. If the orjson package is not available,
the standard Python json module is used.

This custom module is required in order to override the json-module used
in socketio.AsyncServer, which expects a module as parameter
to override Python's default json module.
"""

try:
    # orjson not available on all platforms, fallback to Python's json module if not available
    import orjson
    has_orjson = True
except ImportError:
    has_orjson = False


if has_orjson:
    from nicegui.json.orjson_wrapper import NiceGUIJSONResponse, dumps, loads
else:
    from nicegui.json.builtin_wrapper import NiceGUIJSONResponse, dumps, loads


__all__ = [
    'dumps',
    'loads',
    'NiceGUIJSONResponse'
]
