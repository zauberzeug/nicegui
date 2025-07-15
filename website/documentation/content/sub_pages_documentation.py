from nicegui import PageArgs
from nicegui import ui

from . import doc


@doc.demo('Sub Pages', '''
    Sub pages provide URL-based navigation between different views.
    This allows you to easily build a single page application (SPA).
    The `ui.sub_pages` element itself functions as the container for the currently active sub page.
    You only need to provide the routes for each view builder function.
    NiceGUI takes care of replacing the content without triggering a full page reload when the URL changes.

    **NOTE: This is an experimental feature, and the API is subject to change.**
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
    If a sub page needs data from its parent, a dictionary can be passed to the `ui.sub_pages` element.
    The data will be available as a keyword argument in the sub page function or as `PageArgs` object.
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
    #        '/': main,
    #        '/other': other,
    #     }, data={'title': title})

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
    ui.sub_pages({'/': main, '/other': other}, root_path='/documentation/sub_pages', data={'title': title})


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


@doc.demo('Using PageArgs', '''
          By type-hinting the parameter as `PageArgs`, the sub page builder function gets unified access to
          query parameters, path parameters, and more.
''')
def page_args_demo():
    from nicegui import PageArgs

    # @ui.page('/')
    # @ui.page('/{_:path}') # NOTE: our page should catch all paths
    # def index():
    #     ui.link('msg=hello', '/documentation/sub_pages?msg=hello')
    #     ui.link('msg=world', '/documentation/sub_pages?msg=world')
    #     ui.sub_pages({'/': main})

    def main(args: PageArgs):
        ui.label(args.query_parameters.get('msg', 'no message'))

    # END OF DEMO
    ui.link('msg=hello', '/documentation/sub_pages?msg=hello')
    ui.link('msg=world', '/documentation/sub_pages?msg=world')
    ui.sub_pages({'/': main}, root_path='/documentation/sub_pages')


@doc.demo('Nested Sub Pages', '''
    Sub pages elements can be nested to create a hierarchical page structure.
    Each of these elements determines which part of the path they should handle by:

      1. getting the full url path from `ui.context.client.sub_pages_router`
      2. removing the leading part which was handled by the parent element
      3. matching the route with the most specific path
      4. leaving the remaining part of the path for the next element (or if there is none, show a 404 error)
''')
def nested_sub_pages_demo():
    # @ui.page('/')
    # @ui.page('/{_:path}')  # NOTE: our page should catch all paths
    # def index():
    #     ui.link('Go to main', '/')
    #     ui.link('Go to other', '/other')
    #     ui.sub_pages({
    #         '/': main,
    #         '/other': other,
    #     }).classes('border-2 p-2')

    def main():
        ui.label('main page')

    def other():
        ui.label('sub page')
        # ui.link('Go to A', '/sub/a')
        # ui.link('Go to B', '/sub/b')
        ui.link('Go to A', '/documentation/sub_pages/other/a')  # HIDE
        ui.link('Go to B', '/documentation/sub_pages/other/b')  # HIDE
        ui.sub_pages({
            '/': sub_main,
            '/a': sub_page_a,
            '/b': sub_page_b
        }).classes('border-2 p-2')

    def sub_main():
        ui.label('sub main page')

    def sub_page_a():
        ui.label('sub A page')

    def sub_page_b():
        ui.label('sub B page')

    # END OF DEMO
    ui.link('Go to main', '/documentation/sub_pages')
    ui.link('Go to other', '/documentation/sub_pages/other')
    ui.sub_pages({'/': main, '/other': other, }, root_path='/documentation/sub_pages').classes('border-2 p-2')


doc.reference(ui.sub_pages, title='Reference for ui.sub_pages')

doc.reference(PageArgs, title='Reference for PageArgs')
