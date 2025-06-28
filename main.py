#!/usr/bin/env python3
import os
from pathlib import Path
from typing import Optional

from fastapi import HTTPException, Request
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware

from nicegui import app, ui
from website import anti_scroll_hack, documentation, fly, header, imprint_privacy, main_page, svg

# session middleware is required for demo in documentation
app.add_middleware(SessionMiddleware, secret_key=os.environ.get('NICEGUI_SECRET_KEY', ''))

on_fly = fly.setup()
anti_scroll_hack.setup()

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


@ui.page('/')
@ui.page('{path:path}')
def _main_page() -> None:
    ui.context.client.content.classes('p-0 gap-0')
    header.add_head_html()
    with ui.left_drawer() \
        .classes('column no-wrap gap-1 bg-[#eee] dark:bg-[#1b1b1b] mt-[-20px] px-8 py-20') \
            .style('height: calc(100% + 20px) !important') as menu:
        tree = ui.tree(documentation.tree.nodes, label_key='title').classes('w-full').props('accordion no-connectors')
        tree.add_slot('default-header', '''
                <a :href="'/documentation/' + props.node.id" onclick="event.stopPropagation()">{{ props.node.title }}</a>
            ''')
    header.add_header(menu)

    window_state = {'is_desktop': None}
    ui.on('is_desktop', lambda v: window_state.update(is_desktop=v.args))
    ui.add_head_html('''<script>
            const mq = window.matchMedia('(min-width: 1024px)')
            mq.addEventListener('change', e => emitEvent('is_desktop', e.matches))
            window.addEventListener('load', () => {
                emitEvent('is_desktop', mq.matches)
            })
        </script>''')

    def _show_menu(path: str) -> bool:
        if path.startswith('/documentation/'):
            return window_state['is_desktop'] if window_state['is_desktop'] is not None else menu.value
        else:
            return False

    ui.sub_pages({
        '/': main_page.create,
        '/documentation': _documentation_page,
        '/documentation/{name}': lambda name: _documentation_detail_page(name, menu, tree),
        '/imprint_privacy': imprint_privacy.create,
    }).classes('mx-auto').bind_path_to(menu, 'value', _show_menu)


def _documentation_page() -> None:
    documentation.render_page(documentation.registry[''])


def _documentation_detail_page(name: str, menu: ui.left_drawer, tree: ui.tree) -> Optional[RedirectResponse]:
    tree.expand(documentation.rendering._ancestor_nodes(name))
    ui.run_javascript(f'''
        Array.from(getHtmlElement({tree.id}).getElementsByTagName("a"))
            .find(el => el.innerText.trim() === "{(documentation.registry[name].parts[0].title or '').replace('*', '')}")
            .scrollIntoView({{block: "center"}});
    ''')

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
