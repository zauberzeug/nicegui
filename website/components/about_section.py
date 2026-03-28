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
                    NiceGUI manages web development details, letting you focus on Python code
                    for diverse applications, including robotics, IoT solutions, smart home automation,
                    and machine learning. Designed to work smoothly with connected peripherals like
                    webcams and GPIO pins in IoT setups, NiceGUI streamlines the management of all
                    your code in one place.
                ''').classes(d.TEXT_SECONDARY)
                ui.markdown('''
                    With a gentle learning curve, NiceGUI is user-friendly for beginners and offers
                    advanced customization for experienced users, ensuring simplicity for basic tasks
                    and feasibility for complex projects.
                ''').classes(d.TEXT_SECONDARY)
                ui.markdown('''
                    Available as
                    [PyPI package](https://pypi.org/project/nicegui/),
                    [Docker image](https://hub.docker.com/r/zauberzeug/nicegui) and on
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
