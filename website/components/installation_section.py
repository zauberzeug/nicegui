from nicegui import ui

from .. import design as d
from ..documentation.windows import bash_window, browser_window, python_window
from .shared import section, section_heading


def create() -> None:
    """Create the installation section with 3-step flow and Docker expansion."""
    with section('installation'):
        section_heading('installation', 'Three lines to a running app.',
                        'Write a Python file, install and run \u2014 that\u2019s it.')

        with ui.grid().classes('grid-cols-3 max-lg:grid-cols-1 w-full gap-6 items-stretch'):
            with ui.column().classes('mo-reveal gap-3 items-stretch'):
                _step(1, 'Write')
                python_window('''
                    from nicegui import ui

                    ui.label('Hello NiceGUI!')

                    ui.run()
                ''').classes('grow')

            with ui.column().classes('mo-reveal gap-3 items-stretch delay-250!'):
                _step(2, 'Run')
                bash_window('''
                    $ pip3 install nicegui
                    $ python3 main.py
                ''').classes('grow')

            with ui.column().classes('mo-reveal gap-3 items-stretch delay-500!'):
                _step(3, 'Enjoy')
                browser_window(lambda: ui.label('Hello NiceGUI!'), lazy=False).classes('grow')

        with ui.expansion('...or use Docker to run your main.py').classes('w-full gap-2 mt-8'):
            with ui.row().classes('mt-8 w-full gap-8'):
                ui.markdown('''
                    With our [multi-arch Docker image](https://hub.docker.com/repository/docker/zauberzeug/nicegui)
                    you can start the server without installing any packages.

                    The command searches for `main.py` in your current directory and makes the app available
                    at http://localhost:8888.
                ''').classes('max-w-xl')
                bash_window('''
                    docker run -it --rm -p 8888:8080 \\\\
                        -v "$PWD":/app zauberzeug/nicegui
                ''')


def _step(number: int, label: str) -> None:
    """Render a step number badge with label."""
    with ui.row().classes(f'items-center gap-2.5 font-semibold {d.TEXT_15PX}'):
        ui.label(str(number)) \
            .classes(f'flex items-center justify-center size-[26px] rounded-full {d.TEXT_13PX} font-bold border-2 {d.BORDER_ACCENT} {d.TEXT_ACCENT}')
        ui.label(label)
