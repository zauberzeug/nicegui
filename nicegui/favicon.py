from pathlib import Path

from fastapi.responses import FileResponse

from . import globals


def create_favicon_routes() -> None:
    fallback = Path(__file__).parent / 'static' / 'favicon.ico'
    for path, favicon in globals.favicons.items():
        if is_remote_url(favicon):
            continue
        globals.app.add_route(f'{path}/favicon.ico', lambda _: FileResponse(favicon or globals.favicon or fallback))
    if '/' not in globals.favicons:
        globals.app.add_route('/favicon.ico', lambda _: FileResponse(globals.favicon or fallback))


def get_favicon_url(path: str, favicon: str) -> str:
    favicon = favicon or globals.favicon
    if is_remote_url(favicon):
        return favicon
    return f'{path[1:]}/favicon.ico' if favicon else 'static/favicon.ico'


def is_remote_url(favicon: str) -> bool:
    return favicon and (favicon.startswith('http://') or favicon.startswith('https://'))
