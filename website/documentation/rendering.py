import docutils.core

from nicegui import ui
from nicegui.elements.markdown import apply_tailwind

from ..header import add_head_html, add_header
from ..style import section_heading, subheading
from .content import DocumentationPage
from .demo import demo
from .reference import generate_class_doc


def render_page(documentation: DocumentationPage, *, is_main: bool = False) -> None:
    """Render the documentation."""

    # header
    add_head_html()
    add_header()
    ui.add_head_html('<style>html {scroll-behavior: auto;}</style>')

    # menu
    if not is_main:
        with ui.left_drawer() \
                .classes('column no-wrap gap-1 bg-[#eee] dark:bg-[#1b1b1b] mt-[-20px] px-8 py-20') \
                .style('height: calc(100% + 20px) !important'):
            ui.markdown(f'[← back]({documentation.back_link})').classes('bold-links')
            ui.markdown(f'**{documentation.heading.replace("*", "")}**').classes('mt-4')

    # content
    with ui.column().classes('w-full p-8 lg:p-16 max-w-[1250px] mx-auto'):

        # heading
        section_heading(documentation.subtitle or '', documentation.heading)

        # parts
        for part in documentation.parts:
            if part.title:
                if part.link_target:
                    ui.link_target(part.link_target)
                subheading(part.title, link=part.link)
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
                demo(part.demo.function, lazy=part.demo.lazy)
            if part.reference:
                generate_class_doc(part.reference)
