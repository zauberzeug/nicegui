from nicegui import ui

from ..header import add_head_html, add_header
from ..style import section_heading
from .model import Documentation


def render_page(documentation: Documentation, *, is_main: bool = False) -> None:
    """Render the documentation."""
    add_head_html()
    add_header()
    ui.add_head_html('<style>html {scroll-behavior: auto;}</style>')
    with ui.column().classes('w-full p-8 lg:p-16 max-w-[1250px] mx-auto'):
        if is_main:
            section_heading('Reference, Demos and more', '*NiceGUI* Documentation')
        if documentation.title:
            ui.markdown(f'# {documentation.title}')
        for part in documentation:
            if part.title:
                if part.link_target:
                    ui.link_target(part.link_target)
                if part.link:
                    with ui.link(target=part.link):
                        ui.markdown(f'### {part.title}')
                else:
                    ui.markdown(f'### {part.title}')
            if part.description:
                ui.markdown(part.description)
            if part.function:
                part.function()

    if not is_main:
        with ui.left_drawer():
            ui.markdown(f'[← back]({documentation.back_link})').classes('bold-links')
            for part in documentation:
                if part.title and part.link_target:
                    ui.link(part.title, f'#{part.link_target}')
