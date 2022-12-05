#!/usr/bin/env python3
from pathlib import Path

import docutils.core
from pygments.formatters import HtmlFormatter

from nicegui import Client, ui
from website import demo_card, reference
from website.constants import ACCENT_COLOR, HEADER_HEIGHT, STATIC
from website.example import bash_window, browser_window, python_window

ui.add_static_files('/favicon', Path(__file__).parent / 'website' / 'favicon')


def add_head_html() -> None:
    ui.add_head_html('<meta name="viewport" content="width=device-width, initial-scale=1" />')
    ui.add_head_html(docutils.core.publish_parts('', writer_name='html')['stylesheet'])
    ui.add_head_html(f'<style>{HtmlFormatter(nobackground=True).get_style_defs(".codehilite")}</style>')
    ui.add_head_html('''
        <link rel="apple-touch-icon" sizes="180x180" href="/favicon/apple-touch-icon.png">
        <link rel="icon" type="image/png" sizes="32x32" href="/favicon/favicon-32x32.png">
        <link rel="icon" type="image/png" sizes="16x16" href="/favicon/favicon-16x16.png">
        <link rel="manifest" href="/favicon/site.webmanifest">
        <link rel="mask-icon" href="/favicon/safari-pinned-tab.svg" color="#000000">
        <link rel="shortcut icon" href="/favicon/favicon.ico">
        <meta name="msapplication-TileColor" content="#ffffff">
        <meta name="msapplication-config" content="/favicon/browserconfig.xml">
        <meta name="theme-color" content="#ffffff">
    ''')  # https://realfavicongenerator.net/
    ui.add_head_html(f'''
        <style>
        html {{
            scroll-behavior: smooth;
        }}
        body {{
            background-color: #f8f8f8;
        }}
        em {{
            font-style: normal;
            color: {ACCENT_COLOR};
        }}
        a:hover {{
            opacity: 0.9;
        }}
        </style>
    ''')
    ui.add_head_html(f'''
    <style>
    .q-header {{
        height: calc({HEADER_HEIGHT} + 20px);
        background-color: {ACCENT_COLOR};
    }}
    .q-header.fade {{
        height: {HEADER_HEIGHT};
        background-color: {ACCENT_COLOR}d0;
        backdrop-filter: blur(5px);
    }}
    </style>
    <script>
    window.onscroll = () => {{
        const header = document.querySelector(".q-header");
        if (document.documentElement.scrollTop > 50)
            header.classList.add("fade");
        else
            header.classList.remove("fade");
    }};
    </script>
    ''')


def add_header() -> None:
    with ui.header() \
            .classes('items-center duration-200 px-4', remove='q-pa-md') \
            .style('box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1)'):
        with ui.link(target=index_page).classes('row gap-4 items-center'):
            ui.html((STATIC / 'happy_face.svg').read_text()).classes('w-8 stroke-white')
            ui.html((STATIC / 'nicegui_word.svg').read_text()).classes('w-24')
        with ui.row().classes('items-center ml-auto'):
            ui.link('Features', '/#features').classes(replace='text-lg text-white')
            ui.link('Installation', '/#installation').classes(replace='text-lg text-white')
            ui.link('Examples', '/#examples').classes(replace='text-lg text-white')
            ui.link('API Reference', reference_page).classes(replace='text-lg text-white')
            ui.link('Demos', '/#demos').classes(replace='text-lg text-white')
            ui.link('Why?', '/#why').classes(replace='text-lg text-white')
            with ui.link(target='https://github.com/zauberzeug/nicegui/'):
                ui.html((STATIC / 'github.svg').read_text()).classes('fill-white scale-125 m-1')


