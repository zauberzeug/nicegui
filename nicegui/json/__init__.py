"""
Custom json module. Provides dumps and loads implementations
wrapping the `orjson` package.

Custom module required in order to override json-module used
in socketio.AsyncServer, which expects a module as parameter
to override Python's default json module.
"""

from nicegui.json.orjson_wrapper import dumps, loads

__all__ = [
    'dumps',
    'loads'
]
