from nicegui import ui

from .. import design as d
from .shared import section, section_label, section_title


def create() -> None:
    """Create the about section with description text and interactive demo card."""
    with section('about'):
        with ui.grid().classes(
            'reveal w-full grid-cols-[1.5fr_1fr] max-lg:grid-cols-1 gap-16 items-center justify-items-center'
        ):
            with ui.column().classes('gap-0'):
                section_label('about')
                section_title('Interact with Python through buttons, dialogs, 3D\u00a0scenes, plots and much more.')
                ui.markdown('''
                    NiceGUI manages web development details, letting you focus on Python code.
                    Connect peripherals like webcams and GPIO pins, build interactive UIs,
                    and run your entire application from a single script.
                ''').classes(f'{d.TEXT_SECONDARY} max-lg:hidden')
                ui.markdown('''
                    Focus on Python - connect peripherals, build interactive UIs, and run everything from a single script.
                ''').classes(f'{d.TEXT_SECONDARY} lg:hidden')
                ui.markdown('''
                    Available on
                    [PyPI](https://pypi.org/project/nicegui/),
                    [Docker](https://hub.docker.com/r/zauberzeug/nicegui) and
                    [GitHub](https://github.com/zauberzeug/nicegui).
                ''').classes(d.TEXT_SECONDARY)

            with ui.column().classes(f'rounded-2xl p-8 w-full max-w-120 {d.BG_SURFACE} {d.BORDER} {d.SHADOW_CARD}'):
                _simple_demo()


def _simple_demo() -> None:
    """Create a simplified interactive demo matching the click dummy style."""
    with ui.column().classes('w-full items-stretch'):
        output = ui.label('Try it out!') \
            .classes(f'min-h-14 p-3 text-center text-lg rounded-lg overflow-auto {d.BG} {d.TEXT_SECONDARY} {d.BORDER}')
        ui.button('Click me!', on_click=lambda: output.set_text('Clicked!')).props('unelevated no-caps')
        ui.input(placeholder='Type here...', on_change=lambda e: output.set_text(e.value)).props('outlined dense')
        ui.slider(min=0, max=100, value=50, on_change=lambda e: output.set_text(f'{e.value:.0f}%'))
        ui.checkbox('Check me', on_change=lambda e: output.set_text('Checked' if e.value else 'Unchecked'))
