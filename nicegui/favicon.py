import base64
import io
import urllib.parse
from pathlib import Path
from typing import TYPE_CHECKING, Optional, Tuple, Union

from fastapi.responses import FileResponse, Response, StreamingResponse

from . import __version__, globals
from .helpers import is_file

if TYPE_CHECKING:
    from .page import page


def create_favicon_route(path: str, favicon: Optional[Union[str, Path]]) -> None:
    if is_file(favicon):
        globals.app.add_route(f'{path}/favicon.ico', lambda _: FileResponse(favicon))


def get_favicon_url(page: 'page', prefix: str) -> str:
    favicon = page.favicon or globals.favicon
    if not favicon:
        return f'{prefix}/_nicegui/{__version__}/static/favicon.ico'
    favicon = str(favicon).strip()
    if is_remote_url(favicon):
        return favicon
    elif is_data_url(favicon):
        return favicon
    elif is_svg(favicon):
        return svg_to_data_url(favicon)
    elif is_char(favicon):
        return svg_to_data_url(char_to_svg(favicon))
    elif page.path == '/':
        return f'{prefix}/favicon.ico'
    else:
        return f'{prefix}{page.path}/favicon.ico'


def get_favicon_response() -> Response:
    if not globals.favicon:
        raise ValueError(f'invalid favicon: {globals.favicon}')
    favicon = str(globals.favicon).strip()
    if is_svg(favicon):
        return Response(favicon, media_type='image/svg+xml')
    elif is_data_url(favicon):
        media_type, bytes = data_url_to_bytes(favicon)
        return StreamingResponse(io.BytesIO(bytes), media_type=media_type)
    elif is_char(favicon):
        return Response(char_to_svg(favicon), media_type='image/svg+xml')
    else:
        raise ValueError(f'invalid favicon: {favicon}')


def is_remote_url(favicon: str) -> bool:
    return favicon.startswith('http://') or favicon.startswith('https://')


def is_char(favicon: str) -> bool:
    return len(favicon) == 1


def is_svg(favicon: str) -> bool:
    return favicon.strip().startswith('<svg')


def is_data_url(favicon: str) -> bool:
    return favicon.startswith('data:')


def char_to_svg(char: str) -> str:
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


def svg_to_data_url(svg: str) -> str:
    svg_urlencoded = urllib.parse.quote(svg)
    return f'data:image/svg+xml,{svg_urlencoded}'


def data_url_to_bytes(data_url: str) -> Tuple[str, bytes]:
    media_type, base64_image = data_url.split(',', 1)
    media_type = media_type.split(':')[1].split(';')[0]
    return media_type, base64.b64decode(base64_image)
