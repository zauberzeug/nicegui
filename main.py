#!/usr/bin/env python3
# pylint: disable=missing-function-docstring
import os
from pathlib import Path

from fastapi import Request
from starlette.middleware.sessions import SessionMiddleware

import prometheus
from nicegui import app, ui
from website import anti_scroll_hack, documentation_pages, fly, main_page, svg

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


@app.post('/dark_mode')
async def post_dark_mode(request: Request) -> None:
    app.storage.browser['dark_mode'] = (await request.json()).get('value')


ui.page('/')(main_page.create)
ui.page('/documentation')(documentation_pages.create_overview)
ui.page('/documentation/{name}')(documentation_pages.create_page)


@app.get('/status')
def status():
    return 'Ok'


# NOTE: do not reload on fly.io (see https://github.com/zauberzeug/nicegui/discussions/1720#discussioncomment-7288741)
ui.run(uvicorn_reload_includes='*.py, *.css, *.html', reload=not on_fly, reconnect_timeout=10.0)