@ui.page('/')
async def index_page(client: Client):
    client.content.classes(remove='q-pa-md gap-4')
    add_head_html()
    add_header()

    with ui.row() \
            .classes('w-full h-screen q-pa-md items-center gap-12 no-wrap') \
            .style(f'transform: translateX(-250px)'):
        ui.html((STATIC / 'happy_face.svg').read_text()).classes('stroke-black').style('width: 500px')
        with ui.column().classes('gap-8'):
            ui.html('Meet the <em>NiceGUI</em>.') \
                .style('font-size: 400%; line-height: 0.9; font-weight: 500')
            ui.markdown('And let any browser be the frontend\n\nof your Python code.') \
                .style('font-size: 200%; line-height: 0.9')
            with ui.column().classes('q-mt-md'):
                ui.icon('keyboard_arrow_down').classes('text-4xl text-grey-5').style('margin: 0 0 -1.4em 0.32em')
                ui.icon('keyboard_arrow_down').classes('text-6xl text-black')
                ui.icon('keyboard_arrow_down').classes('text-4xl text-grey-5').style('margin: -1.3em 0 0 0.32em')

    with ui.row() \
            .classes('w-full h-screen q-pa-md items-center gap-28 p-32 no-wrap') \
            .style(f'background: {ACCENT_COLOR}'):
        with ui.column().classes('gap-6'):
            ui.markdown('Interact with Python through buttons, dialogs, 3D scenes, plots and much more.') \
                .style('font-size: 300%; color: white; line-height: 0.9; font-weight: 500').classes('mb-4')
            ui.label('''
                NiceGUI handles all the web development details for you.
                So you can focus on writing Python code.
                Anything from short scripts and dashboards to full robotics projects, IoT solutions, 
                smart home automations and machine learning projects can benefit from having all code in one place.
                
            ''').style('font-size: 150%; color: white').classes('leading-tight')
            with ui.row().style('font-size: 150%; color: white').classes('leading-tight gap-2'):
                ui.html('''
                    Available as
                    <a href="https://pypi.org/project/nicegui/"><strong>PyPI package</strong><span class="material-icons">north_east</span></a>,
                    <a href="https://hub.docker.com/r/zauberzeug/nicegui"><strong>Docker image</strong><span class="material-icons">north_east</span></a> and on
                    <a href="https://github.com/zauberzeug/nicegui"><strong>GitHub</strong><span class="material-icons">north_east</span></a>.
                ''')

        demo_card.create()

    ui.link_target('features').style(f'position: relative; top: -{HEADER_HEIGHT}')
    with ui.column().classes('w-full q-pa-xl q-mb-xl'):
        ui.label('Features').classes('text-bold text-lg')
        ui.html('Code <em>nicely</em>') \
            .style('font-size: 300%; font-weight: 500; margin-top: -20px')
        with ui.row().classes('w-full no-wrap text-lg leading-tight justify-between q-mb-xl'):
            with ui.column().classes('gap-1 col-3'):
                ui.icon('swap_horiz').classes('text-5xl q-mb-md text-primary opacity-80')
                ui.label('Interaction').classes('text-bold mb-4')
                ui.markdown('- buttons, switches, slider, input, ...')
                ui.markdown('- notifications, dialogs and menus')
                ui.markdown('- keyboard input')
                ui.markdown('- on-screen joystick')
            with ui.column().classes('gap-1 col-3'):
                ui.icon('space_dashboard').classes('text-5xl q-mb-md text-primary opacity-80')
                ui.label('Layout').classes('text-bold mb-4')
                ui.markdown('- navigation bars, tabs, panels, ...')
                ui.markdown('- grouping with rows, columns and cards')
                ui.markdown('- HTML and markdown elements')
                ui.markdown('- flex layout by default')
            with ui.column().classes('gap-1 col-3'):
                ui.icon('insights').classes('text-5xl q-mb-md text-primary')
                ui.label('Visualization').classes('text-bold mb-4')
                ui.markdown('- charts, diagrams and tables')
                ui.markdown('- 3D scenes')
                ui.markdown('- progress bars')
                ui.markdown('- built-in timer for data refresh')
        with ui.row().classes('w-full no-wrap text-lg leading-tight justify-between'):
            with ui.column().classes('gap-1 col-3'):
                ui.icon('brush').classes('text-5xl q-mb-xs text-primary opacity-80')
                ui.label('Styling').classes('text-bold mb-4')
                ui.markdown('- customizable color themes')
                ui.markdown('- add custom css and classes')
                ui.markdown('- modern look with material design')
            with ui.column().classes('gap-1 col-3'):
                ui.icon('source').classes('text-5xl q-mb-md text-primary opacity-80')
                ui.label('Coding').classes('text-bold mb-4')
                ui.markdown('- live-cycle events')
                ui.markdown('- implicit reload on code change')
                ui.markdown('- straight-forward data binding')
                ui.markdown('- execute javascript from Python')
            with ui.column().classes('gap-1 col-3'):
                ui.icon('anchor').classes('text-5xl q-mb-md text-primary opacity-80')
                ui.label('Foundation').classes('text-bold mb-4')
                ui.markdown('- generic Vue to Python bridge')
                ui.markdown('- dynamic GUI through Quasar')
                ui.markdown('- content is served with FastAPI')
                ui.markdown('- Python 3.7 - 3.11')

    ui.link_target('installation').style(f'position: relative; top: -{HEADER_HEIGHT}')
    with ui.column().classes('w-full q-pa-xl q-mb-xl'):
        ui.label('Installation').classes('text-bold text-lg')
        ui.html('Get <em>started</em>') \
            .style('font-size: 300%; font-weight: 500; margin-top: -20px')
        with ui.row().classes('w-full no-wrap text-lg leading-tight'):
            with ui.column().classes('w-1/3 gap-2'):
                ui.html('<em>1.</em>').classes('text-3xl text-bold')
                ui.markdown('Create __main.py__').classes('text-lg')
                with python_window().classes('w-full h-52'):
                    ui.markdown('''```python\n
from nicegui import ui

ui.label('Hello NiceGUI!')

ui.run()
```''')
            with ui.column().classes('w-1/3 gap-2'):
                ui.html('<em>2.</em>').classes('text-3xl text-bold')
                ui.markdown('Install and launch').classes('text-lg')
                with bash_window().classes('w-full h-52'):
                    ui.markdown('```bash\npip3 install nicegui\npython3 main.py\n```')
            with ui.column().classes('w-1/3 gap-2'):
                ui.html('<em>3.</em>').classes('text-3xl text-bold')
                ui.markdown('Enjoy').classes('text-lg')
                with browser_window().classes('w-full h-52'):
                    ui.label('Hello NiceGUI!')

    ui.link_target('examples').style(f'position: relative; top: -{HEADER_HEIGHT}')
    with ui.column().classes('w-full q-pa-xl q-mb-xl'):
        ui.label('Examples').classes('text-bold text-lg')
        ui.html('Try <em>this</em>') \
            .style('font-size: 300%; font-weight: 500; margin-top: -20px')
        reference.create_intro()

    with ui.row() \
            .classes('w-full items-center gap-28 px-32 py-16 no-wrap') \
            .style(f'background: {ACCENT_COLOR}'):
        with ui.column().classes('gap-4'):
            ui.markdown('Browse through tons of live examples.') \
                .style('font-size: 220%; color: white; line-height: 0.9; font-weight: 500')
            ui.html('Fun-Fact: This whole website is also coded with NiceGUI.') \
                .style('font-size: 150%; color: white')
        ui.link('API reference', '/reference') \
            .classes('rounded-full mx-auto px-12 py-2 text-xl text-bold bg-white')

    ui.link_target('demos').style(f'position: relative; top: -{HEADER_HEIGHT}')
    with ui.column().classes('w-full q-pa-xl q-mb-xl'):
        ui.label('In-depth demonstrations').classes('text-bold text-lg')
        ui.html('Pick your <em>solution</em>') \
            .style('font-size: 300%; font-weight: 500; margin-top: -20px')
        with ui.row().classes('w-full no-wrap text-lg leading-tight'):
            with ui.column().classes('w-1/3'):
                example_link('Slideshow', 'implements a keyboard-controlled image slideshow')
                example_link('Authentication', 'shows how to use sessions to build a login screen')
                example_link(
                    'Modularization',
                    'provides an example of how to modularize your application into multiple files and reuse code')
                example_link(
                    'FastAPI',
                    'illustrates the integration of NiceGUI with an existing FastAPI application')
            with ui.column().classes('w-1/3'):
                example_link(
                    'Map',
                    'demonstrates wrapping the JavaScript library leaflet to display a map at specific locations')
                example_link(
                    'AI Interface',
                    'utilizes the great [replicate](https://replicate.com) library to perform voice-to-text transcription and generate images from prompts with Stable Diffusion')
                example_link('3D Scene', 'creates a webGL view and loads an STL mesh illuminated with a spotlight')
            with ui.column().classes('w-1/3'):
                example_link('Custom Vue Component', 'shows how to write and integrate a custom vue component')
                example_link('Image Mask Overlay', 'shows how to overlay an image with a mask')
                example_link('Infinite Scroll', 'presents an infinitely scrolling image gallery')

    ui.link_target('why')
    with ui.row() \
            .classes('w-full h-screen q-pa-md items-center gap-28 p-32 no-wrap') \
            .style(f'background: {ACCENT_COLOR}'):
        with ui.column().classes('gap-6'):
            ui.markdown('Why?') \
                .style('font-size: 300%; color: white; line-height: 0.9; font-weight: 500').classes('mb-4')
            ui.html('''
                We like
                <strong><a href="https://streamlit.io/">Streamlit</a></strong>
                but find it does
                <strong><a href="https://github.com/zauberzeug/nicegui/issues/1#issuecomment-847413651">too much magic</a></strong>
                when it comes to state handling.
                In search for an alternative nice library to write simple graphical user interfaces in Python we discovered
                <strong><a href="https://justpy.io/">JustPy</a></strong>.
                Although we liked the approach, it is too "low-level HTML" for our daily usage.
                But it inspired us to use
                <strong><a href="https://vuejs.org/">Vue</a></strong>
                and
                <strong><a href="https://quasar.dev/">Quasar</a></strong>
                for the frontend.<br/>

                We have build on top of
                <strong><a href="https://fastapi.tiangolo.com/">FastAPI</a></strong>,
                which itself is based on the ASGI framework
                <strong><a href="https://www.starlette.io/">Starlette</a></strong>,
                and the ASGI webserver
                <strong><a href="https://www.uvicorn.org/">Uvicorn</a></strong>
                because of their great performance and ease of use.
            ''').style('font-size: 150%; color: white').classes('leading-tight')

        ui.html((STATIC / 'happy_face.svg').read_text()).classes('stroke-white').style('width: 1500px')


def example_link(title: str, description: str) -> None:
    name = title.lower().replace(' ', '_')
    with ui.column().classes('gap-0'):
        with ui.link(target=f'https://github.com/zauberzeug/nicegui/tree/main/examples/{name}/main.py'):
            ui.label(title).classes(replace='text-black text-bold')
            ui.markdown(description).classes(replace='text-black')


@ui.page('/reference')
def reference_page():
    add_head_html()
    add_header()
    reference.create_full()


ui.run()
