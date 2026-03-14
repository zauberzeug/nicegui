from nicegui import ui

from .shared import section, section_label, section_title


def _simple_demo() -> None:
    """Create a simplified interactive demo matching the click dummy style."""
    output = ui.label('Try it out!').classes(
        'text-center text-lg py-3 px-4 rounded-lg w-full',
    ).style(
        'background: var(--mo-bg); border: 1px solid var(--mo-border); color: var(--mo-text-secondary)',
    )

    with ui.column().classes('gap-3 mt-4 w-full'):
        ui.button('Click me!', on_click=lambda: output.set_text('Clicked!')) \
            .classes('w-full').props('unelevated color=primary')
        ui.input('Type here...', value='abc', on_change=lambda e: output.set_text(e.value)) \
            .classes('w-full')
        ui.slider(min=0, max=100, value=50, on_change=lambda e: output.set_text(str(int(e.value)))) \
            .classes('w-full')
        ui.checkbox('Check me', on_change=lambda e: output.set_text('Checked' if e.value else 'Unchecked'))


def create() -> None:
    """Create the about section with description text and interactive demo card."""
    with section('about', offset='70px'):
        with ui.row().classes('mo-about-inner mo-reveal items-center'):
            with ui.column().classes('mo-about-text'):
                section_label('about')
                section_title('Interact with Python through buttons, dialogs, 3D\u00a0scenes, plots and much more.')
                ui.markdown('''
                    NiceGUI manages web development details, letting you focus on Python code
                    for diverse applications, including robotics, IoT solutions, smart home automation,
                    and machine learning. Designed to work smoothly with connected peripherals like
                    webcams and GPIO pins in IoT setups, NiceGUI streamlines the management of all
                    your code in one place.
                ''').style('color: var(--mo-text-secondary)')
                ui.markdown('''
                    With a gentle learning curve, NiceGUI is user-friendly for beginners and offers
                    advanced customization for experienced users, ensuring simplicity for basic tasks
                    and feasibility for complex projects.
                ''').style('color: var(--mo-text-secondary)')
                ui.markdown('''
                    Available as
                    [PyPI package](https://pypi.org/project/nicegui/),
                    [Docker image](https://hub.docker.com/r/zauberzeug/nicegui) and on
                    [GitHub](https://github.com/zauberzeug/nicegui).
                ''').classes('bold-links').style('color: var(--mo-text-secondary)')

            with ui.column().classes('mo-demo-card'):
                _simple_demo()
