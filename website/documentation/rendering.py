from nicegui import ui

from ..header import add_head_html, add_header
from ..style import section_heading
from .model import Documentation, UiElementDocumentation
from .tools import generate_class_doc


def render_page(documentation: Documentation, *, is_main: bool = False) -> None:
    """Render the documentation."""

    # header
    add_head_html()
    add_header()
    ui.add_head_html('<style>html {scroll-behavior: auto;}</style>')

    # menu
    if is_main:
        menu = None
    else:
        with ui.left_drawer() \
                .classes('column no-wrap gap-1 bg-[#eee] dark:bg-[#1b1b1b] mt-[-20px] px-8 py-20') \
                .style('height: calc(100% + 20px) !important') as menu:
            ui.markdown(f'[← back]({documentation.back_link})').classes('bold-links')
            ui.markdown(f'**{documentation.title.replace("*", "")}**').classes('mt-4')
            for part in documentation:
                if part.title and part.link_target:
                    ui.link(part.title, f'#{part.link_target}')

    # content
    with ui.column().classes('w-full p-8 lg:p-16 max-w-[1250px] mx-auto'):

        # heading
        section_heading(documentation.subtitle, documentation.title)

        # parts
        for part in documentation:
            if part.title:
                if part.link_target:
                    ui.link_target(part.link_target)
                if part.link and part.link != documentation.route:
                    with ui.link(target=part.link):
                        ui.markdown(f'### {part.title}')
                else:
                    ui.markdown(f'### {part.title}')
            if part.description:
                ui.markdown(part.description)
            if part.function:
                part.function()

        # reference
        if isinstance(documentation, UiElementDocumentation) and isinstance(documentation.element, type) and menu:
            with menu:
                ui.markdown('**Reference**').classes('mt-4')
            ui.markdown('## Reference').classes('mt-16')
            generate_class_doc(documentation.element)
