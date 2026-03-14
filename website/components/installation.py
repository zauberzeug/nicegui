from nicegui import ui

from .. import documentation
from ..style import link_target


def _code_window(filename: str, icon: str, code_html: str) -> None:
    """Create a styled code window with filename header."""
    with ui.element('div').classes('mo-code-window'):
        with ui.element('div').classes('mo-code-header'):
            ui.html(
                f'<span class="mo-code-filename">'
                f'<i class="material-icons" style="font-size:1rem">{icon}</i> {filename}'
                f'</span>',
                sanitize=False,
            )
        ui.html(f'<div class="mo-code-body">{code_html}</div>', sanitize=False)


def _browser_window(content_html: str) -> None:
    """Create a styled browser preview window."""
    with ui.element('div').classes('mo-browser-window'):
        with ui.element('div').classes('mo-browser-header'):
            ui.html(
                '<span class="mo-browser-tab">'
                '<i class="material-icons" style="font-size:1rem">language</i> localhost:8080'
                '</span>',
                sanitize=False,
            )
        ui.html(f'<div class="mo-browser-content">{content_html}</div>', sanitize=False)


def create() -> None:
    """Create the installation section with 3-step flow and Docker expansion."""
    with ui.element('section').classes('mo-section').props('id=installation'):
        link_target('installation')
        with ui.element('div').classes('mo-reveal'):
            ui.html('<div class="mo-section-label">get_started</div>', sanitize=False)
            ui.html('<h2 class="mo-section-title">Three lines to a running app.</h2>', sanitize=False)
            ui.html('<p class="mo-section-desc">Write a Python file, install and run — that\'s it.</p>', sanitize=False)

        with ui.element('div').classes('mo-install-steps mo-reveal'):
            # Step 1: Write
            with ui.element('div').classes('mo-install-step'):
                ui.html(
                    '<div class="mo-step-number"><span class="mo-step-num">1</span> Write</div>',
                    sanitize=False,
                )
                _code_window('main.py', 'description', (
                    '<span class="kw">from</span> nicegui <span class="kw">import</span> ui\n'
                    'ui.label(<span class="str">\'Hello NiceGUI!\'</span>)\n'
                    'ui.run()'
                ))

            # Step 2: Run
            with ui.element('div').classes('mo-install-step'):
                ui.html(
                    '<div class="mo-step-number"><span class="mo-step-num">2</span> Run</div>',
                    sanitize=False,
                )
                _code_window('bash', 'terminal', (
                    '<span class="op">$</span> pip3 install nicegui\n'
                    '<span class="op">$</span> python3 main.py'
                ))

            # Step 3: Enjoy
            with ui.element('div').classes('mo-install-step'):
                ui.html(
                    '<div class="mo-step-number"><span class="mo-step-num">3</span> Enjoy</div>',
                    sanitize=False,
                )
                _browser_window(
                    '<div style="font-size:1rem; margin-bottom:10px">Hello NiceGUI!</div>'
                    '<button style="padding:5px 14px; border-radius:6px; '
                    'background:var(--mo-brand-blue); color:white; border:none; '
                    'font-size:0.8125rem; cursor:pointer; font-family:inherit">Button</button>'
                )

        # Docker expansion
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
