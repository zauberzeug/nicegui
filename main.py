#!/usr/bin/env python3
import importlib
import inspect
import logging
import os
from pathlib import Path
from typing import Awaitable, Callable, Optional
from urllib.parse import parse_qs

from fastapi import Request
from fastapi.responses import FileResponse, RedirectResponse, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.types import ASGIApp, Receive, Scope, Send

import prometheus
from nicegui import Client, app
from nicegui import globals as nicegui_globals
from nicegui import ui
from website import documentation, example_card, svg
from website.demo import bash_window, browser_window, python_window
from website.documentation_tools import create_anchor_name, element_demo, generate_class_doc
from website.search import Search
from website.star import add_star
from website.style import example_link, features, heading, link_target, section_heading, side_menu, subtitle, title

prometheus.start_monitor(app)

# session middleware is required for demo in documentation and prometheus
app.add_middleware(SessionMiddleware, secret_key=os.environ.get('NICEGUI_SECRET_KEY', ''))

app.add_static_files('/favicon', str(Path(__file__).parent / 'website' / 'favicon'))
app.add_static_files('/fonts', str(Path(__file__).parent / 'website' / 'fonts'))
app.add_static_files('/static', str(Path(__file__).parent / 'website' / 'static'))

if True:  # HACK: prevent the page from scrolling when closing a dialog (#1404)
    def on_dialog_value_change(sender, value, on_value_change=ui.dialog.on_value_change) -> None:
        ui.query('html').classes(**{'add' if value else 'remove': 'has-dialog'})
        on_value_change(sender, value)
    ui.dialog.on_value_change = on_dialog_value_change


@app.get('/logo.png')
def logo() -> FileResponse:
    return FileResponse(svg.PATH / 'logo.png', media_type='image/png')


@app.get('/logo_square.png')
def logo_square() -> FileResponse:
    return FileResponse(svg.PATH / 'logo_square.png', media_type='image/png')


@app.post('/dark_mode')
async def dark_mode(request: Request) -> None:
    app.storage.browser['dark_mode'] = (await request.json()).get('value')


@app.middleware('http')
async def redirect_reference_to_documentation(request: Request,
                                              call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    if request.url.path == '/reference':
        return RedirectResponse('/documentation')
    try:
        return await call_next(request)
    except RuntimeError as e:
        logging.error(f'Error while processing request {request.url.path}: {e}')

# NOTE In our global fly.io deployment we need to make sure that we connect back to the same instance.
fly_instance_id = os.environ.get('FLY_ALLOC_ID', 'local').split('-')[0]
nicegui_globals.socket_io_js_extra_headers['fly-force-instance-id'] = fly_instance_id  # for HTTP long polling
nicegui_globals.socket_io_js_query_params['fly_instance_id'] = fly_instance_id  # for websocket (FlyReplayMiddleware)


class FlyReplayMiddleware(BaseHTTPMiddleware):
    """Replay to correct fly.io instance.

    If the wrong instance was picked by the fly.io load balancer, we use the fly-replay header
    to repeat the request again on the right instance.

    This only works if the correct instance is provided as a query_string parameter.
    """

    def __init__(self, app: ASGIApp) -> None:
        self.app = app
        self.app_name = os.environ.get('FLY_APP_NAME')

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        query_string = scope.get('query_string', b'').decode()
        query_params = parse_qs(query_string)
        target_instance = query_params.get('fly_instance_id', [fly_instance_id])[0]

        async def send_wrapper(message):
            if target_instance != fly_instance_id and self.is_online(target_instance):
                if message['type'] == 'websocket.close':
                    # fly.io only seems to look at the fly-replay header if websocket is accepted
                    message = {'type': 'websocket.accept'}
                if 'headers' not in message:
                    message['headers'] = []
                message['headers'].append([b'fly-replay', f'instance={target_instance}'.encode()])
            await send(message)
        await self.app(scope, receive, send_wrapper)

    def is_online(self, fly_instance_id: str) -> bool:
        hostname = f'{fly_instance_id}.vm.{self.app_name}.internal'
        try:
            dns.resolver.resolve(hostname, 'AAAA')
            return True
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers, dns.resolver.Timeout):
            return False


if 'FLY_ALLOC_ID' in os.environ:
    import dns.resolver  # NOTE only import on fly where we have it installed to look up if instance is still available
    app.add_middleware(FlyReplayMiddleware)


