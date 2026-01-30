import importlib.util
import json
from datetime import date, datetime
from typing import Any

from fastapi.responses import JSONResponse

HAS_NUMPY = importlib.util.find_spec('numpy') is not None


def dumps(obj: Any,
          sort_keys: bool = False,
          separators: tuple[str, str] | None = None, *,
          indent: bool = False) -> str:
    """Serializes a Python object to a JSON-encoded string.

    This implementation uses Python's default json module, but extends it in order to support NumPy arrays.
    """
    if separators is None:
        separators = (',', ':')
    return json.dumps(
        obj,
        sort_keys=sort_keys,
        separators=separators,
        indent=2 if indent else None,
        allow_nan=False,
        ensure_ascii=False,
        cls=NumpyJsonEncoder)


def loads(value: str) -> Any:
    """Deserialize a JSON-encoded string to a corresponding Python object/value.

    Uses Python's default json module internally.
    """
    return json.loads(value)


class NiceGUIJSONResponse(JSONResponse):
    """FastAPI response class to support our custom json serializer implementation."""

    def render(self, content: Any) -> bytes:
        return dumps(content).encode('utf-8')


class NumpyJsonEncoder(json.JSONEncoder):
    """Special json encoder that supports NumPy arrays and date/datetime objects."""

    def default(self, o):
        if HAS_NUMPY:
            import numpy as np  # pylint: disable=import-outside-toplevel
            if isinstance(o, np.integer):
                return int(o)
            if isinstance(o, np.floating):
                return float(o)
            if isinstance(o, np.ndarray):
                return o.tolist()
        if isinstance(o, (datetime, date)):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)
