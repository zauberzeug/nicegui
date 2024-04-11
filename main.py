#!/usr/bin/env python3
import os
from pathlib import Path
from typing import Optional

from fastapi import HTTPException, Request
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware

import prometheus
from nicegui import app, ui
from website import anti_scroll_hack, documentation, fly, main_page, svg

prometheus.start_monitor(app)

# session middleware is required for demo in documentation and prometheus
app.add_middleware(SessionMiddleware, secret_key=os.environ.get('NICEGUI_SECRET_KEY', ''))

on_fly = fly.setup()
anti_scroll_hack.setup()

app.add_static_files('/favicon', str(Path(__file__).parent / 'website' / 'favicon'))
app.add_static_files('/fonts', str(Path(__file__).parent / 'website' / 'fonts'))
app.add_static_files('/static', str(Path(__file__).parent / 'website' / 'static'))
app.add_static_file(local_file=svg.PATH / 'logo.png', url_path='/logo.png')
app.add_static_file(local_file=svg.PATH / 'logo_square.png', url_path='/logo_square.png')

documentation.build_search_index()


@app.post('/dark_mode')
async def _post_dark_mode(request: Request) -> None:
    app.storage.browser['dark_mode'] = (await request.json()).get('value')


@ui.page('/')
def _main_page() -> None:
    main_page.create()


@ui.page('/documentation')
def _documentation_page() -> None:
    documentation.render_page(documentation.registry[''], with_menu=False)


@ui.page('/documentation/{name}')
def _documentation_detail_page(name: str) -> Optional[RedirectResponse]:
    if name in documentation.registry:
        documentation.render_page(documentation.registry[name])
        return None
    if name in documentation.redirects:
        return RedirectResponse(documentation.redirects[name])
    raise HTTPException(404, f'documentation for "{name}" could not be found')


@app.get('/status')
def _status():
    return 'Ok'


# NOTE: do not reload on fly.io (see https://github.com/zauberzeug/nicegui/discussions/1720#discussioncomment-7288741)
ui.run(uvicorn_reload_includes='*.py, *.css, *.html', reload=not on_fly, reconnect_timeout=10.0)
