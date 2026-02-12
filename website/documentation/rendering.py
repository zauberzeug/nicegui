from nicegui import ui

from ..style import section_heading, subheading
from .content import DocumentationPage
from .custom_restructured_text import CustomRestructuredText as custom_restructured_text
from .demo import demo
from .reference import generate_class_doc


def render_page(documentation: DocumentationPage) -> None:
    """Render the documentation."""
    title = (documentation.title or '').replace('*', '')
    ui.page_title('NiceGUI' if not title else title if title.split()[0] == 'NiceGUI' else f'{title} | NiceGUI')

    def _render_part(part):
        if part.title:
            if part.link_target:
                ui.link_target(part.link_target)
            is_group = bool(part.children)
            subheading(part.title,
                       link=f'/documentation/{part.link}' if part.link and not is_group else None,
                       major=part.reference is not None or is_group)
        if part.description:
            if part.description_format == 'rst':
                element = custom_restructured_text(part.description.replace(':param ', ':'))
            else:
                element = ui.markdown(part.description)
            element.classes('bold-links arrow-links w-full overflow-x-auto')
            if ':param' in part.description:
                element.classes('rst-param-tables')
        if part.ui:
            part.ui()
        if part.demo:
            demo(part.demo.function, lazy=part.demo.lazy, tab=part.demo.tab)
        if part.reference:
            generate_class_doc(part.reference, part.title)
        if part.link and not part.children:
            ui.markdown(f'See [more...](/documentation/{part.link})').classes('bold-links arrow-links')

    def render_content():
        section_heading(documentation.subtitle or '', documentation.heading)
        for part in documentation.parts:
            _render_part(part)
            for child in part.children:
                _render_part(child)
    with ui.column().classes('w-full p-8 lg:p-16 max-w-[1250px] mx-auto'):
        if documentation.extra_column:
            with ui.grid().classes('grid-cols-[2fr_1fr] max-[600px]:grid-cols-[1fr] gap-x-8 gap-y-16'):
                with ui.column().classes('w-full'):
                    render_content()
                with ui.column():
                    documentation.extra_column()
        else:
            render_content()
    with ui.column().classes('w-full p-4 items-end'):
        ui.link('Imprint & Privacy', '/imprint_privacy').classes('text-sm')
