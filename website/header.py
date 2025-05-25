import os
from pathlib import Path
from typing import Optional

from nicegui import app, ui

from . import svg
from .search import Search
from .star import add_star

HEADER_HTML = (Path(__file__).parent / 'static' / 'header.html').read_text(encoding='utf-8')
STYLE_CSS = (Path(__file__).parent / 'static' / 'style.css').read_text(encoding='utf-8')


def add_head_html() -> None:
    """Add the code from header.html and reference style.css."""
    ui.add_head_html(HEADER_HTML + f'<style>{STYLE_CSS}</style>')
    if os.environ.get('ENABLE_ANALYTICS', 'false').lower() == 'true':
        ui.add_head_html(
            '<script defer data-domain="nicegui.io" src="https://plausible.io/js/script.hash.outbound-links.js">'
            '</script>'
        )


def add_header(menu: Optional[ui.left_drawer] = None) -> None:
    """Create the page header."""
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
    '''))
    with ui.header() \
            .classes('items-center duration-200 p-0 px-4 no-wrap') \
            .style('box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1)'):
        if menu:
            ui.button(on_click=menu.toggle, icon='menu').props('flat color=white round').classes('lg:hidden')
        with ui.link(target='/').classes('row gap-4 items-center no-wrap mr-auto'):
            svg.face().classes('w-8 stroke-white stroke-2 max-[610px]:hidden')
            svg.word().classes('w-24')

        with ui.row().classes('max-[1050px]:hidden'):
            for title_, target in menu_items.items():
                ui.link(title_, target).classes(replace='text-lg text-white')

        search = Search()
        search.create_button()

        with ui.element().classes('max-[420px]:hidden').tooltip('Cycle theme mode through dark, light, and system/auto.'):
            ui.button(icon='dark_mode', on_click=lambda: dark_mode.set_value(None)) \
                .props('flat fab-mini color=white').bind_visibility_from(dark_mode, 'value', value=True)
            ui.button(icon='light_mode', on_click=lambda: dark_mode.set_value(True)) \
                .props('flat fab-mini color=white').bind_visibility_from(dark_mode, 'value', value=False)
            ui.button(icon='brightness_auto', on_click=lambda: dark_mode.set_value(False)) \
                .props('flat fab-mini color=white').bind_visibility_from(dark_mode, 'value', lambda mode: mode is None)

        with ui.link(target='https://discord.gg/TEpFeAaF4f').classes('max-[515px]:hidden').tooltip('Discord'):
            svg.discord().classes('fill-white scale-125 m-1')
        with ui.link(target='https://www.reddit.com/r/nicegui/').classes('max-[465px]:hidden').tooltip('Reddit'):
            svg.reddit().classes('fill-white scale-125 m-1')
        with ui.link(target='https://github.com/zauberzeug/nicegui/').classes('max-[365px]:hidden').tooltip('GitHub'):
            svg.github().classes('fill-white scale-125 m-1')

        add_star().classes('max-[550px]:hidden')

        with ui.row().classes('min-[1051px]:hidden'):
            with ui.button(icon='more_vert').props('flat color=white round'):
                with ui.menu().classes('bg-primary text-white text-lg'):
                    for title_, target in menu_items.items():
                        ui.menu_item(title_, on_click=lambda target=target: ui.navigate.to(target))
