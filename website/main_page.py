from nicegui import context, ui

from . import documentation, example_card, svg
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
                ui.html('<em>1.</em>').classes('text-3xl font-bold')
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
                ui.html('<em>2.</em>').classes('text-3xl font-bold')
                ui.markdown('Install and launch').classes('text-lg')
                with documentation.bash_window(classes='w-full h-52'):
                    ui.markdown('''
                        ```bash
                        pip3 install nicegui
                        python3 main.py
                        ```
                    ''')
            with ui.column().classes('w-full max-w-md gap-2'):
                ui.html('<em>3.</em>').classes('text-3xl font-bold')
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
                'charts, diagrams and tables',
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
                'Jupyter notebook compatibility',
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
            example_link('Slideshow', 'implements a keyboard-controlled image slideshow')
            example_link('Authentication', 'shows how to use sessions to build a login screen')
            example_link('Modularization',
                         'provides an example of how to modularize your application into multiple files and reuse code')
            example_link('FastAPI', 'illustrates the integration of NiceGUI with an existing FastAPI application')
            example_link('Map',
                         'demonstrates wrapping the JavaScript library [leaflet](https://leafletjs.com/) '
                         'to display a map at specific locations')
            example_link('AI Interface',
                         'utilizes the [replicate](https://replicate.com) library to perform voice-to-text '
                         'transcription and generate images from prompts with Stable Diffusion')
            example_link('3D Scene', 'creates a webGL view and loads an STL mesh illuminated with a spotlight')
            example_link('Custom Vue Component', 'shows how to write and integrate a custom Vue component')
            example_link('Image Mask Overlay', 'shows how to overlay an image with a mask')
            example_link('Infinite Scroll', 'presents an infinitely scrolling image gallery')
            example_link('OpenCV Webcam', 'uses OpenCV to capture images from a webcam')
            example_link('SVG Clock', 'displays an analog clock by updating an SVG with `ui.timer`')
            example_link('Progress', 'demonstrates a progress bar for heavy computations')
            example_link('NGINX Subpath', 'shows the setup to serve an app behind a reverse proxy subpath')
            example_link('Script Executor', 'executes scripts on selection and displays the output')
            example_link('Local File Picker', 'demonstrates a dialog for selecting files locally on the server')
            example_link('Search as you type', 'using public API of thecocktaildb.com to search for cocktails')
            example_link('Menu and Tabs', 'uses Quasar to create foldable menu and tabs inside a header bar')
            example_link('Todo list', 'shows a simple todo list with checkboxes and text input')
            example_link('Trello Cards', 'shows Trello-like cards that can be dragged and dropped into columns')
            example_link('Slots', 'shows how to use scoped slots to customize Quasar elements')
            example_link('Table and slots', 'shows how to use component slots in a table')
            example_link('Single Page App', 'navigate without reloading the page')
            example_link('Chat App', 'a simple chat app')
            example_link('Chat with AI', 'a simple chat app with AI')
            example_link('SQLite Database', 'CRUD operations on a SQLite database with async-support through Tortoise ORM')
            example_link('Pandas DataFrame', 'displays an editable [pandas](https://pandas.pydata.org) DataFrame')
            example_link('Lightbox', 'A thumbnail gallery where each image can be clicked to enlarge')
            example_link('ROS2', 'Using NiceGUI as web interface for a ROS2 robot')
            example_link('Docker Image',
                         'Demonstrate using the official '
                         '[zauberzeug/nicegui](https://hub.docker.com/r/zauberzeug/nicegui) docker image')
            example_link('Download Text as File', 'providing in-memory data like strings as file download')
            example_link('Generate PDF', 'create SVG preview and PDF download from input form elements')
            example_link('Custom Binding', 'create a custom binding for a label with a bindable background color')
            example_link('Descope Auth', 'login form and user profile using [Descope](https://descope.com)')
            example_link('Editable table', 'editable table allowing to add, edit, delete rows')
            example_link('Editable AG Grid', 'editable AG Grid allowing to add, edit, delete rows')

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
