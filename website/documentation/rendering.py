from typing import Optional, Tuple

from nicegui import ui

from ..header import add_head_html, add_header
from ..style import section_heading
from .model import Documentation


def render(documentation: Documentation, heading: Optional[Tuple[str, str]] = None) -> None:
    """Render the documentation."""
    add_head_html()
    add_header()
    ui.add_head_html('<style>html {scroll-behavior: auto;}</style>')
    with ui.column().classes('w-full p-8 lg:p-16 max-w-[1250px] mx-auto'):
        if heading:
            section_heading(*heading)
        if documentation.TITLE:
            ui.markdown(f'# {documentation.TITLE}')
        for part in documentation:
            if part.title:
                if part.link:
                    with ui.link(target=part.link):
                        ui.markdown(f'### {part.title}')
                else:
                    ui.markdown(f'### {part.title}')
            if part.description:
                ui.markdown(part.description)
            if part.function:
                part.function()
