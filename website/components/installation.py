from nicegui import ui

from .. import documentation
from .shared import browser_window, code_window, section, section_heading


def _step(number: int, label: str) -> None:
    """Render a step number badge with label."""
    with ui.row().classes('items-center gap-2.5 font-semibold'):
        ui.label(str(number)).classes('mo-step-num')
        ui.label(label)


def create() -> None:
    """Create the installation section with 3-step flow and Docker expansion."""
    with section('installation'):
        section_heading('get_started', 'Three lines to a running app.',
                        'Write a Python file, install and run \u2014 that\u2019s it.')

        with ui.element('div').classes('mo-install-steps mo-reveal'):
            with ui.column().classes('mo-install-step'):
                _step(1, 'Write')
                code_window('main.py', 'description', (
                    '<span class="kw">from</span> nicegui <span class="kw">import</span> ui\n'
                    'ui.label(<span class="str">\'Hello NiceGUI!\'</span>)\n'
                    'ui.run()'
                ))

            with ui.column().classes('mo-install-step'):
                _step(2, 'Run')
                code_window('bash', 'terminal', (
                    '<span class="op">$</span> pip3 install nicegui\n'
                    '<span class="op">$</span> python3 main.py'
                ))

            with ui.column().classes('mo-install-step'):
                _step(3, 'Enjoy')
                with browser_window():
                    with ui.column().classes('mo-browser-content'):
                        ui.label('Hello NiceGUI!')
                        ui.button('Button').props('unelevated dense color=primary size=sm')

        with ui.expansion('...or use Docker to run your main.py').classes('w-full gap-2 mt-8'):
            with ui.row().classes('mt-8 w-full justify-center items-center gap-8'):
                ui.markdown('''
                    With our [multi-arch Docker image](https://hub.docker.com/repository/docker/zauberzeug/nicegui)
                    you can start the server without installing any packages.

                    The command searches for `main.py` in your current directory and makes the app available
                    at http://localhost:8888.
                ''').classes('max-w-xl')
                with documentation.bash_window(classes='max-w-lg w-full h-52'):
                    ui.markdown('''
                        ```bash
                        docker run -it --rm -p 8888:8080 \\\\
                            -v "$PWD":/app zauberzeug/nicegui
                        ```
                    ''')
