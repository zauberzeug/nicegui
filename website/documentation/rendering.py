import docutils.core

from nicegui import ui

from ..header import add_head_html, add_header
from ..style import section_heading, subheading
from .content import DocumentationPage
from .demo import demo
from .reference import generate_class_doc


def render_page(documentation: DocumentationPage, *, with_menu: bool = True) -> None:
    """Render the documentation."""

    # menu
    if with_menu:
        with ui.left_drawer() \
                .classes('column no-wrap gap-1 bg-[#eee] dark:bg-[#1b1b1b] mt-[-20px] px-8 py-20') \
                .style('height: calc(100% + 20px) !important') as menu:
            if documentation.back_link:
                ui.markdown(f'[← back]({documentation.back_link or "."})').classes('bold-links')
            else:
                ui.markdown('[← Overview](/documentation)').classes('bold-links')
            ui.markdown(f'**{documentation.heading.replace("*", "")}**').classes('mt-4')
    else:
        menu = None

    # header
    add_head_html()
    add_header(menu)
    ui.add_head_html('<style>html {scroll-behavior: auto;}</style>')

    # content
    def render_content():
        section_heading(documentation.subtitle or '', documentation.heading)
        for part in documentation.parts:
            if part.title:
                if part.link_target:
                    ui.link_target(part.link_target)
                subheading(part.title, link=part.link, major=part.reference is not None)
            if part.description:
                if part.description_format == 'rst':
                    description = part.description.replace('param ', '')
                    html = docutils.core.publish_parts(description, writer_name='html5_polyglot')['html_body']
                    ui.html(html).classes('bold-links arrow-links nicegui-markdown')
                else:
                    ui.markdown(part.description).classes('bold-links arrow-links')
            if part.ui:
                part.ui()
            if part.demo:
                demo(part.demo.function, lazy=part.demo.lazy, tab=part.demo.tab)
            if part.reference:
                generate_class_doc(part.reference)
            if part.link:
                ui.markdown(f'See [more...]({part.link})').classes('bold-links arrow-links')
    with ui.column().classes('w-full p-8 lg:p-16 max-w-[1250px] mx-auto'):
        if documentation.extra_column:
            with ui.grid().classes('grid-cols-[2fr_1fr] max-[600px]:grid-cols-[1fr] gap-x-8 gap-y-16'):
                with ui.column().classes('w-full'):
                    render_content()
                with ui.column():
                    documentation.extra_column()
        else:
            render_content()
