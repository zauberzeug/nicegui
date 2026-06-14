from typing import Any

from fastapi.responses import JSONResponse

try:
    import orjson

    from .orjson_wrapper import ORJSON_OPTS, _orjson_converter

    def _render(content: Any) -> bytes:
        return orjson.dumps(content, option=ORJSON_OPTS, default=_orjson_converter)  # pylint: disable=no-member
except ImportError:
    from . import dumps

    def _render(content: Any) -> bytes:
        return dumps(content).encode('utf-8')


class NiceGUIJSONResponse(JSONResponse):
    """FastAPI response class to support our custom json serializer implementation."""

    def render(self, content: Any) -> bytes:
        return _render(content)
