from pathlib import Path
from typing import TYPE_CHECKING

from fastapi.responses import FileResponse

from . import globals

if TYPE_CHECKING:
    from .page import page


def create_favicon_routes() -> None:
    fallback = Path(__file__).parent / 'static' / 'favicon.ico'
    for path, favicon in globals.favicons.items():
        if is_remote_url(favicon):
            continue
        globals.app.add_route(f'{"" if path == "/" else path}/favicon.ico',
                              lambda _, favicon=favicon or globals.favicon or fallback: FileResponse(favicon))


def get_favicon_url(page: 'page', prefix: str) -> str:
    favicon = page.favicon or globals.favicon
    if is_remote_url(favicon):
        return favicon
    elif not favicon:
        return f'{prefix}/_nicegui/static/favicon.ico'
    elif page.path == '/':
        return f'{prefix}/favicon.ico'
    else:
        return f'{prefix}{page.path}/favicon.ico'


def is_remote_url(favicon: str) -> bool:
    return favicon and (favicon.startswith('http://') or favicon.startswith('https://'))
