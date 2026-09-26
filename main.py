#!/usr/bin/env python3
import os
from pathlib import Path

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import FileResponse, PlainTextResponse, Response

from nicegui import app, core, ui
from nicegui.page_arguments import RouteMatch
from website import design as d
from website import (
    documentation,
    examples_page,
    fly,
    header,
    i18n,
    imprint_privacy,
    main_page,
    rate_limits,
    sitemap,
    svg,
)
from website.components import footer_section
from website.documentation.intersection_observer import IntersectionObserver as intersection_observer


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


@app.get('/llms.md')
@app.get('/llms.txt')
def _get_llms() -> FileResponse:
    return FileResponse(Path(__file__).parent / 'nicegui' / 'llms.md', media_type='text/markdown; charset=utf-8')


@app.get('/sitemap.xml')
def _get_sitemap() -> Response:
    return Response(sitemap.build(), media_type='application/xml')


@app.get('/robots.txt')
def _get_robots() -> PlainTextResponse:
    return PlainTextResponse(f'User-agent: *\nAllow: /\nSitemap: {sitemap.SITE_URL}/sitemap.xml\n')


@app.post('/dark_mode')
async def _post_dark_mode(request: Request) -> None:
    app.storage.browser['dark_mode'] = (await request.json()).get('value')


class custom_sub_pages(ui.sub_pages):
    def _render_page(self, match: RouteMatch) -> bool:
        if match.path == '/' and match.remaining_path:
            return False
        return super()._render_page(match)


@ui.page('/')
@ui.page('/examples')
@ui.page('/documentation')
@ui.page('/documentation/{path:path}')
@ui.page('/imprint_privacy')
def _main_page() -> None:
    _build_page('en')


def _create_language_page(language: str):
    def page() -> None:
        _build_page(language)
    page.__name__ = f'_main_page_{language}'
    return page


for _slug, _language in i18n.LANGUAGES.items():
    if _slug != 'en':
        _page = _create_language_page(_slug)
        for _route in ('', '/examples', '/documentation', '/documentation/{path:path}', '/imprint_privacy'):
            _page = ui.page(f'/{_slug}{_route}', language=_language.code)(_page)


def _build_page(language: str) -> None:
    i18n.set_language(language)
    prefix = '' if language == 'en' else f'/{language}'

    ui.context.client.content.classes('p-0 gap-0')

    header.add_head_html()
    _add_hreflang_links(language)

    with ui.left_drawer().classes(f'column no-wrap gap-1 {d.BG_FOOTER} {d.BORDER_R} p-8') as menu:
        tree = ui.tree([], label_key='title', on_select=lambda e: ui.navigate.to(f'{prefix}/documentation/{e.value}')) \
            .classes(r'w-full [&_.q-tree\_\_children]:pl-4') \
            .props('accordion no-connectors no-selection-unset icon=chevron_right color=primary')
        tree.visible = False
        spinner = ui.image('/static/loading.gif').classes('w-8 h-8 m-auto').props('no-spinner no-transition')
        d.override_markdown(spinner, '')

        @intersection_observer
        def update_tree() -> None:
            tree.props['nodes'] = documentation.tree.nodes
            tree.visible = True
            spinner.delete()
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

    main_content = custom_sub_pages({
        '/': main_page.create,
        '/examples': examples_page.create,
        '/documentation': lambda: documentation.render_page(documentation.registry['']),
        '/documentation/{name}': lambda name: _documentation_detail_page(name, tree),
        '/imprint_privacy': imprint_privacy.create,
    }, root_path=prefix or None, show_404=False).classes('w-full')
    ui.skip_link(target=main_content)

    footer_section.create()

    def _update_menu(path: str):
        if path.removeprefix(prefix).startswith('/documentation/'):
            menu_button.visible = True
            if window_state['is_desktop'] is not None:
                menu.value = window_state['is_desktop']
        else:
            menu_button.visible = False
            menu.value = False
    ui.context.client.sub_pages_router.on_path_changed(_update_menu)
    _update_menu(ui.context.client.sub_pages_router.current_path)


def _add_hreflang_links(language: str) -> None:
    """Declare the language alternates of the current page for search engines."""
    base_path = ui.context.client.request.url.path.removeprefix(f'/{language}') or '/'
    ui.add_head_html('\n'.join(f'<link rel="alternate" hreflang="{iso}" href="{sitemap.SITE_URL}{path}">'
                               for iso, path in i18n.alternates(base_path)))


def _documentation_detail_page(name: str, tree: ui.tree) -> None:
    tree.props.update(expanded=documentation.tree.ancestors(name))
    tree.update()
    if name in documentation.registry:
        documentation.render_page(documentation.registry[name])
    elif name in documentation.redirects:
        ui.navigate.to(i18n.url('/documentation/' + documentation.redirects[name]))
    else:
        ui.status_code(404)
        with ui.column().classes('w-full min-h-[50vh] items-center justify-center text-center p-16'):
            ui.label(i18n.t('Documentation for "{name}" could not be found.').format(name=name))


@app.get('/status')
def _status():
    return 'Ok'


# do not reload on fly.io (see https://github.com/zauberzeug/nicegui/discussions/1720#discussioncomment-7288741)
ui.run(uvicorn_reload_includes='*.py, *.css, *.html', reload=not on_fly, reconnect_timeout=10.0, markdown=True,
       language=i18n.LANGUAGES['en'].code)
