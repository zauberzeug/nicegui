from pathlib import Path
from typing import TYPE_CHECKING, Optional

from fastapi.responses import FileResponse

from . import globals

if TYPE_CHECKING:
    from .page import page


def create_favicon_route(path: str, favicon: Optional[str]) -> None:
    if favicon and is_remote_url(favicon):
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
        return f'{prefix}/_nicegui/static/favicon.ico'
    elif page.path == '/':
        return f'{prefix}/favicon.ico'
    else:
        return f'{prefix}{page.path}/favicon.ico'


def is_remote_url(favicon: str) -> bool:
    return favicon.startswith('http://') or favicon.startswith('https://')
