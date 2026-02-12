from nicegui import ui

from .. import doc
from . import (
    page_documentation,
    page_layout_documentation,
    sub_pages_documentation,
)

doc.title('Page Setup')

doc.intro(page_documentation)
doc.intro(page_layout_documentation)
doc.intro(sub_pages_documentation)


@doc.demo('Script Mode', '''
    While generally you would either use `@ui.page` decorators or a root function to create pages,
    it is cumbersome when making quick prototypes or demos.
    In such cases, you can use "script mode" by simply writing code at the top level of a script.
    The code will be executed once per client connection, and the interface will be created for that client.
''')
def script_mode_demo():
    ui.label('No @ui.page, no root function, but still a working page!')


doc.text('', 'Note: Many of the demos in this documentation are written in script mode for conciseness.')


@doc.auto_execute
@doc.demo('Parameter injection', '''
    Thanks to FastAPI, a page function accepts optional parameters to provide
    [path parameters](https://fastapi.tiangolo.com/tutorial/path-params/),
    [query parameters](https://fastapi.tiangolo.com/tutorial/query-params/) or the whole incoming
    [request](https://fastapi.tiangolo.com/advanced/using-request-directly/) for accessing
    the body payload, headers, cookies and more.
''')
def parameter_demo():
    @ui.page('/icon/{icon}')
    def icons(icon: str, amount: int = 1):
        ui.label(icon).classes('text-h3')
        with ui.row():
            [ui.icon(icon).classes('text-h3') for _ in range(amount)]

    # @ui.page('/')
    def page():
        ui.link('Star', '/icon/star?amount=5')
        ui.link('Home', '/icon/home')
        ui.link('Water', '/icon/water_drop?amount=3')
    page()  # HIDE
