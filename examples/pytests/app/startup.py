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

    @ui.page('/scoped_user')
    def scoped_user_page() -> None:
        with ui.card().mark('scope-card left'):
            ui.label('Scope').mark('scope-title left')
            ui.button('Shared Action Left').mark('duplicate-button')
            ui.input('duplicated').mark('duplicated-marker')

        with ui.card().mark('scope-card right'):
            ui.label('Scope').mark('scope-title right')
            ui.button('Shared Action Right').mark('duplicate-button')
            ui.input('duplicated').mark('duplicated-marker')
