import docutils.core

from nicegui import ui
from nicegui.elements.markdown import apply_tailwind

from ..header import add_head_html, add_header
from ..style import section_heading, subheading
from .demo import demo
from .model import Documentation, UiElementDocumentation
from .reference import generate_class_doc


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

    # content
    with ui.column().classes('w-full p-8 lg:p-16 max-w-[1250px] mx-auto'):

        # heading
        section_heading(documentation.subtitle, documentation.title)

        # parts
        for part in documentation:
            if part.title:
                if part.link_target:
                    ui.link_target(part.link_target)
                link = part.link if part.link != documentation.route else None
                subheading(part.title, make_menu_entry=not is_main, link=link)
            if part.description:
                if part.description_format == 'rst':
                    description = part.description.replace('param ', '')
                    html = docutils.core.publish_parts(description, writer_name='html5_polyglot')['html_body']
                    html = apply_tailwind(html)
                    ui.html(html)
                else:
                    ui.markdown(part.description)
            if part.ui:
                part.ui()
            if part.demo:
                demo(part.demo)

        # reference
        if isinstance(documentation, UiElementDocumentation) and isinstance(documentation.element, type) and menu:
            with menu:
                ui.markdown('**Reference**').classes('mt-4')
            ui.markdown('## Reference').classes('mt-16')
            generate_class_doc(documentation.element)
