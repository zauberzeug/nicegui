from typing import Any

from fastapi.responses import JSONResponse

from . import render as _render


class NiceGUIJSONResponse(JSONResponse):
    """FastAPI response class to support our custom json serializer implementation."""

    def render(self, content: Any) -> bytes:
        return _render(content)
