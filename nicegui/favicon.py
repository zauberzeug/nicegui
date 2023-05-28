import urllib.parse
from pathlib import Path
from typing import TYPE_CHECKING, Optional

from fastapi import Response
from fastapi.responses import FileResponse

from . import __version__, globals

if TYPE_CHECKING:
    from .page import page


def create_favicon_route(path: str, favicon: Optional[str]) -> None:
    if favicon and Path(favicon).exists():
        globals.app.add_route(f'{path}/favicon.ico', lambda _: FileResponse(favicon))


def get_favicon_url(page: 'page', prefix: str) -> str:
    favicon = str(page.favicon or globals.favicon)
    if favicon and is_remote_url(favicon):
        return favicon
    elif not favicon:
        return f'{prefix}/_nicegui/{__version__}/static/favicon.ico'
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
    return Response(char_to_svg(globals.favicon), media_type='image/svg+xml')


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
