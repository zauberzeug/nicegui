#!/usr/bin/env python3
import os
from pathlib import Path

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import Response

from nicegui import app, core, ui
from nicegui.page_arguments import RouteMatch
from website import documentation, examples_page, fly, header, imprint_privacy, main_page, rate_limits, svg
from website.i18n import SUPPORTED_LANGUAGES, get_url_prefix, set_language


@app.add_middleware
class DocsSetCacheControlMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)
        if request.url.path.startswith('/fonts/') or request.url.path.startswith('/static/'):
            response.headers['Cache-Control'] = core.app.config.cache_control_directives
        elif request.url.path.startswith('/examples/images/'):
            response.headers['Cache-Control'] = 'public, max-age=86400'  # 1 day
        return response


# session middleware is required for demo in documentation
app.add_middleware(SessionMiddleware, secret_key=os.environ.get('NICEGUI_SECRET_KEY', ''))
rate_limits.setup()

on_fly = fly.setup()

app.add_static_files('/favicon', str(Path(__file__).parent / 'website' / 'favicon'))
app.add_static_files('/fonts', str(Path(__file__).parent / 'website' / 'fonts'))
app.add_static_files('/static', str(Path(__file__).parent / 'website' / 'static'))
app.add_static_file(local_file=svg.PATH / 'logo.png', url_path='/logo.png')
app.add_static_file(local_file=svg.PATH / 'logo_square.png', url_path='/logo_square.png')

documentation.build_search_index()
documentation.build_tree()


@app.post('/dark_mode')
async def _post_dark_mode(request: Request) -> None:
    app.storage.browser['dark_mode'] = (await request.json()).get('value')


class custom_sub_pages(ui.sub_pages):
    def _render_page(self, match: RouteMatch) -> bool:
        if match.path == '/' and match.remaining_path:
            return False
        return super()._render_page(match)


def _build_page(lang: str = 'en') -> None:
    """Build the page content for a given language."""
    set_language(lang)
    prefix = get_url_prefix()

    ui.context.client.content.classes('p-0 gap-0')
    header.add_head_html()

    with ui.left_drawer() \
            .classes('column no-wrap gap-1 bg-[#eee] dark:bg-[#1b1b1b] mt-[-20px] px-8 py-20') \
            .style('height: calc(100% + 20px) !important') as menu:
        tree = ui.tree(documentation.tree.nodes, label_key='title',
                       on_select=lambda e: ui.navigate.to(f'{prefix}/documentation/{e.value}')) \
            .classes('w-full').props('accordion no-connectors no-selection-unset')
    menu_button = header.add_header(menu)

    window_state = {'is_desktop': None}
    ui.on('is_desktop', lambda v: window_state.update(is_desktop=v.args))
    ui.add_head_html('''
        <script>
            const mediaQuery = window.matchMedia('(min-width: 1024px)');
            mediaQuery.addEventListener('change', e => emitEvent('is_desktop', e.matches));
            window.addEventListener('load', () => emitEvent('is_desktop', mediaQuery.matches));
        </script>
    ''')

    custom_sub_pages({
        '/': main_page.create,
        '/examples': examples_page.create,
        '/documentation': lambda: documentation.render_page(documentation.registry['']),
        '/documentation/{name}': lambda name: _documentation_detail_page(name, tree, prefix),
        '/imprint_privacy': imprint_privacy.create,
    }, root_path=prefix or None, show_404=False).classes('w-full')

    def _update_menu(path: str):
        if path.startswith('/documentation/'):
            menu_button.visible = True
            if window_state['is_desktop'] is not None:
                menu.value = window_state['is_desktop']
        else:
            menu_button.visible = False
            menu.value = False
    ui.context.client.sub_pages_router.on_path_changed(_update_menu)
    _update_menu(ui.context.client.sub_pages_router.current_path)


@ui.page('/')
@ui.page('/examples')
@ui.page('/documentation')
@ui.page('/documentation/{path:path}')
@ui.page('/imprint_privacy')
def _main_page() -> None:
    _build_page('en')


# Register language-prefixed routes for each supported language (except English).
for _lang in SUPPORTED_LANGUAGES:
    if _lang == 'en':
        continue

    def _make_i18n_handler(lang: str):
        def handler() -> None:
            _build_page(lang)
        handler.__name__ = f'_i18n_page_{lang}'
        handler.__qualname__ = f'_i18n_page_{lang}'
        return handler

    _handler = _make_i18n_handler(_lang)
    for _route in [
        f'/{_lang}',
        f'/{_lang}/examples',
        f'/{_lang}/documentation',
        f'/{_lang}/documentation/{{path:path}}',
        f'/{_lang}/imprint_privacy',
    ]:
        _handler = ui.page(_route)(_handler)


def _documentation_detail_page(name: str, tree: ui.tree, prefix: str) -> None:
    tree.props.update(expanded=documentation.tree.ancestors(name))
    tree.update()
    if name in documentation.registry:
        documentation.render_page(documentation.registry[name])
    elif name in documentation.redirects:
        ui.navigate.to(f'{prefix}/documentation/' + documentation.redirects[name])
    else:
        ui.label(f'Documentation for "{name}" could not be found.').classes('absolute-center')


@app.get('/status')
def _status():
    return 'Ok'


# NOTE: do not reload on fly.io (see https://github.com/zauberzeug/nicegui/discussions/1720#discussioncomment-7288741)
ui.run(uvicorn_reload_includes='*.py, *.css, *.html, *.json', reload=not on_fly, reconnect_timeout=10.0)
