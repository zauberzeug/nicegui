#!/usr/bin/env python3
from pathlib import Path

import docutils.core
from pygments.formatters import HtmlFormatter

from nicegui import Client, ui
from website import reference

ACCENT_COLOR = '#428BF5'
HEADER_HEIGHT = '70px'
STATIC = Path(__file__).parent / 'website' / 'static'


def add_head_html() -> None:
    ui.add_head_html('<meta name="viewport" content="width=device-width, initial-scale=1" />')
    ui.add_head_html(docutils.core.publish_parts('', writer_name='html')['stylesheet'])
    ui.add_head_html(f'<style>{HtmlFormatter(nobackground=True).get_style_defs(".codehilite")}</style>')


@ui.page('/')
async def index_page(client: Client):
    add_head_html()
    client.content.classes(remove='q-pa-md gap-4').style('background: #f8f8f8')

    with ui.header() \
            .classes('items-center') \
            .style(f'background-color: {ACCENT_COLOR}; height: {HEADER_HEIGHT}') \
            .props('elevated'):
        ui.html((STATIC / 'happy_face.svg').read_text()).classes('w-8 stroke-white')
        ui.html((STATIC / 'nicegui_word.svg').read_text()).classes('w-24')
        with ui.row().classes('items-center ml-auto'):
            ui.link('Features').classes('text-lg').style('color: white!important')
            ui.link('Installation').classes('text-lg').style('color: white!important')
            ui.link('Documentation').classes('text-lg').style('color: white!important')
            ui.link('API Reference').classes('text-lg').style('color: white!important')
            ui.link('Docker').classes('text-lg').style('color: white!important')
            ui.link('Deployment').classes('text-lg').style('color: white!important')
            with ui.link(target='https://github.com/zauberzeug/nicegui/'):
                ui.html((STATIC / 'github.svg').read_text()).classes('fill-white scale-125 m-1')

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
            .classes('w-full q-pa-md items-center gap-32 p-32 no-wrap') \
            .style(f'height: calc(100vh - {HEADER_HEIGHT}); background: {ACCENT_COLOR}'):
        with ui.column().classes('gap-8'):
            ui.markdown('Create buttons, dialogs, markdown,\n\n3D scenes, plots and much more at ease.') \
                .style('font-size: 300%; color: white; line-height: 0.9; font-weight: 500')
            ui.label('''
                It is great for micro web apps, dashboards, robotics projects, smart home solutions
                and similar use cases. You can also use it in development, for example when
                tweaking/configuring a machine learning algorithm or tuning motor controllers.
                NiceGUl is available as PyPl package, Docker image and on GitHub
            ''') \
                .style('font-size: 150%; color: white')
        with ui.card().style('min-width: 350px; height: 500px'):
            ui.label('Demo')

    with ui.row().classes('w-full q-pa-md'):
        reference.create_intro()


@ui.page('/reference')
def reference_page():
    add_head_html()
    reference.create_full()


ui.run()
