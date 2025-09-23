from __future__ import annotations

import base64
import io
import urllib.parse
from pathlib import Path
from typing import TYPE_CHECKING

from fastapi.responses import FileResponse, Response, StreamingResponse

from . import core
from .helpers import is_file
from .version import __version__

if TYPE_CHECKING:
    from .page import page


def create_favicon_route(path: str, favicon: str | Path | None) -> None:
    """Create a favicon route for the given path."""
    if is_file(favicon):
        core.app.add_route('/favicon.ico' if path == '/' else f'{path}/favicon.ico',
                           lambda _: FileResponse(favicon))  # type: ignore


def get_favicon_url(page: page, prefix: str) -> str:
    """Return the URL of the favicon for a given page."""
    favicon = page.favicon or core.app.config.favicon
    if not favicon:
        return f'{prefix}/_nicegui/{__version__}/static/favicon.ico'

    favicon = str(favicon).strip()
    if _is_remote_url(favicon):
        return favicon
    if _is_data_url(favicon):
        return favicon
    if _is_svg(favicon):
        return _svg_to_data_url(favicon)
    if _is_char(favicon):
        return _svg_to_data_url(_char_to_svg(favicon))
    if page.path == '/' or page.favicon is None:
        return f'{prefix}/favicon.ico'

    return f'{prefix}{page.path}/favicon.ico'


def get_favicon_response() -> Response:
    """Return the FastAPI response for the global favicon."""
    if not core.app.config.favicon:
        raise ValueError(f'invalid favicon: {core.app.config.favicon}')
    favicon = str(core.app.config.favicon).strip()

    if _is_svg(favicon):
        return Response(favicon, media_type='image/svg+xml')
    if _is_data_url(favicon):
        media_type, bytes_ = _data_url_to_bytes(favicon)
        return StreamingResponse(io.BytesIO(bytes_), media_type=media_type)
    if _is_char(favicon):
        return Response(_char_to_svg(favicon), media_type='image/svg+xml')

    raise ValueError(f'invalid favicon: {favicon}')


def _is_remote_url(favicon: str) -> bool:
    return favicon.startswith(('http://', 'https://'))


def _is_char(favicon: str) -> bool:
    return len(favicon) == 1 or '\ufe0f' in favicon


def _is_svg(favicon: str) -> bool:
    return favicon.strip().startswith('<svg')


def _is_data_url(favicon: str) -> bool:
    return favicon.startswith('data:')


def _char_to_svg(char: str) -> str:
    return f'''
        <svg viewBox="0 0 128 128" width="128" height="128" xmlns="http://www.w3.org/2000/svg" >
            <style>
                @supports (-moz-appearance:none) {{
                    text {{
                        font-size: 100px;
                        transform: translateY(0.1em);
                    }}
                }}
                text {{
                    font-family: Arial, sans-serif;
                }}
            </style>
            <text y=".9em" font-size="128" font-family="Georgia, sans-serif">{char}</text>
        </svg>
    '''


def _svg_to_data_url(svg: str) -> str:
    svg_urlencoded = urllib.parse.quote(svg)
    return f'data:image/svg+xml,{svg_urlencoded}'


def _data_url_to_bytes(data_url: str) -> tuple[str, bytes]:
    media_type, base64_image = data_url.split(',', 1)
    media_type = media_type.split(':')[1].split(';')[0]
    return media_type, base64.b64decode(base64_image)
