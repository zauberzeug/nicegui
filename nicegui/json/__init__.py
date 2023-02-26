"""
Custom json module. Provides dumps and loads implementations
wrapping orjson.

Custom module required in order to override json-module used
in socketio.AsyncServer.
"""

from typing import Any

import orjson
from fastapi import Response

ORJSON_OPTS = orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_NON_STR_KEYS


def dumps(obj, sort_keys=False, separators=None):
    """
    Serializes a Python object to a JSON-encoded string.
    By default, this function supports serializing numpy arrays.
    """
    return orjson.dumps(obj, option=ORJSON_OPTS).decode('utf-8')


def loads(value):
    """
    Deserializes a JSON-encoded string to a corresponding Python object/value.
    """
    return orjson.loads(value)


class NiceGUIJSONResponse(Response):
    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        return orjson.dumps(content, option=ORJSON_OPTS)
