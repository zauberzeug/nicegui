from nicegui import ui

from . import doc


@doc.demo(ui.page)
def main_demo() -> None:
    @ui.page('/other_page')
    def other_page():
        ui.label('Welcome to the other side')

    @ui.page('/dark_page', dark=True)
    def dark_page():
        ui.label('Welcome to the dark side')

    ui.link('Visit other page', other_page)
    ui.link('Visit dark page', dark_page)


@doc.demo('Pages with Path Parameters', '''
    Page routes can contain parameters like [FastAPI](https://fastapi.tiangolo.com/tutorial/path-params/).
    If type-annotated, they are automatically converted to bool, int, float and complex values.
    If the page function expects a `request` argument, the request object is automatically provided.
    The `client` argument provides access to the websocket connection, layout, etc.
''')
def page_with_path_parameters_demo():
    @ui.page('/repeat/{word}/{count}')
    def page(word: str, count: int):
        ui.label(word * count)

    ui.link('Say hi to Santa!', '/repeat/Ho! /3')


@doc.demo('Wait for Client Connection', '''
    To wait for a client connection, you can add a `client` argument to the decorated page function
    and await `client.connected()`.
    All code below that statement is executed after the websocket connection between server and client has been established.

    For example, this allows you to run JavaScript commands; which is only possible with a client connection (see [#112](https://github.com/zauberzeug/nicegui/issues/112)).
    Also it is possible to do async stuff while the user already sees some content.
''')
def wait_for_connected_demo():
    import asyncio

    @ui.page('/wait_for_connection')
    async def wait_for_connection():
        ui.label('This text is displayed immediately.')
        await ui.context.client.connected()
        await asyncio.sleep(2)
        ui.label('This text is displayed 2 seconds after the page has been fully loaded.')
        ui.label(f'The IP address {ui.context.client.ip} was obtained from the websocket.')

    ui.link('wait for connection', wait_for_connection)


@doc.demo('Modularize with APIRouter', '''
    You can use the NiceGUI specialization of
    [FastAPI's APIRouter](https://fastapi.tiangolo.com/tutorial/bigger-applications/?h=apirouter#apirouter)
    to modularize your code by grouping pages and other routes together.
    This is especially useful if you want to reuse the same prefix for multiple pages.
    The router and its pages can be neatly tugged away in a separate module (e.g. file) and
    the router is simply imported and included in the main app.
    See our [modularization example](https://github.com/zauberzeug/nicegui/blob/main/examples/modularization/api_router_example.py)
    for a multi-file app structure using an API router.
''', tab='/sub-path')
def api_router_demo():
    # from nicegui import APIRouter, app
    #
    # router = APIRouter(prefix='/sub-path')
    #
    # @router.page('/')
    # def page():
    #     ui.label('This is content on /sub-path')
    #
    # @router.page('/sub-sub-path')
    # def page():
    #     ui.label('This is content on /sub-path/sub-sub-path')
    #
    # ui.link('Visit sub-path', '/sub-path')
    # ui.link('Visit sub-sub-path', '/sub-path/sub-sub-path')
    #
    # app.include_router(router)
    # END OF DEMO
    ui.label('Shows up on /sub-path')
