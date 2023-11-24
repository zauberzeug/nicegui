import importlib
import inspect
import logging
from typing import Dict

from nicegui import context, ui

from . import documentation
from .documentation.content.overview import Overview
from .documentation.model import ElementDocumentation, SectionDocumentation
from .documentation.sections.text_elements import TextElementsDocumentation
from .header import add_head_html, add_header
from .style import section_heading, side_menu

overview = Overview('/documentation')
sections: Dict[str, SectionDocumentation] = {
    d.route.split('/')[-1]: d
    for d in [
        TextElementsDocumentation('/documentation/section_text_elements'),
    ]
}
elements: Dict[str, ElementDocumentation] = {
    element_documentation.route.split('/')[-1]: element_documentation
    for section in sections.values()
    for element_documentation in section.element_documentations
}


def create_overview() -> None:
    """Create the documentation overview."""
    documentation.render(overview)


def create_page(name: str) -> None:
    doc = elements.get(name) or sections.get(name)
    if not doc:
        raise ValueError(f'unknown documentation page: {name}')
    documentation.render(doc)


def create_section(name: str) -> None:
    """Create a documentation section."""
    add_head_html()
    with side_menu() as menu:
        ui.markdown('[← Overview](/documentation)').classes('bold-links')
    add_header(menu)
    ui.add_head_html('<style>html {scroll-behavior: auto;}</style>')
    with ui.column().classes('w-full p-8 lg:p-16 max-w-[1250px] mx-auto'):
        documentation.create_section(name)


async def create_more(name: str) -> None:
    """Create a documentation page for a "more" page."""
    if name in {'ag_grid', 'e_chart'}:
        name = name.replace('_', '')  # NOTE: "AG Grid" leads to anchor name "ag_grid", but class is `ui.aggrid`
    module = importlib.import_module(f'website.documentation.more.{name}_documentation')
    more = getattr(module, 'more', None)
    api = getattr(ui, name, name)

    add_head_html()
    add_header()
    with side_menu() as menu:
        ui.markdown('[← Overview](/documentation)').classes('bold-links')  # TODO: back to section
    with ui.column().classes('w-full p-8 lg:p-16 max-w-[1250px] mx-auto'):
        section_heading('Documentation', f'ui.*{name}*' if hasattr(ui, name) else f'*{name.replace("_", " ").title()}*')
        with menu:
            ui.markdown('**Demos**' if more else '**Demo**').classes('mt-4')
        documentation.element_demo(api)(getattr(module, 'main_demo'))
        if more:
            more()
        if inspect.isclass(api):
            with menu:
                ui.markdown('**Reference**').classes('mt-4')
            ui.markdown('## Reference').classes('mt-16')
            documentation.generate_class_doc(api)
    try:
        await context.get_client().connected()
        ui.run_javascript(f'document.title = "{name} • NiceGUI";')
    except TimeoutError:
        logging.warning(f'client did not connect for page /documentation/{name}')
