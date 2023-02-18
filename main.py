#!/usr/bin/env python3

if True:
    # increasing max decode packets to be able to transfer images
    # see https://github.com/miguelgrinberg/python-engineio/issues/142
    from engineio.payload import Payload
    Payload.max_decode_packets = 500

import os
from pathlib import Path

from fastapi.responses import FileResponse
from pygments.formatters import HtmlFormatter

import prometheus
from nicegui import Client, app
from nicegui import globals as nicegui_globals
from nicegui import ui
from website import demo_card, reference, svg
from website.example import bash_window, browser_window, python_window
from website.star import add_star
from website.style import example_link, features, heading, link_target, section_heading, subtitle, title

prometheus.start_monitor(app)

app.add_static_files('/favicon', str(Path(__file__).parent / 'website' / 'favicon'))
app.add_static_files('/fonts', str(Path(__file__).parent / 'website' / 'fonts'))


@app.get('/logo.png')
def logo():
    return FileResponse(svg.PATH / 'logo.png', media_type='image/png')


# NOTE in our global fly.io deployment we need to make sure that the websocket connects back to the same instance
fly_instance_id = os.environ.get('FLY_ALLOC_ID', '').split('-')[0]
if fly_instance_id:
    nicegui_globals.socket_io_js_extra_headers['fly-force-instance-id'] = fly_instance_id


def add_head_html() -> None:
    ui.add_head_html((Path(__file__).parent / 'website' / 'static' / 'header.html').read_text())
    ui.add_head_html(f'<style>{HtmlFormatter(nobackground=True).get_style_defs(".codehilite")}</style>')
    ui.add_head_html(f"<style>{(Path(__file__).parent / 'website' / 'static' / 'style.css').read_text()}</style>")


def add_header() -> None:
    menu_items = {
        'Features': '/#features',
        'Installation': '/#installation',
        'Examples': '/#examples',
        'API Reference': '/reference',
        'Demos': '/#demos',
        'Why?': '/#why',
    }
    with ui.header() \
            .classes('items-center duration-200 p-0 px-4 no-wrap') \
            .style('box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1)'):
        with ui.link(target=index_page).classes('row gap-4 items-center no-wrap mr-auto'):
            svg.face().classes('w-8 stroke-white stroke-2')
            svg.word().classes('w-24')
        with ui.row().classes('lg:hidden'):
            with ui.menu().classes('bg-primary text-white text-lg') as menu:
                for title, target in menu_items.items():
                    ui.menu_item(title, on_click=lambda _, target=target: ui.open(target))
            ui.button(on_click=menu.open).props('flat color=white icon=menu')
        with ui.row().classes('max-lg:hidden'):
            for title, target in menu_items.items():
                ui.link(title, target).classes(replace='text-lg text-white')
        with ui.link(target='https://github.com/zauberzeug/nicegui/'):
            svg.github().classes('fill-white scale-125 m-1')
        add_star()


