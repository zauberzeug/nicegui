from nicegui import ui

from ..documentation_tools import text_demo


def main_demo() -> None:
    @ui.page('/other_page')
    def other_page():
        ui.label('Welcome to the other side')
        ui.link('Back to main page', '/documentation#page')

    @ui.page('/dark_page', dark=True)
    def dark_page():
        ui.label('Welcome to the dark side')
        ui.link('Back to main page', '/documentation#page')

    ui.link('Visit other page', other_page)
    ui.link('Visit dark page', dark_page)


def more() -> None:
    @text_demo('Pages with Path Parameters', '''
        Page routes can contain parameters like [FastAPI](https://fastapi.tiangolo.com/tutorial/path-params/>).
        If type-annotated, they are automatically converted to bool, int, float and complex values.
        If the page function expects a `request` argument, the request object is automatically provided.
        The `client` argument provides access to the websocket connection, layout, etc.
    ''')
    def page_with_path_parameters_demo():
        @ui.page('/repeat/{word}/{count}')
        def page(word: str, count: int):
            ui.label(word * count)

        ui.link('Say hi to Santa!', 'repeat/Ho! /3')

    @text_demo('Wait for Client Connection', '''
        To wait for a client connection, you can add a `client` argument to the decorated page function
        and await `client.connected()`.
        All code below that statement is executed after the websocket connection between server and client has been established.

        For example, this allows you to run JavaScript commands; which is only possible with a client connection (see [#112](https://github.com/zauberzeug/nicegui/issues/112)).
        Also it is possible to do async stuff while the user already sees some content.
    ''')
    def wait_for_connected_demo():
        import asyncio

        from nicegui import Client

        @ui.page('/wait_for_connection')
        async def wait_for_connection(client: Client):
            ui.label('This text is displayed immediately.')
            await client.connected()
            await asyncio.sleep(2)
            ui.label('This text is displayed 2 seconds after the page has been fully loaded.')
            ui.label(f'The IP address {client.ip} was obtained from the websocket.')

        ui.link('wait for connection', wait_for_connection)
