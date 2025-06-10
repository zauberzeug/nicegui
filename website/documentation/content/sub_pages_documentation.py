import asyncio
from nicegui import ui

from . import doc


@doc.demo('Sub Pages', '''
    Sub pages provide url based navigation between different views.
    This allows you to easily build a single page application (SPA).
    The `ui.sub_pages` element itself functions as the container for the currently active sub page.
    You only need to provide the routes for each view builder function.
    NiceGUI takes care of replacing the content without triggering a full page reload when the url changes.
    The `ui.sub_pages` element can be used as a context manager to automatically navigate to the correct sub page when the context is entered or exited.
''')
def main_demo() -> None:
    from uuid import uuid4
    # @ui.page('/')
    # @ui.page('/{_:path}') # NOTE: our page should catch all paths
    # def index():
    #     ui.label(f'This id {str(uuid4())[:6]} changes only on reload')
    #     ui.separator()
    #     ui.sub_pages({'/': main, '/other': other})
    location = 'section_pages_routing' if 'section_pages_routing' in ui.context.client.request.url.path else 'sub_pages'  # HIDE

    def main():
        ui.label('Main page content')
        # ui.link('Go to other page', '/other')
        ui.link('Go to other page', f'/documentation/{location}/other')  # HIDE

    def other():
        ui.label('Another page content')
        # ui.link('Go to main page', '/')
        ui.link('Go to main page', f'/documentation/{location}')  # HIDE

    # END OF DEMO
    ui.label(f'This id {str(uuid4())[:6]} changes only on reload')
    ui.separator()
    ui.sub_pages({'/': main, '/other': other}, root_path=f'/documentation/{location}')


@doc.demo('Passing Parameters', '''
    If a sub page needs to modify content from it's parent, the object can simply be passed via lambda.
''')
def parameters_demo():
    # @ui.page('/')
    # def index():
    #     with ui.row():
    #         ui.label('Title:')
    #         title = ui.label()
    #     ui.separator()
    #     ui.sub_pages({
    #        '/': lambda: main(title),
    #        '/other': lambda: other(title),
    #     })

    async def main(title: ui.label):
        title.set_text('Main page content')
        # ui.button('Go to other page', on_click=lambda: ui.navigate.to('/other'))
        ui.button('Go to other page', on_click=lambda: ui.navigate.to('/documentation/sub_pages/other'))  # HIDE

    def other(title: ui.label):
        title.set_text('Other page content')
        # ui.button('Go to main page', on_click=ui.navigate.to('/'))
        ui.button('Go to main page', on_click=lambda: ui.navigate.to('/documentation/sub_pages'))  # HIDE

    # END OF DEMO
    with ui.row():
        ui.label('Title:')
        title = ui.label()
    ui.separator()
    ui.sub_pages({'/': lambda: main(title), '/other': lambda: other(title)}, root_path='/documentation/sub_pages')


@doc.demo('Async Sub Pages', '''
    `ui.sub_pages` also work for async builder functions.
''')
def async_demo():
    # @ui.page('/')
    # def index():
    #     title = ui.label()
    #     ui.sub_pages({'/': lambda: main(title)})
    #     ui.toggle({'main': '/', 'other': '/other'},
    #               value='main',
    #               on_change=lambda e: ui.navigate.to(f'/{e.value}'))

    async def main(delay: int):
        label = ui.label('delayed...')
        await asyncio.sleep(delay)
        label.set_text(f'after {delay} sec')

    async def other():
        label = ui.label('delayed...')
        await asyncio.sleep(1)
        label.set_text('after 1 sec')

    # END OF DEMO
    ui.sub_pages({'/': lambda: main(2), '/other': other}, root_path='/documentation/sub_pages')
    ui.toggle({'': 'main', 'other': 'other'}, value='',
              on_change=lambda e: ui.navigate.to(f'/documentation/sub_pages/{e.value}'))


doc.reference(ui.sub_pages)
