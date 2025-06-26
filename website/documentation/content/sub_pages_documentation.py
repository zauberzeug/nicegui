from nicegui import ui

from . import doc


@doc.demo('Sub Pages', '''
    Sub pages provide URL-based navigation between different views.
    This allows you to easily build a single page application (SPA).
    The `ui.sub_pages` element itself functions as the container for the currently active sub page.
    You only need to provide the routes for each view builder function.
    NiceGUI takes care of replacing the content without triggering a full page reload when the URL changes.
''')
def main_demo() -> None:
    from uuid import uuid4

    # @ui.page('/')
    # @ui.page('/{_:path}')  # NOTE: our page should catch all paths
    # def index():
    #     ui.label(f'This ID {str(uuid4())[:6]} changes only on reload.')
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
    ui.label(f'This ID {str(uuid4())[:6]} changes only on reload.')
    ui.separator()
    ui.sub_pages({'/': main, '/other': other}, root_path=f'/documentation/{location}')


@doc.demo('Passing Parameters to Sub Page', '''
    If a sub page needs to modify content from its parent, the object can simply be passed in a lambda function.
''')
def parameters_demo():
    # @ui.page('/')
    # @ui.page('/{_:path}') # NOTE: our page should catch all paths
    # def index():
    #     with ui.row():
    #         ui.label('Title:')
    #         title = ui.label()
    #     ui.separator()
    #     ui.sub_pages({
    #        '/': lambda: main(title),
    #        '/other': lambda: other(title),
    #     })

    def main(title: ui.label):
        title.text = 'Main page content'
        # ui.button('Go to other page', on_click=lambda: ui.navigate.to('/other'))
        ui.button('Go to other page', on_click=lambda: ui.navigate.to('/documentation/sub_pages/other'))  # HIDE

    def other(title: ui.label):
        title.text = 'Other page content'
        # ui.button('Go to main page', on_click=ui.navigate.to('/'))
        ui.button('Go to main page', on_click=lambda: ui.navigate.to('/documentation/sub_pages'))  # HIDE

    # END OF DEMO
    with ui.row():
        ui.label('Title:')
        title = ui.label()
    ui.separator()
    ui.sub_pages({'/': lambda: main(title), '/other': lambda: other(title)}, root_path='/documentation/sub_pages')


@doc.demo('Async Sub Pages', '''
    Sub pages also work with async builder functions.
''')
def async_demo():
    import asyncio

    # @ui.page('/')
    # @ui.page('/{_:path}')
    # def index():
    #     with ui.row():
    #         ui.link('main', '/')
    #         ui.link('other', '/other')
    #     ui.sub_pages({'/': main, '/other': lambda: other('other page')})

    async def main():
        ui.label('main page').classes('font-bold')
        await asyncio.sleep(2)
        ui.label('after 2 sec')

    async def other(title: str):
        ui.label(title).classes('font-bold')
        await asyncio.sleep(1)
        ui.label('after 1 sec')

    # END OF DEMO

    with ui.row():
        ui.link('main', '/documentation/sub_pages')
        ui.link('other', '/documentation/sub_pages/other')
    ui.sub_pages({'/': main, '/other': lambda: other('other page')},
                 root_path='/documentation/sub_pages')


@doc.demo('Adding Sub Pages', '''
    Sometimes not all routes are known when creating the `ui.sub_pages` element.
    In such cases, the `add` method can be used to add routes after the element has been created.
    This can also be used to pass elements which should be placed below the `ui.sub_pages` container.
''')
def adding_sub_pages_demo() -> None:
    # @ui.page('/')
    # @ui.page('/{_:path}') # NOTE: our page should catch all paths
    # def index():
    #     pages = ui.sub_pages()
    #     ui.separator()
    #     footer = ui.label()
    #     pages.add('/', lambda: main(footer))
    #     pages.add('/other', lambda: other(footer))

    def main(footer: ui.label):
        footer.text = 'normal footer'
        # ui.link('Go to other page', '/other')
        ui.link('Go to other page', '/documentation/sub_pages/other')  # HIDE

    def other(footer: ui.label):
        footer.text = 'other footer'
        # ui.link('Go to main page', '/')
        ui.link('Go to main page', '/documentation/sub_pages')  # HIDE

    # END OF DEMO
    pages = ui.sub_pages(root_path='/documentation/sub_pages')
    ui.separator()
    footer = ui.label()
    pages.add('/', lambda: main(footer))
    pages.add('/other', lambda: other(footer))


@doc.demo('Binding current path', '''
    The sub pages element has a `current_path` property which can be bound to.
''')
def binding_to_sub_pages_demo():
    # @ui.page('/')
    # @ui.page('/{_:path}') # NOTE: our page should catch all paths
    # def index():
    #     toggle = ui.toggle(['/', '/other'], value='/')
    #     ui.sub_pages({'/': main, '/{name}': main}) \
    #         .bind_current_path_from(toggle, 'value')
    #     ui.label().bind_text_from(pages, 'current_path')

    def main(name: str = 'main'):
        ui.label(name).classes('font-bold')

    # END OF DEMO
    toggle = ui.toggle(['/', '/other'], value='/')
    pages = ui.sub_pages({'/': main, '/{name}': main}, root_path='/documentation/sub_pages') \
        .bind_current_path_from(toggle, 'value')
    ui.label().bind_text_from(pages, 'current_path')


doc.reference(ui.sub_pages)
