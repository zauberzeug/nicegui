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
    with ui.column():  # HIDE
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
    As with all other elements, you can implement your own subclass with specialized logic.
    Like this red/green toggle button with an internal boolean state.
''')
def toggle_button() -> None:
    class ToggleButton(ui.button):

        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)
            self._state = False
            self.on('click', self.toggle)

        def toggle(self) -> None:
            """Toggle the button state."""
            self._state = not self._state
            self.update()

        def update(self) -> None:
            self.props(f'color={"green" if self._state else "red"}')
            super().update()

    ToggleButton('Toggle me')


@doc.demo('Floating Action Button', '''
    As described in the [Quasar documentation](https://quasar.dev/vue-components/floating-action-button),
    a Floating Action Button (FAB) is simply a "page-sticky" with a button inside.
    With the "fab" prop, the button will be rounded and gets a shadow.
    Color can be freely chosen, but most often it is an accent color.
''')
def fab() -> None:
    ui.colors(accent='#6AD4DD')
    # with ui.page_sticky(x_offset=18, y_offset=18):
    with ui.row().classes('w-full h-full justify-end items-end'):  # HIDE
        ui.button(icon='home', on_click=lambda: ui.notify('home')) \
            .props('fab color=accent')


doc.text('Expandable Floating Action Button', '''We now have `ui.fab` and `ui.fab_action` elements, which are based on the [Quasar FAB (q-fab)](https://quasar.dev/vue-components/floating-action-button).

You can use them to create a Floating Action Button (FAB) with multiple actions that are revealed when the FAB is clicked.

Please see the [documentation for these elements](fab) for more information and migration instructions from the old `ui.element` approach.''')

doc.reference(ui.button)
