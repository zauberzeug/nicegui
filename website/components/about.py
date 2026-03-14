from nicegui import ui

from ..style import link_target


def _simple_demo() -> None:
    """Create a simplified interactive demo matching the click dummy style."""
    output = ui.label('Try it out!').classes(
        'text-center text-lg py-3 px-4 rounded-lg w-full'
    ).style(
        'background: var(--mo-bg); border: 1px solid var(--mo-border); color: var(--mo-text-secondary);'
    )

    with ui.column().classes('gap-3 mt-4 w-full'):
        ui.button('Click me!', on_click=lambda: output.set_text('Clicked!')) \
            .classes('w-full').style(
                'background: var(--mo-brand-blue); color: white; border-radius: 8px;'
            )
        ui.input('Type here...', value='abc', on_change=lambda e: output.set_text(e.value)) \
            .classes('w-full')
        ui.slider(min=0, max=100, value=50, on_change=lambda e: output.set_text(str(int(e.value)))) \
            .classes('w-full').style('accent-color: var(--mo-brand-blue);')
        ui.checkbox('Check me', on_change=lambda e: output.set_text('Checked' if e.value else 'Unchecked'))


def create() -> None:
    """Create the about section with description text and interactive demo card."""
    with ui.element('section').classes('mo-about'):
        link_target('about', '70px')
        with ui.element('div').classes('mo-about-inner mo-reveal'):
            with ui.element('div').classes('mo-about-text'):
                ui.html('<div class="mo-section-label">about</div>', sanitize=False)
                ui.html(
                    '<h2 class="mo-section-title">'
                    'Interact with Python through buttons, dialogs, 3D&nbsp;scenes, plots and much more.'
                    '</h2>',
                    sanitize=False,
                )
                ui.html('''
                    <p>NiceGUI manages web development details, letting you focus on Python code
                    for diverse applications, including robotics, IoT solutions, smart home automation,
                    and machine learning. Designed to work smoothly with connected peripherals like
                    webcams and GPIO pins in IoT setups, NiceGUI streamlines the management of all
                    your code in one place.</p>
                ''', sanitize=False)
                ui.html('''
                    <p>With a gentle learning curve, NiceGUI is user-friendly for beginners and offers
                    advanced customization for experienced users, ensuring simplicity for basic tasks
                    and feasibility for complex projects.</p>
                ''', sanitize=False)
                ui.html('''
                    <p>Available as
                    <a href="https://pypi.org/project/nicegui/">PyPI package</a>,
                    <a href="https://hub.docker.com/r/zauberzeug/nicegui">Docker image</a> and on
                    <a href="https://github.com/zauberzeug/nicegui">GitHub</a>.</p>
                ''', sanitize=False)

            with ui.element('div').classes('mo-demo-card'):
                _simple_demo()
