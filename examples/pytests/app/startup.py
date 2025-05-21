from nicegui import Client, ui

# pylint: disable=missing-function-docstring


def startup() -> None:
    @ui.page('/')
    def main_page() -> None:
        ui.markdown('Try running `pytest` on this project!')
        ui.button('Click me', on_click=lambda: ui.notify('Button clicked!'))
        ui.link('go to subpage', '/subpage')

    @ui.page('/subpage')
    def sub_page() -> None:
        ui.markdown('This is a subpage')

    @ui.page('/with_connected')
    async def with_connected(client: Client) -> None:
        ui.markdown('This is an async connection demo')
        await client.connected()
        ui.markdown('Connected!')
