#!/usr/bin/env python3
from pathlib import Path

from pygments.formatters import HtmlFormatter

from nicegui import Client, ui
from website import demo_card, reference, svg
from website.example import bash_window, browser_window, python_window
from website.style import example_link, features, header_link, heading, link_target, section_heading, subtitle, title

ui.add_static_files('/favicon', Path(__file__).parent / 'website' / 'favicon')


def add_head_html() -> None:
    ui.add_head_html((Path(__file__).parent / 'website' / 'static' / 'header.html').read_text())
    ui.add_head_html(f'<style>{HtmlFormatter(nobackground=True).get_style_defs(".codehilite")}</style>')
    ui.add_head_html(f"<style>{(Path(__file__).parent / 'website' / 'static' / 'style.css').read_text()}</style>")


def add_header() -> None:
    with ui.header() \
            .classes('items-center duration-200 p-0 px-4') \
            .style('box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1)'):
        with ui.link(target=index_page).classes('row gap-4 items-center'):
            svg.face().classes('w-8 stroke-white stroke-2')
            svg.word().classes('w-24')
        with ui.row().classes('items-center ml-auto'):
            header_link('Features', '/#features')
            header_link('Installation', '/#installation')
            header_link('Examples', '/#examples')
            header_link('API Reference', reference_page)
            header_link('Demos', '/#demos')
            header_link('Why?', '/#why')
            with ui.link(target='https://github.com/zauberzeug/nicegui/'):
                svg.github().classes('fill-white scale-125 m-1')


