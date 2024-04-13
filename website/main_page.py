from nicegui import context, ui

from . import documentation, example_card, svg
from .examples import examples
from .header import add_head_html, add_header
from .style import example_link, features, heading, link_target, section_heading, subtitle, title


def create() -> None:
    """Create the content of the main page."""
    context.get_client().content.classes('p-0 gap-0')
    add_head_html()
    add_header()

    with ui.row().classes('w-full h-screen items-center gap-8 pr-4 no-wrap into-section'):
        svg.face(half=True).classes('stroke-black dark:stroke-white w-[200px] md:w-[230px] lg:w-[300px]')
        with ui.column().classes('gap-4 md:gap-8 pt-32'):
            title('Meet the *NiceGUI*.')
            subtitle('And let any browser be the frontend of your Python code.') \
                .classes('max-w-[20rem] sm:max-w-[24rem] md:max-w-[30rem]')
            ui.link(target='#about').classes('scroll-indicator')

    with ui.row().classes('''
            dark-box min-h-screen no-wrap
            justify-center items-center flex-col md:flex-row
            py-20 px-8 lg:px-16
            gap-8 sm:gap-16 md:gap-8 lg:gap-16
        '''):
        link_target('about')
        with ui.column().classes('text-white max-w-4xl'):
            heading('Interact with Python through buttons, dialogs, 3D&nbsp;scenes, plots and much more.')
            with ui.column().classes('gap-2 bold-links arrow-links text-lg'):
                ui.markdown('''
                    NiceGUI manages web development details, letting you focus on Python code for diverse applications,
                    including robotics, IoT solutions, smart home automation, and machine learning.
                    Designed to work smoothly with connected peripherals like webcams and GPIO pins in IoT setups,
                    NiceGUI streamlines the management of all your code in one place.
                    <br><br>
                    With a gentle learning curve, NiceGUI is user-friendly for beginners
                    and offers advanced customization for experienced users,
                    ensuring simplicity for basic tasks and feasibility for complex projects.
                    <br><br><br>
                    Available as
                    [PyPI package](https://pypi.org/project/nicegui/),
                    [Docker image](https://hub.docker.com/r/zauberzeug/nicegui) and on
                    [GitHub](https://github.com/zauberzeug/nicegui).
                ''')
        example_card.create()

    with ui.column().classes('w-full text-lg p-8 lg:p-16 max-w-[1600px] mx-auto'):
        link_target('installation', '-50px')
        section_heading('Installation', 'Get *started*')
        with ui.row().classes('w-full text-lg leading-tight grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-8'):
            with ui.column().classes('w-full max-w-md gap-2'):
                ui.html('<em>1.</em>').classes('text-3xl font-bold fancy-em')
                ui.markdown('Create __main.py__').classes('text-lg')
                with documentation.python_window(classes='w-full h-52'):
                    ui.markdown('''
                        ```python\n
                        from nicegui import ui

                        ui.label('Hello NiceGUI!')

                        ui.run()
                        ```
                    ''')
            with ui.column().classes('w-full max-w-md gap-2'):
                ui.html('<em>2.</em>').classes('text-3xl font-bold fancy-em')
                ui.markdown('Install and launch').classes('text-lg')
                with documentation.bash_window(classes='w-full h-52'):
                    ui.markdown('''
                        ```bash
                        pip3 install nicegui
                        python3 main.py
                        ```
                    ''')
            with ui.column().classes('w-full max-w-md gap-2'):
                ui.html('<em>3.</em>').classes('text-3xl font-bold fancy-em')
                ui.markdown('Enjoy!').classes('text-lg')
                with documentation.browser_window(classes='w-full h-52'):
                    ui.label('Hello NiceGUI!')
        with ui.expansion('...or use Docker to run your main.py').classes('w-full gap-2 bold-links arrow-links'):
            with ui.row().classes('mt-8 w-full justify-center items-center gap-8'):
                ui.markdown('''
                    With our [multi-arch Docker image](https://hub.docker.com/repository/docker/zauberzeug/nicegui)
                    you can start the server without installing any packages.

                    The command searches for `main.py` in in your current directory and makes the app available at http://localhost:8888.
                ''').classes('max-w-xl')
                with documentation.bash_window(classes='max-w-lg w-full h-52'):
                    ui.markdown('''
                        ```bash
                        docker run -it --rm -p 8888:8080 \\
                            -v "$PWD":/app zauberzeug/nicegui
                        ```
                    ''')

    with ui.column().classes('w-full p-8 lg:p-16 bold-links arrow-links max-w-[1600px] mx-auto'):
        link_target('features', '-50px')
        section_heading('Features', 'Code *nicely*')
        with ui.row().classes('w-full text-lg leading-tight grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-8'):
            features('swap_horiz', 'Interaction', [
                'buttons, switches, sliders, inputs, ...',
                'notifications, dialogs and menus',
                'interactive images with SVG overlays',
                'web pages and native window apps',
            ])
            features('space_dashboard', 'Layout', [
                'navigation bars, tabs, panels, ...',
                'grouping with rows, columns, grids and cards',
                'HTML and Markdown elements',
                'flex layout by default',
            ])
            features('insights', 'Visualization', [
                'charts, diagrams, tables, audio/video',
                '3D scenes',
                'straight-forward data binding',
                'built-in timer for data refresh',
            ])
            features('brush', 'Styling', [
                'customizable color themes',
                'custom CSS and classes',
                'modern look with material design',
                '[Tailwind CSS](https://tailwindcss.com/) auto-completion',
            ])
            features('source', 'Coding', [
                'routing for multiple pages',
                'auto-reload on code change',
                'persistent user sessions',
                'built-in testing framework',
            ])
            features('anchor', 'Foundation', [
                'generic [Vue](https://vuejs.org/) to Python bridge',
                'dynamic GUI through [Quasar](https://quasar.dev/)',
                'content is served with [FastAPI](http://fastapi.tiangolo.com/)',
                'Python 3.8+',
            ])

    with ui.column().classes('w-full p-8 lg:p-16 max-w-[1600px] mx-auto'):
        link_target('demos', '-50px')
        section_heading('Demos', 'Try *this*')
        with ui.column().classes('w-full'):
            documentation.create_intro()

    with ui.column().classes('dark-box p-8 lg:p-16 my-16'):
        with ui.column().classes('mx-auto items-center gap-y-8 gap-x-32 lg:flex-row'):
            with ui.column().classes('gap-1 max-lg:items-center max-lg:text-center'):
                ui.markdown('Browse through plenty of live demos.') \
                    .classes('text-white text-2xl md:text-3xl font-medium')
                ui.html('Fun-Fact: This whole website is also coded with NiceGUI.') \
                    .classes('text-white text-lg md:text-xl')
            ui.link('Documentation', '/documentation').style('color: black !important') \
                .classes('rounded-full mx-auto px-12 py-2 bg-white font-medium text-lg md:text-xl')

    with ui.column().classes('w-full p-8 lg:p-16 max-w-[1600px] mx-auto'):
        link_target('examples', '-50px')
        section_heading('In-depth examples', 'Pick your *solution*')
        with ui.row().classes('w-full text-lg leading-tight grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4'):
            for example in examples:
                example_link(example)

    with ui.row().classes('dark-box min-h-screen mt-16'):
        link_target('why')
        with ui.column().classes('''
                max-w-[1600px] m-auto
                py-20 px-8 lg:px-16
                items-center justify-center no-wrap flex-col md:flex-row gap-16
            '''):
            with ui.column().classes('gap-8'):
                heading('Why?')
                with ui.column().classes('gap-2 text-xl text-white bold-links arrow-links'):
                    ui.markdown('''
                        We at
                        [Zauberzeug](https://zauberzeug.com)
                        like
                        [Streamlit](https://streamlit.io/)
                        but find it does
                        [too much magic](https://github.com/zauberzeug/nicegui/issues/1#issuecomment-847413651)
                        when it comes to state handling.
                        In search for an alternative nice library to write simple graphical user interfaces in Python we discovered
                        [JustPy](https://justpy.io/).
                        Although we liked the approach, it is too "low-level HTML" for our daily usage.
                        But it inspired us to use
                        [Vue](https://vuejs.org/)
                        and
                        [Quasar](https://quasar.dev/)
                        for the frontend.
                    ''')
                    ui.markdown('''
                        We have built on top of
                        [FastAPI](https://fastapi.tiangolo.com/),
                        which itself is based on the ASGI framework
                        [Starlette](https://www.starlette.io/)
                        and the ASGI webserver
                        [Uvicorn](https://www.uvicorn.org/)
                        because of their great performance and ease of use.
                    ''')
            svg.face().classes('stroke-white shrink-0 w-[200px] md:w-[300px] lg:w-[450px]')
