import json
from pathlib import Path

from nicegui import ui

from . import documentation, example_card, svg
from .examples import examples
from .i18n import get_url_prefix, t
from .style import example_link, features, heading, link_target, section_heading, subtitle, title

SPONSORS = json.loads((Path(__file__).parent / 'sponsors.json').read_text(encoding='utf-8'))


def create() -> None:
    """Create the content of the main page."""
    prefix = get_url_prefix()

    with ui.row().classes('w-full h-screen max-h-[200vw] items-center gap-8 pr-4 no-wrap into-section'):
        svg.face(half=True).classes('stroke-black dark:stroke-white w-[200px] md:w-[230px] lg:w-[300px]')
        with ui.column().classes('gap-4 md:gap-8 pt-32'):
            title(t('Meet the *NiceGUI*.'))
            subtitle(t('And let any browser be the frontend of your Python code.')) \
                .classes('max-w-[20rem] sm:max-w-[24rem] md:max-w-[30rem]')
            ui.link(target='#about').classes('scroll-indicator')

    with ui.row().classes('''
            dark-box min-h-screen no-wrap
            justify-center items-center flex-col md:flex-row
            py-20 px-8 lg:px-16
            gap-8 sm:gap-16 md:gap-8 lg:gap-16
        '''):
        link_target('about', '70px')
        with ui.column().classes('text-white max-w-4xl'):
            heading(t('Interact with Python through buttons, dialogs, 3D&nbsp;scenes, plots and much more.'))
            with ui.column().classes('gap-2 bold-links arrow-links text-lg'):
                ui.markdown(t(
                    'NiceGUI manages web development details, letting you focus on Python code for diverse applications,\n'
                    'including robotics, IoT solutions, smart home automation, and machine learning.\n'
                    'Designed to work smoothly with connected peripherals like webcams and GPIO pins in IoT setups,\n'
                    'NiceGUI streamlines the management of all your code in one place.\n'
                    '<br><br>\n'
                    'With a gentle learning curve, NiceGUI is user-friendly for beginners\n'
                    'and offers advanced customization for experienced users,\n'
                    'ensuring simplicity for basic tasks and feasibility for complex projects.\n'
                    '<br><br><br>\n'
                    'Available as\n'
                    '[PyPI package](https://pypi.org/project/nicegui/),\n'
                    '[Docker image](https://hub.docker.com/r/zauberzeug/nicegui) and on\n'
                    '[GitHub](https://github.com/zauberzeug/nicegui).'
                ))
        example_card.create()

    with ui.column().classes('w-full text-lg p-8 lg:p-16 max-w-[1600px] mx-auto'):
        link_target('installation')
        section_heading(t('Installation'), t('Get *started*'))
        with ui.row().classes('w-full text-lg leading-tight grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-8'):
            with ui.column().classes('w-full max-w-md gap-2'):
                ui.html('<em>1.</em>', sanitize=False).classes('text-3xl font-bold fancy-em')
                ui.markdown(t('Create __main.py__')).classes('text-lg')
                with documentation.python_window(classes='w-full h-52'):
                    ui.markdown('''
                        ```python\n
                        from nicegui import ui

                        ui.label('Hello NiceGUI!')

                        ui.run()
                        ```
                    ''')
            with ui.column().classes('w-full max-w-md gap-2'):
                ui.html('<em>2.</em>', sanitize=False).classes('text-3xl font-bold fancy-em')
                ui.markdown(t('Install and launch')).classes('text-lg')
                with documentation.bash_window(classes='w-full h-52'):
                    ui.markdown('''
                        ```bash
                        pip3 install nicegui
                        python3 main.py
                        ```
                    ''')
            with ui.column().classes('w-full max-w-md gap-2'):
                ui.html('<em>3.</em>', sanitize=False).classes('text-3xl font-bold fancy-em')
                ui.markdown(t('Enjoy!')).classes('text-lg')
                with documentation.browser_window(classes='w-full h-52'):
                    ui.label('Hello NiceGUI!')
        with ui.expansion(t('...or use Docker to run your main.py')).classes('w-full gap-2 bold-links arrow-links'):
            with ui.row().classes('mt-8 w-full justify-center items-center gap-8'):
                ui.markdown(t(
                    'With our [multi-arch Docker image](https://hub.docker.com/repository/docker/zauberzeug/nicegui)\n'
                    'you can start the server without installing any packages.\n'
                    '\n'
                    'The command searches for `main.py` in in your current directory and makes the app available at http://localhost:8888.'
                )).classes('max-w-xl')
                with documentation.bash_window(classes='max-w-lg w-full h-52'):
                    ui.markdown('''
                        ```bash
                        docker run -it --rm -p 8888:8080 \\
                            -v "$PWD":/app zauberzeug/nicegui
                        ```
                    ''')

    with ui.column().classes('w-full p-8 lg:p-16 bold-links arrow-links max-w-[1600px] mx-auto'):
        link_target('features')
        section_heading(t('Features'), t('Code *nicely*'))
        with ui.row().classes('w-full text-lg leading-tight grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-8'):
            features('swap_horiz', t('Interaction'), [
                t('[buttons, switches, sliders, inputs, ...](/documentation/section_controls)'),
                t('[notifications, dialogs and menus](/documentation/section_page_layout)'),
                t('[interactive images](/documentation/interactive_image) with SVG overlays'),
                t('web pages and [native window apps](/documentation/section_configuration_deployment#native_mode)'),
            ])
            features('space_dashboard', t('Layout'), [
                t('[navigation bars, tabs, panels, ...](/documentation/section_page_layout)'),
                t('grouping with rows, columns, grids and cards'),
                t('[HTML](/documentation/html) and [Markdown](/documentation/markdown) elements'),
                t('flex layout by default'),
            ])
            features('insights', t('Visualization'), [
                t('[charts, diagrams, tables](/documentation/section_data_elements), [audio/video](/documentation/section_audiovisual_elements)'),
                t('[3D scenes](/documentation/scene)'),
                t('straight-forward [data binding](/documentation/section_binding_properties)'),
                t('built-in [timer for data refresh](/documentation/timer)'),
            ])
            features('brush', t('Styling'), [
                t('customizable [color themes](/documentation/section_styling_appearance#color_theming)'),
                t('custom CSS and classes'),
                t('modern look with material design'),
                '[Tailwind CSS](https://tailwindcss.com/)',
            ])
            features('source', t('Coding'), [
                t('single page apps with [ui.sub_pages](/documentation/sub_pages)'),
                t('auto-reload on code change'),
                t('persistent [user sessions](/documentation/storage)'),
                t('super powerful [testing framework](/documentation/section_testing)'),
            ])
            features('anchor', t('Foundation'), [
                t('generic [Vue](https://vuejs.org/) to Python bridge'),
                t('dynamic GUI through [Quasar](https://quasar.dev/)'),
                t('content is served with [FastAPI](https://fastapi.tiangolo.com/)'),
                'Python 3.10+',
            ])

    with ui.column().classes('w-full p-8 lg:p-16 max-w-[1600px] mx-auto'):
        link_target('demos')
        section_heading(t('Demos'), t('Try *this*'))
        with ui.column().classes('w-full'):
            documentation.create_intro()

    with ui.column().classes('dark-box p-8 lg:p-16 my-16'):
        with ui.column().classes('mx-auto items-center gap-y-8 gap-x-32 lg:flex-row'):
            with ui.column().classes('gap-1 max-lg:items-center max-lg:text-center'):
                ui.markdown(t('Browse through plenty of live demos.')) \
                    .classes('text-white text-2xl md:text-3xl font-medium')
                ui.label(t('Fun-Fact: This whole website is also coded with NiceGUI.')) \
                    .classes('text-white text-lg md:text-xl')
            ui.link(t('Documentation'), f'{prefix}/documentation').style('color: black !important') \
                .classes('rounded-full mx-auto px-12 py-2 bg-white font-medium text-lg md:text-xl')

    with ui.column().classes('w-full p-8 lg:p-16 max-w-[1600px] mx-auto'):
        link_target('examples')
        section_heading(t('In-depth examples'), t('Pick your *solution*'))
        with ui.row().classes('w-full text-lg leading-tight grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4'):
            for example in examples:
                if example.title in {'Authentication', 'Chat App', 'Todo List'}:
                    example_link(example)
            example_link().classes('min-h-40 text-center items-center justify-center xl:col-span-3')

    with ui.column().classes('dark-box p-8 lg:p-16 my-16 bg-transparent border-y-2 border-gray-200'):
        with ui.column().classes('mx-auto items-center gap-y-8 gap-x-32 lg:flex-row'):
            with ui.column().classes('max-lg:items-center max-lg:text-center gap-8'):
                link_target('sponsors')
                ui.markdown(t('NiceGUI is supported by')) \
                    .classes('text-2xl md:text-3xl font-medium')
                if SPONSORS['special'] or SPONSORS['top']:
                    with ui.row().classes('gap-8 justify-center'):
                        for sponsor in SPONSORS['special']:
                            with ui.link(target=SPONSORS['special'][sponsor]):
                                img_path = Path(__file__).parent / 'static' / 'sponsors' / f'{sponsor}.webp'
                                if img_path.exists():
                                    ui.interactive_image(f'/static/sponsors/{sponsor}.webp').classes('h-12')
                                else:
                                    ui.interactive_image(f'/static/sponsors/{sponsor}.light.webp') \
                                        .classes('h-12 block dark:!hidden')
                                    ui.interactive_image(f'/static/sponsors/{sponsor}.dark.webp') \
                                        .classes('h-12 hidden dark:!block')
                        for sponsor in SPONSORS['top']:
                            with ui.link(target=f'https://github.com/{sponsor}').classes('row items-center gap-2'):
                                ui.image(f'https://github.com/{sponsor}.png').classes('w-12 h-12 border')
                                ui.label(f'@{sponsor}')
                    ui.markdown(f'''
                        as well as {SPONSORS['normal']} other [sponsors](https://github.com/sponsors/zauberzeug)
                        and {SPONSORS['contributors']} [contributors](https://github.com/zauberzeug/nicegui/graphs/contributors).
                    ''').classes('bold-links arrow-links')
                else:
                    ui.markdown(f'''
                        {SPONSORS['normal']} [sponsors](https://github.com/sponsors/zauberzeug)
                        and {SPONSORS['contributors']} [contributors](https://github.com/zauberzeug/nicegui/graphs/contributors).
                    ''').classes('bold-links arrow-links')
            with ui.link(target='https://github.com/sponsors/zauberzeug').style('color: black !important') \
                    .classes('rounded-full mx-auto px-12 py-2 border-2 border-[#3e6a94] font-medium text-lg md:text-xl'):
                with ui.row(wrap=False).classes('items-center gap-4'):
                    ui.icon('favorite_border', color='#3e6a94')
                    ui.label(t('Become a sponsor')).classes('text-[#3e6a94] whitespace-nowrap')

    with ui.row().classes('dark-box min-h-screen mt-16'):
        link_target('why', '70px')
        with ui.column().classes('''
                max-w-[1600px] m-auto
                py-20 px-8 lg:px-16
                items-center justify-center no-wrap flex-col md:flex-row gap-16
            '''):
            with ui.column().classes('gap-8'):
                heading(t('Why?'))
                with ui.column().classes('gap-2 text-xl text-white bold-links arrow-links'):
                    ui.markdown(t(
                        'We at\n'
                        '[Zauberzeug](https://zauberzeug.com)\n'
                        'like\n'
                        '[Streamlit](https://streamlit.io/)\n'
                        'but find it does\n'
                        '[too much magic](https://github.com/zauberzeug/nicegui/issues/1#issuecomment-847413651)\n'
                        'when it comes to state handling.\n'
                        'In search for an alternative nice library to write simple graphical user interfaces in Python we discovered\n'
                        '[JustPy](https://justpy.io/).\n'
                        'Although we liked the approach, it is too "low-level HTML" for our daily usage.\n'
                        'But it inspired us to use\n'
                        '[Vue](https://vuejs.org/)\n'
                        'and\n'
                        '[Quasar](https://quasar.dev/)\n'
                        'for the frontend.'
                    ))
                    ui.markdown(t(
                        'We have built on top of\n'
                        '[FastAPI](https://fastapi.tiangolo.com/),\n'
                        'which itself is based on the ASGI framework\n'
                        '[Starlette](https://www.starlette.io/)\n'
                        'and the ASGI webserver\n'
                        '[Uvicorn](https://www.uvicorn.org/)\n'
                        'because of their great performance and ease of use.'
                    ))
            svg.face().classes('stroke-white shrink-0 w-[200px] md:w-[300px] lg:w-[450px]')
        with ui.column().classes('w-full p-4 items-end text-white self-end'):
            ui.link(t('Imprint & Privacy'), f'{prefix}/imprint_privacy').classes('text-sm')