@ui.page('/')
async def index_page(client: Client):
    client.content.classes(remove='q-pa-md gap-4')
    add_head_html()
    add_header()

    with ui.row().classes('w-full h-screen items-center gap-16 no-wrap').style(f'transform: translateX(-250px)'):
        svg.face().classes('stroke-black w-[500px]')
        with ui.column().classes('gap-8'):
            title('Meet the *NiceGUI*.')
            subtitle('And let any browser be the frontend\n\nof your Python code.')
            with ui.link(target='#about') \
                    .classes('column mt-6 items-center ml-[-12px] hover:translate-y-1 duration-100 ease-out'):
                ui.icon('keyboard_arrow_down').classes('text-4xl text-grey-5 mb-[-0.95em]')
                ui.icon('keyboard_arrow_down').classes('text-6xl text-black')
                ui.icon('keyboard_arrow_down').classes('text-4xl text-grey-5 mt-[-0.85em]')

    with ui.row().classes('dark-box h-screen items-center gap-28 p-32 no-wrap'):
        link_target('about')
        with ui.column().classes('gap-6 text-white'):
            heading('Interact with Python through buttons, dialogs, 3D scenes, plots and much more.')
            with ui.column().classes('gap-2 text-xl bold-links arrow-links'):
                ui.markdown(
                    'NiceGUI handles all the web development details for you. '
                    'So you can focus on writing Python code. '
                    'Anything from short scripts and dashboards to full robotics projects, IoT solutions, '
                    'smart home automations and machine learning projects can benefit from having all code in one place.'
                )
                ui.markdown(
                    'Available as '
                    '[PyPI package](https://pypi.org/project/nicegui/), '
                    '[Docker image](https://hub.docker.com/r/zauberzeug/nicegui) and on '
                    '[GitHub](https://github.com/zauberzeug/nicegui).')
        demo_card.create()

    with ui.column().classes('w-full q-pa-xl q-mb-xl bold-links'):
        link_target('features', '-50px')
        section_heading('Features', 'Code *nicely*')
        with ui.row().classes('w-full no-wrap text-lg leading-tight justify-between q-mb-xl'):
            features('swap_horiz', 'Interaction', [
                'buttons, switches, sliders, inputs, ...',
                'notifications, dialogs and menus',
                'keyboard input',
                'on-screen joystick',
            ])
            features('space_dashboard', 'Layout', [
                'navigation bars, tabs, panels, ...',
                'grouping with rows, columns and cards',
                'HTML and markdown elements',
                'flex layout by default',
            ])
            features('insights', 'Visualization', [
                'charts, diagrams and tables',
                '3D scenes',
                'progress bars',
                'built-in timer for data refresh',
            ])
        with ui.row().classes('w-full no-wrap text-lg leading-tight justify-between'):
            features('brush', 'Styling', [
                'customizable color themes',
                'custom CSS and classes',
                'modern look with material design',
                'built-in [Tailwind](https://tailwindcss.com/) support',
            ])
            features('source', 'Coding', [
                'live-cycle events',
                'implicit reload on code change',
                'straight-forward data binding',
                'execute javascript from Python',
            ])
            features('anchor', 'Foundation', [
                'generic [Vue](https://vuejs.org/) to Python bridge',
                'dynamic GUI through [Quasar](https://quasar.dev/)',
                'content is served with [FastAPI](http://fastapi.tiangolo.com/)',
                'Python 3.7+',
            ])

    with ui.column().classes('w-full q-pa-xl q-mb-xl'):
        link_target('installation', '-50px')
        section_heading('Installation', 'Get *started*')
        with ui.row().classes('w-full no-wrap text-lg leading-tight'):
            with ui.column().classes('w-1/3 gap-2'):
                ui.html('<em>1.</em>').classes('text-3xl text-bold')
                ui.markdown('Create __main.py__').classes('text-lg')
                with python_window().classes('w-full h-52'):
                    ui.markdown('''```python\n
from nicegui import ui

ui.label('Hello NiceGUI!')

ui.run()
```''')
            with ui.column().classes('w-1/3 gap-2'):
                ui.html('<em>2.</em>').classes('text-3xl text-bold')
                ui.markdown('Install and launch').classes('text-lg')
                with bash_window().classes('w-full h-52'):
                    ui.markdown('```bash\npip3 install nicegui\npython3 main.py\n```')
            with ui.column().classes('w-1/3 gap-2'):
                ui.html('<em>3.</em>').classes('text-3xl text-bold')
                ui.markdown('Enjoy').classes('text-lg')
                with browser_window().classes('w-full h-52'):
                    ui.label('Hello NiceGUI!')

    with ui.column().classes('w-full q-pa-xl q-mb-xl'):
        link_target('examples', '-50px')
        section_heading('Examples', 'Try *this*')
        with ui.row().classes('justify-center w-full'), ui.column().classes('w-[65rem]'):
            reference.create_intro()

    with ui.row().classes('dark-box items-center gap-28 px-32 py-16'):
        with ui.column().classes('gap-2'):
            ui.markdown('Browse through plenty of live examples.').classes('text-3xl text-white font-medium')
            ui.html('Fun-Fact: This whole website is also coded with NiceGUI.').classes('text-xl text-white')
        ui.link('API reference', '/reference').classes('rounded-full mx-auto px-12 py-2 text-xl text-bold bg-white')

    with ui.column().classes('w-full q-pa-xl q-mb-xl'):
        link_target('demos', '-50px')
        section_heading('In-depth demonstrations', 'Pick your *solution*')
        with ui.row().classes('w-full no-wrap text-lg leading-tight'):
            with ui.column().classes('w-1/3'):
                example_link('Slideshow', 'implements a keyboard-controlled image slideshow')
                example_link('Authentication', 'shows how to use sessions to build a login screen')
                example_link(
                    'Modularization',
                    'provides an example of how to modularize your application into multiple files and reuse code')
                example_link(
                    'FastAPI',
                    'illustrates the integration of NiceGUI with an existing FastAPI application')
            with ui.column().classes('w-1/3'):
                example_link(
                    'Map',
                    'demonstrates wrapping the JavaScript library leaflet to display a map at specific locations')
                example_link(
                    'AI Interface',
                    'utilizes the [replicate](https://replicate.com) library to perform voice-to-text transcription and generate images from prompts with Stable Diffusion')
                example_link('3D Scene', 'creates a webGL view and loads an STL mesh illuminated with a spotlight')
            with ui.column().classes('w-1/3'):
                example_link('Custom Vue Component', 'shows how to write and integrate a custom vue component')
                example_link('Image Mask Overlay', 'shows how to overlay an image with a mask')
                example_link('Infinite Scroll', 'presents an infinitely scrolling image gallery')

    with ui.row().classes('dark-box h-screen items-center gap-28 p-32 no-wrap'):
        link_target('why')
        with ui.column().classes('gap-8'):
            heading('Why?')
            with ui.column().classes('gap-2 text-xl text-white bold-links arrow-links'):
                ui.markdown(
                    'We like '
                    '[Streamlit](https://streamlit.io/) '
                    'but find it does '
                    '[too much magic](https://github.com/zauberzeug/nicegui/issues/1#issuecomment-847413651) '
                    'when it comes to state handling. '
                    'In search for an alternative nice library to write simple graphical user interfaces in Python we discovered '
                    '[JustPy](https://justpy.io/). '
                    'Although we liked the approach, it is too "low-level HTML" for our daily usage. '
                    'But it inspired us to use '
                    '[Vue](https://vuejs.org/) '
                    'and '
                    '[Quasar](https://quasar.dev/) '
                    'for the frontend.')
                ui.markdown(
                    'We have built on top of '
                    '[FastAPI](https://fastapi.tiangolo.com/), '
                    'which itself is based on the ASGI framework '
                    '[Starlette](https://www.starlette.io/), '
                    'and the ASGI webserver '
                    '[Uvicorn](https://www.uvicorn.org/) '
                    'because of their great performance and ease of use.'
                )
        svg.face().classes('stroke-white w-[1500px]')


@ui.page('/reference')
def reference_page():
    add_head_html()
    add_header()
    reference.create_full()


ui.run(uvicorn_reload_includes='*.py, *.css, *.html')
