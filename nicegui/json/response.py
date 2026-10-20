from typing import Any

from fastapi.responses import JSONResponse

from . import _dumps_bytes


class NiceGUIJSONResponse(JSONResponse):
    """FastAPI response class to support our custom json serializer implementation."""

    def render(self, content: Any) -> bytes:
        return _dumps_bytes(content)