def add_head_html() -> None:
    ui.add_head_html((Path(__file__).parent / 'website' / 'static' / 'header.html').read_text())
    ui.add_head_html(f"<style>{(Path(__file__).parent / 'website' / 'static' / 'style.css').read_text()}</style>")


def add_header(menu: Optional[ui.left_drawer] = None) -> None:
    menu_items = {
        'Installation': '/#installation',
        'Features': '/#features',
        'Demos': '/#demos',
        'Documentation': '/documentation',
        'Examples': '/#examples',
        'Why?': '/#why',
    }
    dark_mode = ui.dark_mode(value=app.storage.browser.get('dark_mode'), on_change=lambda e: ui.run_javascript(f'''
        fetch('/dark_mode', {{
            method: 'POST',
            headers: {{'Content-Type': 'application/json'}},
            body: JSON.stringify({{value: {e.value}}}),
        }});
    ''', respond=False))
    with ui.header() \
            .classes('items-center duration-200 p-0 px-4 no-wrap') \
            .style('box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1)'):
        if menu:
            ui.button(on_click=menu.toggle, icon='menu').props('flat color=white round').classes('lg:hidden')
        with ui.link(target=index_page).classes('row gap-4 items-center no-wrap mr-auto'):
            svg.face().classes('w-8 stroke-white stroke-2 max-[550px]:hidden')
            svg.word().classes('w-24')

        with ui.row().classes('max-[1050px]:hidden'):
            for title, target in menu_items.items():
                ui.link(title, target).classes(replace='text-lg text-white')

        search = Search()
        search.create_button()

        with ui.element().classes('max-[360px]:hidden'):
            ui.button(icon='dark_mode', on_click=lambda: dark_mode.set_value(None)) \
                .props('flat fab-mini color=white').bind_visibility_from(dark_mode, 'value', value=True)
            ui.button(icon='light_mode', on_click=lambda: dark_mode.set_value(True)) \
                .props('flat fab-mini color=white').bind_visibility_from(dark_mode, 'value', value=False)
            ui.button(icon='brightness_auto', on_click=lambda: dark_mode.set_value(False)) \
                .props('flat fab-mini color=white').bind_visibility_from(dark_mode, 'value', lambda mode: mode is None)

        with ui.link(target='https://discord.gg/TEpFeAaF4f').classes('max-[455px]:hidden').tooltip('Discord'):
            svg.discord().classes('fill-white scale-125 m-1')
        with ui.link(target='https://www.reddit.com/r/nicegui/').classes('max-[405px]:hidden').tooltip('Reddit'):
            svg.reddit().classes('fill-white scale-125 m-1')
        with ui.link(target='https://github.com/zauberzeug/nicegui/').classes('max-[305px]:hidden').tooltip('GitHub'):
            svg.github().classes('fill-white scale-125 m-1')

        add_star().classes('max-[490px]:hidden')

        with ui.row().classes('min-[1051px]:hidden'):
            with ui.button(icon='more_vert').props('flat color=white round'):
                with ui.menu().classes('bg-primary text-white text-lg'):
                    for title, target in menu_items.items():
                        ui.menu_item(title, on_click=lambda target=target: ui.open(target))


