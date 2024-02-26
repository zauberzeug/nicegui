from nicegui import ui

from . import doc


@doc.demo(ui.button)
def main_demo() -> None:
    ui.button('Click me!', on_click=lambda: ui.notify('You clicked me!'))


@doc.demo('Icons', '''
    You can also add an icon to a button.
''')
def icons() -> None:
    with ui.row():
        ui.button('demo', icon='history')
        ui.button(icon='thumb_up')
        with ui.button():
            ui.label('sub-elements')
            ui.image('https://picsum.photos/id/377/640/360') \
                .classes('rounded-full w-16 h-16 ml-4')


@doc.demo('Await button click', '''
    Sometimes it is convenient to wait for a button click before continuing the execution.
''')
async def await_button_click() -> None:
    # @ui.page('/')
    # async def index():
    b = ui.button('Step')
    await b.clicked()
    ui.label('One')
    await b.clicked()
    ui.label('Two')
    await b.clicked()
    ui.label('Three')


@doc.demo('Disable button with a context manager', '''
    This showcases a context manager that can be used to disable a button for the duration of an async process.
''')
def disable_context_manager() -> None:
    from contextlib import contextmanager

    import httpx

    @contextmanager
    def disable(button: ui.button):
        button.disable()
        try:
            yield
        finally:
            button.enable()

    async def get_slow_response(button: ui.button) -> None:
        with disable(button):
            async with httpx.AsyncClient() as client:
                response = await client.get('https://httpbin.org/delay/1', timeout=5)
                ui.notify(f'Response code: {response.status_code}')

    ui.button('Get slow response', on_click=lambda e: get_slow_response(e.sender))


@doc.demo('Custom toggle button', '''
As with all other elements you can implement your own subclass with specialized logic.
Like this red/green toggle button with an internal boolean state.
''')
def toggle_button() -> None:
    class ToggleButton(ui.button):

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._state = False
            self.on('click', self.toggle)

        def toggle(self) -> None:
            """Toggle the button state."""
            self._state = not self._state
            self.update()

        def update(self):
            self.props(f'color={"green" if self._state else "red"}')
            super().update()

    ToggleButton('Toggle me')


doc.reference(ui.button)