@ui.page('/')
async def index_page(client: Client):
    client.content.classes(remove='q-pa-md gap-4')
    add_head_html()
    add_header()

    with ui.row().classes('w-full h-screen items-center gap-8 pr-4 no-wrap into-section'):
        svg.face(half=True).classes('stroke-black w-[200px] md:w-[230px] lg:w-[300px]')
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
                ui.markdown(
                    'NiceGUI handles all the web development details for you. '
                    'So you can focus on writing Python code. '
                    'Anything from short scripts and dashboards to full robotics projects, IoT solutions, '
                    'smart home automations and machine learning projects can benefit from having all code in one place.'
                )
                ui.markdown(
                    'Available as '
                    '[PyPI package](https://pypi.org/project/nicegui/), '
                    '[Docker image](https://hub.docker.com/r/zauberzeug/nicegui) and on '
                    '[GitHub](https://github.com/zauberzeug/nicegui).')
        demo_card.create()

    with ui.column().classes('w-full p-8 lg:p-16 bold-links arrow-links max-w-[1600px] mx-auto'):
        link_target('features', '-50px')
        section_heading('Features', 'Code *nicely*')
        with ui.row().classes('w-full text-lg leading-tight grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-8'):
            features('swap_horiz', 'Interaction', [
                'buttons, switches, sliders, inputs, ...',
                'notifications, dialogs and menus',
                'keyboard input',
                'on-screen joystick',
            ])
            features('space_dashboard', 'Layout', [
                'navigation bars, tabs, panels, ...',
                'grouping with rows, columns and cards',
                'HTML and Markdown elements',
                'flex layout by default',
            ])
            features('insights', 'Visualization', [
                'charts, diagrams and tables',
                '3D scenes',
                'progress bars',
                'built-in timer for data refresh',
            ])
            features('brush', 'Styling', [
                'customizable color themes',
                'custom CSS and classes',
                'modern look with material design',
                'built-in [Tailwind](https://tailwindcss.com/) support',
            ])
            features('source', 'Coding', [
                'live-cycle events',
                'implicit reload on code change',
                'straight-forward data binding',
                'execute javascript from Python',
            ])
            features('anchor', 'Foundation', [
                'generic [Vue](https://vuejs.org/) to Python bridge',
                'dynamic GUI through [Quasar](https://quasar.dev/)',
                'content is served with [FastAPI](http://fastapi.tiangolo.com/)',
                'Python 3.7+',
            ])

    with ui.column().classes('w-full p-8 lg:p-16 max-w-[1600px] mx-auto'):
        link_target('installation', '-50px')
        section_heading('Installation', 'Get *started*')
        with ui.row().classes('w-full text-lg leading-tight grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-8'):
            with ui.column().classes('w-full max-w-md gap-2'):
                ui.html('<em>1.</em>').classes('text-3xl font-bold')
                ui.markdown('Create __main.py__').classes('text-lg')
                with python_window(classes='w-full h-52'):
                    ui.markdown('''```python\n
from nicegui import ui

ui.label('Hello NiceGUI!')

ui.run()
```''')
            with ui.column().classes('w-full max-w-md gap-2'):
                ui.html('<em>2.</em>').classes('text-3xl font-bold')
                ui.markdown('Install and launch').classes('text-lg')
                with bash_window(classes='w-full h-52'):
                    ui.markdown('```bash\npip3 install nicegui\npython3 main.py\n```')
            with ui.column().classes('w-full max-w-md gap-2'):
                ui.html('<em>3.</em>').classes('text-3xl font-bold')
                ui.markdown('Enjoy!').classes('text-lg')
                with browser_window(classes='w-full h-52'):
                    ui.label('Hello NiceGUI!')
        with ui.expansion('... or use Docker to run your main.py').classes('w-full gap-2 arrow-links'):
            with ui.row().classes('mt-8 w-full text-lg justify-center items-center gap-8'):
                ui.markdown('''
With our [multi-arch Docker image](https://hub.docker.com/repository/docker/zauberzeug/nicegui) you can start the server at http://localhost:8888.
It searches for `main.py` in in your current directory.
''').classes('max-w-xl')
                with bash_window(classes='max-w-lg w-full h-52'):
                    ui.markdown('```bash\n'
                                'docker run -it --rm -p 8000:8000 \\\n -v "$PWD":/app zauberzeug/nicegui\n'
                                '```')

    with ui.column().classes('w-full p-8 lg:p-16 max-w-[1600px] mx-auto'):
        link_target('examples', '-50px')
        section_heading('Examples', 'Try *this*')
        with ui.column().classes('w-full'):
            reference.create_intro()

    with ui.column().classes('dark-box p-8 lg:p-16 my-16'):
        with ui.column().classes('mx-auto items-center gap-y-8 gap-x-32 lg:flex-row'):
            with ui.column().classes('gap-1 max-lg:items-center max-lg:text-center'):
                ui.markdown('Browse through plenty of live examples.') \
                    .classes('text-white text-2xl md:text-3xl font-medium')
                ui.html('Fun-Fact: This whole website is also coded with NiceGUI.') \
                    .classes('text-white text-lg md:text-xl')
            ui.link('API reference', '/reference') \
                .classes('rounded-full mx-auto px-12 py-2 text-white bg-white font-medium text-lg md:text-xl')

    with ui.column().classes('w-full p-8 lg:p-16 max-w-[1600px] mx-auto'):
        link_target('demos', '-50px')
        section_heading('In-depth demonstrations', 'Pick your *solution*')
        with ui.row().classes('w-full text-lg leading-tight grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4'):
            example_link('Slideshow', 'implements a keyboard-controlled image slideshow')
            example_link('Authentication', 'shows how to use sessions to build a login screen')
            example_link(
                'Modularization',
                'provides an example of how to modularize your application into multiple files and reuse code')
            example_link(
                'FastAPI',
                'illustrates the integration of NiceGUI with an existing FastAPI application')
            example_link(
                'Map',
                'demonstrates wrapping the JavaScript library [leaflet](https://leafletjs.com/) to display a map at specific locations')
            example_link(
                'AI Interface',
                'utilizes the [replicate](https://replicate.com) library to perform voice-to-text transcription and generate images from prompts with Stable Diffusion')
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

    with ui.row().classes('bg-primary w-full min-h-screen mt-16'):
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


@ui.page('/reference')
def reference_page():
    add_head_html()
    add_header()
    menu = ui.left_drawer() \
        .classes('column no-wrap gap-1 bg-[#eee] mt-[-20px] px-8 py-20').style('height: calc(100% + 20px) !important')
    ui.add_head_html('<style>html {scroll-behavior: auto;}</style>')
    with ui.column().classes('w-full p-8 lg:p-16 max-w-[1250px] mx-auto'):
        section_heading('Documentation and Examples', '*API* Reference')
        ui.markdown(
            'This is the API reference for NiceGUI >= 1.0. '
            'Documentation for older versions can be found at [https://0.9.nicegui.io/](https://0.9.nicegui.io/reference).'
        ).classes('bold-links arrow-links')
        reference.create_full(menu)


ui.run(uvicorn_reload_includes='*.py, *.css, *.html')