@ui.page('/')
async def index_page(client: Client) -> None:
    client.content.classes('p-0 gap-0')
    add_head_html()
    add_header()

    with ui.row().classes('w-full h-screen items-center gap-8 pr-4 no-wrap into-section'):
        svg.face(half=True).classes('stroke-black dark:stroke-white w-[200px] md:w-[230px] lg:w-[300px]')
        with ui.column().classes('gap-4 md:gap-8 pt-32'):
            title('Meet the *NiceGUI*.')
            subtitle('And let any browser be the frontend of your Python code.') \
                .classes('max-w-[20rem] sm:max-w-[24rem] md:max-w-[30rem]')
            ui.link(target='#about').classes('scroll-indicator')

    with ui.row().classes('''
            dark-box min-h-screen no-wrap
            justify-center items-center flex-col md:flex-row
            py-20 px-8 lg:px-16
            gap-8 sm:gap-16 md:gap-8 lg:gap-16
        '''):
        link_target('about')
        with ui.column().classes('text-white max-w-4xl'):
            heading('Interact with Python through buttons, dialogs, 3D&nbsp;scenes, plots and much more.')
            with ui.column().classes('gap-2 bold-links arrow-links text-lg'):
                ui.markdown('''
                    NiceGUI manages web development details, letting you focus on Python code for diverse applications,
                    including robotics, IoT solutions, smart home automation, and machine learning.
                    Designed to work smoothly with connected peripherals like webcams and GPIO pins in IoT setups,
                    NiceGUI streamlines the management of all your code in one place.
                    <br><br>
                    With a gentle learning curve, NiceGUI is user-friendly for beginners
                    and offers advanced customization for experienced users,
                    ensuring simplicity for basic tasks and feasibility for complex projects.
                    <br><br><br>
                    Available as
                    [PyPI package](https://pypi.org/project/nicegui/),
                    [Docker image](https://hub.docker.com/r/zauberzeug/nicegui) and on
                    [GitHub](https://github.com/zauberzeug/nicegui).
                ''')
        example_card.create()

    with ui.column().classes('w-full text-lg p-8 lg:p-16 max-w-[1600px] mx-auto'):
        link_target('installation', '-50px')
        section_heading('Installation', 'Get *started*')
        with ui.row().classes('w-full text-lg leading-tight grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-8'):
            with ui.column().classes('w-full max-w-md gap-2'):
                ui.html('<em>1.</em>').classes('text-3xl font-bold')
                ui.markdown('Create __main.py__').classes('text-lg')
                with python_window(classes='w-full h-52'):
                    ui.markdown('''
                        ```python\n
                        from nicegui import ui

                        ui.label('Hello NiceGUI!')

                        ui.run()
                        ```
                    ''')
            with ui.column().classes('w-full max-w-md gap-2'):
                ui.html('<em>2.</em>').classes('text-3xl font-bold')
                ui.markdown('Install and launch').classes('text-lg')
                with bash_window(classes='w-full h-52'):
                    ui.markdown('''
                        ```bash
                        pip3 install nicegui
                        python3 main.py
                        ```
                    ''')
            with ui.column().classes('w-full max-w-md gap-2'):
                ui.html('<em>3.</em>').classes('text-3xl font-bold')
                ui.markdown('Enjoy!').classes('text-lg')
                with browser_window(classes='w-full h-52'):
                    ui.label('Hello NiceGUI!')
        with ui.expansion('...or use Docker to run your main.py').classes('w-full gap-2 bold-links arrow-links'):
            with ui.row().classes('mt-8 w-full justify-center items-center gap-8'):
                ui.markdown('''
                    With our [multi-arch Docker image](https://hub.docker.com/repository/docker/zauberzeug/nicegui) 
                    you can start the server without installing any packages.

                    The command searches for `main.py` in in your current directory and makes the app available at http://localhost:8888.
                ''').classes('max-w-xl')
                with bash_window(classes='max-w-lg w-full h-52'):
                    ui.markdown('''
                        ```bash
                        docker run -it --rm -p 8888:8080 \\
                            -v "$PWD":/app zauberzeug/nicegui
                        ```
                    ''')

    with ui.column().classes('w-full p-8 lg:p-16 bold-links arrow-links max-w-[1600px] mx-auto'):
        link_target('features', '-50px')
        section_heading('Features', 'Code *nicely*')
        with ui.row().classes('w-full text-lg leading-tight grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-8'):
            features('swap_horiz', 'Interaction', [
                'buttons, switches, sliders, inputs, ...',
                'notifications, dialogs and menus',
                'interactive images with SVG overlays',
                'web pages and native window apps',
            ])
            features('space_dashboard', 'Layout', [
                'navigation bars, tabs, panels, ...',
                'grouping with rows, columns, grids and cards',
                'HTML and Markdown elements',
                'flex layout by default',
            ])
            features('insights', 'Visualization', [
                'charts, diagrams and tables',
                '3D scenes',
                'straight-forward data binding',
                'built-in timer for data refresh',
            ])
            features('brush', 'Styling', [
                'customizable color themes',
                'custom CSS and classes',
                'modern look with material design',
                '[Tailwind CSS](https://tailwindcss.com/) auto-completion',
            ])
            features('source', 'Coding', [
                'routing for multiple pages',
                'auto-reload on code change',
                'persistent user sessions',
                'Jupyter notebook compatibility',
            ])
            features('anchor', 'Foundation', [
                'generic [Vue](https://vuejs.org/) to Python bridge',
                'dynamic GUI through [Quasar](https://quasar.dev/)',
                'content is served with [FastAPI](http://fastapi.tiangolo.com/)',
                'Python 3.8+',
            ])

    with ui.column().classes('w-full p-8 lg:p-16 max-w-[1600px] mx-auto'):
        link_target('demos', '-50px')
        section_heading('Demos', 'Try *this*')
        with ui.column().classes('w-full'):
            documentation.create_intro()

    with ui.column().classes('dark-box p-8 lg:p-16 my-16'):
        with ui.column().classes('mx-auto items-center gap-y-8 gap-x-32 lg:flex-row'):
            with ui.column().classes('gap-1 max-lg:items-center max-lg:text-center'):
                ui.markdown('Browse through plenty of live demos.') \
                    .classes('text-white text-2xl md:text-3xl font-medium')
                ui.html('Fun-Fact: This whole website is also coded with NiceGUI.') \
                    .classes('text-white text-lg md:text-xl')
            ui.link('Documentation', '/documentation').style('color: black !important') \
                .classes('rounded-full mx-auto px-12 py-2 bg-white font-medium text-lg md:text-xl')

    with ui.column().classes('w-full p-8 lg:p-16 max-w-[1600px] mx-auto'):
        link_target('examples', '-50px')
        section_heading('In-depth examples', 'Pick your *solution*')
        with ui.row().classes('w-full text-lg leading-tight grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4'):
            example_link('Slideshow', 'implements a keyboard-controlled image slideshow')
            example_link('Authentication', 'shows how to use sessions to build a login screen')
            example_link('Modularization',
                         'provides an example of how to modularize your application into multiple files and reuse code')
            example_link('FastAPI', 'illustrates the integration of NiceGUI with an existing FastAPI application')
            example_link('Map',
                         'demonstrates wrapping the JavaScript library [leaflet](https://leafletjs.com/) '
                         'to display a map at specific locations')
            example_link('AI Interface',
                         'utilizes the [replicate](https://replicate.com) library to perform voice-to-text '
                         'transcription and generate images from prompts with Stable Diffusion')
            example_link('3D Scene', 'creates a webGL view and loads an STL mesh illuminated with a spotlight')
            example_link('Custom Vue Component', 'shows how to write and integrate a custom Vue component')
            example_link('Image Mask Overlay', 'shows how to overlay an image with a mask')
            example_link('Infinite Scroll', 'presents an infinitely scrolling image gallery')
            example_link('OpenCV Webcam', 'uses OpenCV to capture images from a webcam')
            example_link('SVG Clock', 'displays an analog clock by updating an SVG with `ui.timer`')
            example_link('Progress', 'demonstrates a progress bar for heavy computations')
            example_link('NGINX Subpath', 'shows the setup to serve an app behind a reverse proxy subpath')
            example_link('Script Executor', 'executes scripts on selection and displays the output')
            example_link('Local File Picker', 'demonstrates a dialog for selecting files locally on the server')
            example_link('Search as you type', 'using public API of thecocktaildb.com to search for cocktails')
            example_link('Menu and Tabs', 'uses Quasar to create foldable menu and tabs inside a header bar')
            example_link('Todo list', 'shows a simple todo list with checkboxes and text input')
            example_link('Trello Cards', 'shows Trello-like cards that can be dragged and dropped into columns')
            example_link('Slots', 'shows how to use scoped slots to customize Quasar elements')
            example_link('Table and slots', 'shows how to use component slots in a table')
            example_link('Single Page App', 'navigate without reloading the page')
            example_link('Chat App', 'a simple chat app')
            example_link('Chat with AI', 'a simple chat app with AI')
            example_link('SQLite Database', 'CRUD operations on a SQLite database with async-support through Tortoise ORM')
            example_link('Pandas DataFrame', 'displays an editable [pandas](https://pandas.pydata.org) DataFrame')
            example_link('Lightbox', 'A thumbnail gallery where each image can be clicked to enlarge')
            example_link('ROS2', 'Using NiceGUI as web interface for a ROS2 robot')
            example_link('Docker Image',
                         'Demonstrate using the official '
                         '[zauberzeug/nicegui](https://hub.docker.com/r/zauberzeug/nicegui) docker image')
            example_link('Download Text as File', 'providing in-memory data like strings as file download')
            example_link('Generate PDF', 'create SVG preview and PDF download from input form elements')
            example_link('Custom Binding', 'create a custom binding for a label with a bindable background color')
            example_link('Descope Auth', 'login form and user profile using [Descope](https://descope.com)')

    with ui.row().classes('dark-box min-h-screen mt-16'):
        link_target('why')
        with ui.column().classes('''
                max-w-[1600px] m-auto
                py-20 px-8 lg:px-16
                items-center justify-center no-wrap flex-col md:flex-row gap-16
            '''):
            with ui.column().classes('gap-8'):
                heading('Why?')
                with ui.column().classes('gap-2 text-xl text-white bold-links arrow-links'):
                    ui.markdown(
                        'We at '
                        '[Zauberzeug](https://zauberzeug.com) '
                        'like '
                        '[Streamlit](https://streamlit.io/) '
                        'but find it does '
                        '[too much magic](https://github.com/zauberzeug/nicegui/issues/1#issuecomment-847413651) '
                        'when it comes to state handling. '
                        'In search for an alternative nice library to write simple graphical user interfaces in Python we discovered '
                        '[JustPy](https://justpy.io/). '
                        'Although we liked the approach, it is too "low-level HTML" for our daily usage. '
                        'But it inspired us to use '
                        '[Vue](https://vuejs.org/) '
                        'and '
                        '[Quasar](https://quasar.dev/) '
                        'for the frontend.')
                    ui.markdown(
                        'We have built on top of '
                        '[FastAPI](https://fastapi.tiangolo.com/), '
                        'which itself is based on the ASGI framework '
                        '[Starlette](https://www.starlette.io/) '
                        'and the ASGI webserver '
                        '[Uvicorn](https://www.uvicorn.org/) '
                        'because of their great performance and ease of use.'
                    )
            svg.face().classes('stroke-white shrink-0 w-[200px] md:w-[300px] lg:w-[450px]')


