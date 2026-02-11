#!/usr/bin/env python3
import os
from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

from fastapi import Request
from fastapi.responses import PlainTextResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import Response

from nicegui import app, core, ui
from nicegui.page_arguments import RouteMatch
from website import documentation, examples_page, fly, header, imprint_privacy, main_page, rate_limits, seo, svg


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


@app.get('/robots.txt')
def _robots_txt() -> PlainTextResponse:
    return PlainTextResponse(
        f'User-agent: *\nAllow: /\n\nSitemap: {seo.SITE_URL}/sitemap.xml\n',
        media_type='text/plain',
    )


@app.get('/sitemap.xml')
def _sitemap_xml() -> Response:
    today = date.today().isoformat()
    urls = [
        ('/', '1.0', 'weekly'),
        ('/documentation', '0.9', 'weekly'),
        ('/examples', '0.8', 'monthly'),
        ('/imprint_privacy', '0.3', 'yearly'),
    ]
    for name in documentation.registry:
        if name:  # skip the overview page (already added as /documentation)
            urls.append((f'/documentation/{name}', '0.7', 'monthly'))
    xml_urls = '\n'.join(
        f'  <url>\n'
        f'    <loc>{xml_escape(seo.SITE_URL + path)}</loc>\n'
        f'    <lastmod>{today}</lastmod>\n'
        f'    <changefreq>{freq}</changefreq>\n'
        f'    <priority>{priority}</priority>\n'
        f'  </url>'
        for path, priority, freq in urls
    )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f'{xml_urls}\n'
        '</urlset>\n'
    )
    return Response(content=xml, media_type='application/xml')


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
    ui.context.client.content.classes('p-0 gap-0')
    header.add_head_html()

    with ui.left_drawer() \
            .classes('column no-wrap gap-1 bg-[#eee] dark:bg-[#1b1b1b] mt-[-20px] px-8 py-20') \
            .style('height: calc(100% + 20px) !important') as menu:
        tree = ui.tree(documentation.tree.nodes, label_key='title',
                       on_select=lambda e: ui.navigate.to(f'/documentation/{e.value}')) \
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
        '/documentation/{name}': lambda name: _documentation_detail_page(name, tree),
        '/imprint_privacy': imprint_privacy.create,
    }, show_404=False).classes('w-full')

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


def _documentation_detail_page(name: str, tree: ui.tree) -> None:
    tree.props.update(expanded=documentation.tree.ancestors(name))
    tree.update()
    if name in documentation.registry:
        documentation.render_page(documentation.registry[name])
    elif name in documentation.redirects:
        ui.navigate.to('/documentation/' + documentation.redirects[name])
    else:
        ui.status_code(404)
        ui.label(f'Documentation for "{name}" could not be found.').classes('absolute-center')


@app.get('/status')
def _status():
    return 'Ok'


# NOTE: do not reload on fly.io (see https://github.com/zauberzeug/nicegui/discussions/1720#discussioncomment-7288741)
ui.run(uvicorn_reload_includes='*.py, *.css, *.html', reload=not on_fly, reconnect_timeout=10.0)
