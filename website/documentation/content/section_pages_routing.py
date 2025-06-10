import uuid

from nicegui import app, ui

from . import (
    doc,
    download_documentation,
    navigate_documentation,
    page_documentation,
    page_layout_documentation,
    page_title_documentation,
    sub_pages_documentation,
)

CONSTANT_UUID = str(uuid.uuid4())

doc.title('*Pages* & Routing')

doc.intro(page_documentation)


@doc.demo('Auto-index page', '''
    Pages created with the `@ui.page` decorator are "private".
    Their content is re-created for each client.
    Thus, in the demo to the right, the displayed ID on the private page changes when the browser reloads the page.

    UI elements that are not wrapped in a decorated page function are placed on an automatically generated index page at route "/".
    This auto-index page is created once on startup and *shared* across all clients that might connect.
    Thus, each connected client will see the *same* elements.
    In the demo to the right, the displayed ID on the auto-index page remains constant when the browser reloads the page.
''')
def auto_index_page():
    from uuid import uuid4

    @ui.page('/private_page')
    async def private_page():
        ui.label(f'private page with ID {uuid4()}')

    # ui.label(f'shared auto-index page with ID {uuid4()}')
    # ui.link('private page', private_page)
    # END OF DEMO
    ui.label(f'shared auto-index page with ID {CONSTANT_UUID}')
    ui.link('private page', private_page)


doc.intro(page_layout_documentation)
doc.intro(sub_pages_documentation)


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
    ui.link('Star', '/icon/star?amount=5')
    ui.link('Home', '/icon/home')
    ui.link('Water', '/icon/water_drop?amount=3')


doc.intro(page_title_documentation)
doc.intro(navigate_documentation)

doc.redirects['open'] = 'navigate#ui_navigate_to_(formerly_ui_open)'
doc.text('ui.open', f'''
    The `ui.open` function is deprecated.
    Use [`ui.navigate.to`]({doc.redirects["open"]}) instead.
''')

doc.intro(download_documentation)


@doc.demo(app.add_static_files)
def add_static_files_demo():
    from nicegui import app

    app.add_static_files('/examples', 'examples')
    ui.label('Some NiceGUI Examples').classes('text-h5')
    ui.link('AI interface', '/examples/ai_interface/main.py')
    ui.link('Custom FastAPI app', '/examples/fastapi/main.py')
    ui.link('Authentication', '/examples/authentication/main.py')


@doc.demo(app.add_media_files)
def add_media_files_demo():
    from pathlib import Path

    import requests

    from nicegui import app

    media = Path('media')
    # media.mkdir(exist_ok=True)
    # r = requests.get('https://cdn.coverr.co/videos/coverr-cloudy-sky-2765/1080p.mp4')
    # (media  / 'clouds.mp4').write_bytes(r.content)
    # app.add_media_files('/my_videos', media)
    # ui.video('/my_videos/clouds.mp4')
    # END OF DEMO
    ui.video('https://cdn.coverr.co/videos/coverr-cloudy-sky-2765/1080p.mp4')


@doc.demo('Add HTML to the page', '''
    You can add HTML to the page by calling `ui.add_head_html` or `ui.add_body_html`.
    This is useful for adding custom CSS styles or JavaScript code.
''')
def add_head_html_demo():
    ui.add_head_html('''
        <style>
            .my-red-label {
                color: Crimson;
                font-weight: bold;
            }
        </style>
    ''')
    ui.label('RED').classes('my-red-label')


@doc.demo('API Responses', '''
    NiceGUI is based on [FastAPI](https://fastapi.tiangolo.com/).
    This means you can use all of FastAPI's features.
    For example, you can implement a RESTful API in addition to your graphical user interface.
    You simply import the `app` object from `nicegui`.
    Or you can run NiceGUI on top of your own FastAPI app by using `ui.run_with(app)` instead of starting a server automatically with `ui.run()`.

    You can also return any other FastAPI response object inside a page function.
    For example, you can return a `RedirectResponse` to redirect the user to another page if certain conditions are met.
    This is used in our [authentication demo](https://github.com/zauberzeug/nicegui/tree/main/examples/authentication/main.py).
''')
def fastapi_demo():
    import random

    from nicegui import app

    @app.get('/random/{max}')
    def generate_random_number(max: int):
        return {'min': 0, 'max': max, 'value': random.randint(0, max)}

    max = ui.number('max', value=100)
    ui.button('generate random number',
              on_click=lambda: ui.navigate.to(f'/random/{max.value:.0f}'))
