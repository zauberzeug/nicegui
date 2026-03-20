import os
from pathlib import Path

from pygments.formatters import HtmlFormatter

from nicegui import app, ui

from . import design as d
from . import github_stars
from .design import phosphor_icon
from .search import Search

HEADER_HTML = (Path(__file__).parent / 'static' / 'header.html').read_text(encoding='utf-8')
STYLE_CSS = (Path(__file__).parent / 'static' / 'style.css').read_text(encoding='utf-8')

FONT_LINKS = '''
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Fira+Mono&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
    <link href="https://unpkg.com/@phosphor-icons/web@2.1.1/src/duotone/style.css" rel="stylesheet" />
'''

MENU_ITEMS = {
    'Installation': '/#installation',
    'Features': '/#features',
    'Demos': '/#demos',
    'Documentation': '/documentation',
    'Examples': '/examples',
    'Why?': '/#why',
}

SM_UP = 'max-[460px]:hidden'
MD_UP = 'max-[590px]:hidden'
LG_UP = 'max-[1050px]:hidden'
LG_DOWN = 'min-[1050px]:hidden'


def add_head_html() -> None:
    """Add the code from header.html and reference style.css."""
    ui.add_head_html(HEADER_HTML)
    ui.add_head_html(FONT_LINKS)
    ui.add_css(STYLE_CSS)
    ui.add_css(f'''
        {HtmlFormatter(nobackground=True, style="solarized-light").get_style_defs(".code-window .codehilite")}
        {HtmlFormatter(nobackground=True, style="solarized-dark").get_style_defs(".body--dark .code-window .codehilite")}
    ''')
    if os.environ.get('ENABLE_ANALYTICS', 'false').lower() == 'true':
        ui.add_head_html('''
            <!-- Privacy-friendly analytics by Plausible -->
            <script async src="https://plausible.io/js/pa-d9tl9pdueh-ArCJfoLv3H.js"></script>
            <script>
            window.plausible=window.plausible||function(){(plausible.q=plausible.q||[]).push(arguments)},plausible.init=plausible.init||function(i){plausible.o=i||{}};
            plausible.init()
            </script>
        ''')


def add_header(menu: ui.left_drawer) -> ui.button:
    """Create the page header."""
    dark_mode = ui.dark_mode(value=app.storage.browser.get('dark_mode'), on_change=lambda e: ui.run_javascript(f'''
        fetch('/dark_mode', {{
            method: 'POST',
            headers: {{'Content-Type': 'application/json'}},
            body: JSON.stringify({{value: {e.value}}}),
        }});
    '''))
    with ui.header() \
        .style('background: transparent; box-shadow: none') \
        .classes(
        'items-center p-0 px-6 no-wrap h-16'
        ' transition-[background,backdrop-filter,box-shadow] duration-200'
        f' [&.fade]:!bg-[color-mix(in_srgb,{d._BG_SURFACE_LIGHT}_80%,transparent)]'
        f' dark:[&.fade]:!bg-[color-mix(in_srgb,{d._BG_SURFACE_DARK}_80%,transparent)]'
        f' [&.fade]:backdrop-blur-[12px] [&.fade]:!shadow-[0_1px_0_{d._BORDER_LIGHT}]'
        f' dark:[&.fade]:!shadow-[0_1px_0_{d._BORDER_DARK}]'
    ):
        menu_button = ui.button(on_click=menu.toggle, icon='menu').props('flat round').classes('lg:hidden')
        with ui.link(target='/'):
            ui.markdown('**Nice**GUI').classes(f'{d.TEXT_19PX} {d.TEXT_PRIMARY} tracking-wide')

        ui.space()

        with ui.row().classes(f'{d.TEXT_SECONDARY} gap-8 {LG_UP}'):
            for title_, target in MENU_ITEMS.items():
                ui.link(title_, target).classes(d.TEXT_15PX)

        with ui.row().classes('gap-2 items-center ml-8'):
            search = Search()
            _search_pill(search)
            _theme_toggle(dark_mode)
            _github_badge()

        with ui.row().classes(LG_DOWN):
            with ui.button(icon='more_vert').props('flat round'):
                with ui.menu().classes(f'rounded-xl {d.BG_SURFACE} {d.BORDER} no-shadow'):
                    for title_, target in MENU_ITEMS.items():
                        ui.menu_item(title_, on_click=lambda target=target: ui.navigate.to(target)) \
                            .classes(f'{d.TEXT_15PX} {d.TEXT_SECONDARY}')

    return menu_button


def _search_pill(search: Search) -> None:
    """Search button styled as a pill with keyboard shortcut hint."""
    with ui.button(on_click=search.open_dialog, color='transparent') \
            .props('unelevated no-caps rounded') \
            .classes(f'header-search-pill px-3.5 {d.TEXT_13PX} {d.BORDER}'
                     ' hover:border-gray-500 transition-[border-color] duration-150'):
        with ui.row().classes(f'gap-2 items-center {d.TEXT_MUTED}'):
            phosphor_icon('ph-magnifying-glass').classes('text-base')
            ui.label('Search').classes(f'font-normal {MD_UP}')
            ui.label('\u2318K') \
                .classes(f'{d.TEXT_13PX_MONO} px-1.5 rounded {d.BG_SURFACE} {d.BORDER} {d.TEXT_MUTED} {MD_UP}')


def _theme_toggle(dark_mode: ui.dark_mode) -> None:
    """Single theme toggle button cycling dark → light → auto."""
    with ui.element().classes(f'saturate-0 {SM_UP}'):
        d.tooltip('Cycle theme mode through dark, light, and system/auto.')
        with ui.button(on_click=lambda: dark_mode.set_value(None)).props('flat round') \
                .classes('size-9').bind_visibility_from(dark_mode, 'value', value=True):
            phosphor_icon('ph-moon').classes('text-[1.125rem]')
        with ui.button(on_click=lambda: dark_mode.set_value(True)).props('flat round') \
                .classes('size-9').bind_visibility_from(dark_mode, 'value', value=False):
            phosphor_icon('ph-sun').classes('text-[1.125rem]')
        with ui.button(on_click=lambda: dark_mode.set_value(False)).props('flat round') \
                .classes('size-9').bind_visibility_from(dark_mode, 'value', lambda mode: mode is None):
            phosphor_icon('ph-circle-half').classes('text-[1.125rem]')


def _github_badge() -> None:
    """GitHub link with star count badge."""
    with ui.link(target='https://github.com/zauberzeug/nicegui/') \
            .classes(f'rounded-full px-3.5 py-1.5 {d.TEXT_13PX} {d.BORDER} {SM_UP} '
                     'hover:border-gray-500 transition-[border-color] duration-150'):
        with ui.row().classes(f'gap-2 items-center {d.TEXT_MUTED}'):
            phosphor_icon('ph-github-logo').classes('text-base')
            ui.label().bind_text_from(github_stars.stars, 'short_string').classes(MD_UP)