@ui.page('/documentation')
def documentation_page() -> None:
    add_head_html()
    menu = side_menu()
    add_header(menu)
    ui.add_head_html('<style>html {scroll-behavior: auto;}</style>')
    with ui.column().classes('w-full p-8 lg:p-16 max-w-[1250px] mx-auto'):
        section_heading('Reference, Demos and more', '*NiceGUI* Documentation')
        documentation.create_full()


@ui.page('/documentation/{name}')
async def documentation_page_more(name: str, client: Client) -> None:
    if name in {'ag_grid', 'e_chart'}:
        name = name.replace('_', '')  # NOTE: "AG Grid" leads to anchor name "ag_grid", but class is `ui.aggrid`
    module = importlib.import_module(f'website.more_documentation.{name}_documentation')
    more = getattr(module, 'more', None)
    if hasattr(ui, name):
        api = getattr(ui, name)
        back_link_target = str(api.__doc__ or api.__init__.__doc__).splitlines()[0].strip()
    else:
        api = name
        back_link_target = name

    add_head_html()
    add_header()
    with side_menu() as menu:
        ui.markdown(f'[← back](/documentation#{create_anchor_name(back_link_target)})').classes('bold-links')
    with ui.column().classes('w-full p-8 lg:p-16 max-w-[1250px] mx-auto'):
        section_heading('Documentation', f'ui.*{name}*' if hasattr(ui, name) else f'*{name.replace("_", " ").title()}*')
        with menu:
            ui.markdown('**Demos**' if more else '**Demo**').classes('mt-4')
        element_demo(api)(getattr(module, 'main_demo'))
        if more:
            more()
        if inspect.isclass(api):
            with menu:
                ui.markdown('**Reference**').classes('mt-4')
            ui.markdown('## Reference').classes('mt-16')
            generate_class_doc(api)
    try:
        await client.connected()
        await ui.run_javascript(f'document.title = "{name} • NiceGUI";', respond=False)
    except TimeoutError:
        logging.warning(f'client did not connect for page /documentation/{name}')


@app.get('/status')
def status():
    """for health checks"""
    return 'Ok'


ui.run(uvicorn_reload_includes='*.py, *.css, *.html',
       # NOTE: do not reload when running on fly.io (see https://github.com/zauberzeug/nicegui/discussions/1720#discussioncomment-7288741)
       reload='FLY_ALLOC_ID' not in os.environ,
       reconnect_timeout=10.0)
