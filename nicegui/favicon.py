import urllib
from pathlib import Path
from typing import TYPE_CHECKING, Optional

from fastapi.responses import FileResponse

from . import __version__, globals

if TYPE_CHECKING:
    from .page import page


def create_favicon_route(path: str, favicon: Optional[str]) -> None:
    if favicon and (is_remote_url(favicon) or is_char(favicon)):
        return
    fallback = Path(__file__).parent / 'static' / 'favicon.ico'
    path = f'{"" if path == "/" else path}/favicon.ico'
    globals.app.remove_route(path)
    globals.app.add_route(path, lambda _: FileResponse(favicon or globals.favicon or fallback))


def get_favicon_url(page: 'page', prefix: str) -> str:
    favicon = page.favicon or globals.favicon
    if favicon and is_remote_url(favicon):
        return favicon
    elif not favicon:
        return f'{prefix}/_nicegui/{__version__}/static/favicon.ico'
    if is_char(favicon):
        return char_to_data_url(favicon)
    elif page.path == '/':
        return f'{prefix}/favicon.ico'
    else:
        return f'{prefix}{page.path}/favicon.ico'


def is_remote_url(favicon: str) -> bool:
    return favicon.startswith('http://') or favicon.startswith('https://')


def is_char(favicon: str) -> bool:
    return len(favicon) == 1


def char_to_data_url(char: str) -> str:
    svg = f'''
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
    svg_urlencoded = urllib.parse.quote(svg)
    data_url = f"data:image/svg+xml,{svg_urlencoded}"
    return data_url
