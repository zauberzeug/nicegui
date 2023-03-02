from typing import Any

import orjson
from fastapi import Response

from nicegui.json.orjson_wrapper import ORJSON_OPTS


class NiceGUIJSONResponse(Response):
    media_type = 'application/json'

    def render(self, content: Any) -> bytes:
        return orjson.dumps(content, option=ORJSON_OPTS)
