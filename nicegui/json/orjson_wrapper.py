from typing import Any, Optional, Tuple

import orjson
from fastapi import Response

ORJSON_OPTS = orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_NON_STR_KEYS


def dumps(obj: Any, sort_keys: bool = False, separators: Optional[Tuple[str, str]] = None):
    """Serializes a Python object to a JSON-encoded string.

    By default, this function supports serializing numpy arrays,
    which Python's json module does not.

    Uses package `orjson` internally.
    """
    # note that parameters `sort_keys` and `separators` are required by AsyncServer's
    # internal calls, which match Python's default `json.dumps` API.
    assert separators is None or separators == (',', ':'), \
        f'NiceGUI JSON serializer only supports Python''s default ' +\
        f'JSON separators "," and ":", but got {separators} instead.'

    opts = ORJSON_OPTS

    # flag for sorting by object keys
    if sort_keys:
        opts |= orjson.OPT_SORT_KEYS

    return orjson.dumps(obj, option=opts).decode('utf-8')


def loads(value: str) -> Any:
    """Deserialize a JSON-encoded string to a corresponding Python object/value.

    Uses package `orjson` internally.
    """
    return orjson.loads(value)


class NiceGUIJSONResponse(Response):
    """FastAPI response class to support our custom json serializer implementation.

    Uses package `orjson` internally.
    """
    media_type = 'application/json'

    def render(self, content: Any) -> bytes:
        return orjson.dumps(content, option=ORJSON_OPTS)
