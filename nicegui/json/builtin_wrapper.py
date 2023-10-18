import json
from datetime import date, datetime
from typing import Any, Optional, Tuple

from fastapi import Response

try:
    import numpy as np
    has_numpy = True
except ImportError:
    has_numpy = False


def dumps(obj: Any, sort_keys: bool = False, separators: Optional[Tuple[str, str]] = None):
    """Serializes a Python object to a JSON-encoded string.

    This implementation uses Python's default json module, but extends it in order to support NumPy arrays.
    """
    if separators is None:
        separators = (',', ':')
    return json.dumps(
        obj,
        sort_keys=sort_keys,
        separators=separators,
        indent=None,
        allow_nan=False,
        ensure_ascii=False,
        cls=NumpyJsonEncoder)


def loads(value: str) -> Any:
    """Deserialize a JSON-encoded string to a corresponding Python object/value.

    Uses Python's default json module internally.
    """
    return json.loads(value)


class NiceGUIJSONResponse(Response):
    """FastAPI response class to support our custom json serializer implementation."""
    media_type = 'application/json'

    def render(self, content: Any) -> bytes:
        return dumps(content).encode('utf-8')


class NumpyJsonEncoder(json.JSONEncoder):
    """Special json encoder that supports NumPy arrays and date/datetime objects."""

    def default(self, o):
        if has_numpy and isinstance(o, np.integer):
            return int(o)
        if has_numpy and isinstance(o, np.floating):
            return float(o)
        if has_numpy and isinstance(o, np.ndarray):
            return o.tolist()
        if isinstance(o, (datetime, date)):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)
