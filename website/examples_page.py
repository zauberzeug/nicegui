from nicegui import ui

from .examples import examples
from .seo import breadcrumb_jsonld, noscript_fallback, page_seo_html
from .style import example_link, link_target, section_heading


def create() -> None:
    _title = 'NiceGUI Examples - Python UI Code Samples and Demos'
    _description = ('Browse in-depth NiceGUI examples including authentication, '
                    'chat apps, todo lists, and more. '
                    'See real Python GUI code with live demos.')
    ui.page_title(_title)
    ui.add_head_html(page_seo_html(title=_title, description=_description, path='/examples'))
    ui.add_body_html(noscript_fallback(title=_title, description=_description))
    ui.add_head_html(breadcrumb_jsonld([('Home', '/'), ('Examples', '/examples')]))
    with ui.column().classes('w-full p-8 lg:p-16 max-w-[1600px] mx-auto'):
        link_target('examples')
        section_heading('In-depth examples', 'Pick your *solution*')
        with ui.row().classes('w-full text-lg leading-tight grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4'):
            for example in examples:
                example_link(example)
