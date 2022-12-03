#!/usr/bin/env python3
from pathlib import Path

import docutils.core
from pygments.formatters import HtmlFormatter

from nicegui import Client, ui
from website import demo_card, reference

ACCENT_COLOR = '#428BF5'
HEADER_HEIGHT = '70px'
STATIC = Path(__file__).parent / 'website' / 'static'

ui.add_static_files('/favicon', Path(__file__).parent / 'website' / 'favicon')


def add_head_html() -> None:
    ui.add_head_html('<meta name="viewport" content="width=device-width, initial-scale=1" />')
    ui.add_head_html(docutils.core.publish_parts('', writer_name='html')['stylesheet'])
    ui.add_head_html(f'<style>{HtmlFormatter(nobackground=True).get_style_defs(".codehilite")}</style>')
    ui.add_head_html('''
        <link rel="apple-touch-icon" sizes="180x180" href="favicon/apple-touch-icon.png">
        <link rel="icon" type="image/png" sizes="32x32" href="favicon/favicon-32x32.png">
        <link rel="icon" type="image/png" sizes="16x16" href="favicon/favicon-16x16.png">
        <link rel="manifest" href="favicon/site.webmanifest">
        <link rel="mask-icon" href="favicon/safari-pinned-tab.svg" color="#000000">
        <link rel="shortcut icon" href="favicon/favicon.ico">
        <meta name="msapplication-TileColor" content="#ffffff">
        <meta name="msapplication-config" content="favicon/browserconfig.xml">
        <meta name="theme-color" content="#ffffff">
    ''')  # https://realfavicongenerator.net/
    ui.add_head_html(r'''
        <style>
        body {
            background-color: #f8f8f8;
        }
        </style>
    ''')


def add_header() -> None:
    with ui.header() \
            .classes('items-center') \
            .style(f'background-color: {ACCENT_COLOR}; height: {HEADER_HEIGHT}; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1)'):
        ui.html((STATIC / 'happy_face.svg').read_text()).classes('w-8 stroke-white')
        with ui.link(target=index_page):
            ui.html((STATIC / 'nicegui_word.svg').read_text()).classes('w-24')
        with ui.row().classes('items-center ml-auto'):
            ui.link('Features').classes('text-lg').style('color: white!important')
            ui.link('Installation').classes('text-lg').style('color: white!important')
            ui.link('Documentation').classes('text-lg').style('color: white!important')
            ui.link('API Reference', reference_page).classes('text-lg').style('color: white!important')
            ui.link('Docker').classes('text-lg').style('color: white!important')
            ui.link('Deployment').classes('text-lg').style('color: white!important')
            with ui.link(target='https://github.com/zauberzeug/nicegui/'):
                ui.html((STATIC / 'github.svg').read_text()).classes('fill-white scale-125 m-1')


@ui.page('/')
async def index_page(client: Client):
    client.content.classes(remove='q-pa-md gap-4')
    add_head_html()
    add_header()

    with ui.row() \
            .classes('w-full q-pa-md items-center gap-12 no-wrap') \
            .style(f'height: calc(100vh - {HEADER_HEIGHT}); transform: translateX(-250px)'):
        ui.html((STATIC / 'happy_face.svg').read_text()).classes('stroke-black').style('width: 500px')
        with ui.column().classes('gap-8'):
            ui.markdown('The NiceGUI you really\n\nneed in your life.') \
                .style('font-size: 400%; line-height: 0.9; font-weight: 500')
            ui.markdown('An easy-to-use Python-based UI framework\n\nwhich shows up in your web browser.') \
                .style('font-size: 200%; line-height: 0.9')

    with ui.row() \
            .classes('w-full q-pa-md items-center gap-28 p-32 no-wrap') \
            .style(f'height: calc(100vh - {HEADER_HEIGHT}); background: {ACCENT_COLOR}'):
        with ui.column().classes('gap-8'):
            ui.markdown('Create buttons, dialogs, markdown,\n\n3D scenes, plots and much more at ease.') \
                .style('font-size: 300%; color: white; line-height: 0.9; font-weight: 500')
            ui.label('''
                It is great for micro web apps, dashboards, robotics projects, smart home solutions
                and similar use cases. You can also use it in development, for example when
                tweaking/configuring a machine learning algorithm or tuning motor controllers.
                NiceGUl is available as PyPl package, Docker image and on GitHub
            ''').style('font-size: 150%; color: white')
        with ui.row().style('filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.1))'):
            with ui.card().classes('no-shadow') \
                    .style(f'min-width: 360px; height: 380px; clip-path: polygon(0 0, 100% 0, 100% 90%, 0 100%)'):
                demo_card.create_content()

    with ui.row().classes('w-full q-pa-md'):
        reference.create_intro()

    with ui.row() \
            .classes('w-full items-center gap-28 px-32 py-16 no-wrap') \
            .style(f'background: {ACCENT_COLOR}'):
        with ui.column().classes('gap-4'):
            ui.markdown('Go to the API reference to see a ton of live examples') \
                .style('font-size: 220%; color: white; line-height: 0.9; font-weight: 500')
            ui.label('The whole content of https://nicegui.io/ is implemented with NiceGUI itself.') \
                .style('font-size: 150%; color: white')
        ui.link('API reference', '/reference') \
            .classes('rounded-full px-12 py-2 text-xl text-bold bg-white')


@ui.page('/reference')
def reference_page():
    add_head_html()
    add_header()
    reference.create_full()


ui.run()
