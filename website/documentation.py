import uuid

from nicegui import app, events, ui
from nicegui.globals import optional_features

from . import demo
from .documentation_tools import element_demo, heading, intro_demo, load_demo, subheading, text_demo

CONSTANT_UUID = str(uuid.uuid4())


def create_intro() -> None:
    @intro_demo('Styling',
                'While having reasonable defaults, you can still modify the look of your app with CSS as well as Tailwind and Quasar classes.')
    def formatting_demo():
        ui.icon('thumb_up')
        ui.markdown('This is **Markdown**.')
        ui.html('This is <strong>HTML</strong>.')
        with ui.row():
            ui.label('CSS').style('color: #888; font-weight: bold')
            ui.label('Tailwind').classes('font-serif')
            ui.label('Quasar').classes('q-ml-xl')
        ui.link('NiceGUI on GitHub', 'https://github.com/zauberzeug/nicegui')

    @intro_demo('Common UI Elements',
                'NiceGUI comes with a collection of commonly used UI elements.')
    def common_elements_demo():
        from nicegui.events import ValueChangeEventArguments

        def show(event: ValueChangeEventArguments):
            name = type(event.sender).__name__
            ui.notify(f'{name}: {event.value}')

        ui.button('Button', on_click=lambda: ui.notify('Click'))
        with ui.row():
            ui.checkbox('Checkbox', on_change=show)
            ui.switch('Switch', on_change=show)
        ui.radio(['A', 'B', 'C'], value='A', on_change=show).props('inline')
        with ui.row():
            ui.input('Text input', on_change=show)
            ui.select(['One', 'Two'], value='One', on_change=show)
        ui.link('And many more...', '/documentation').classes('mt-8')

    @intro_demo('Value Binding',
                'Binding values between UI elements and data models is built into NiceGUI.')
    def binding_demo():
        class Demo:
            def __init__(self):
                self.number = 1

        demo = Demo()
        v = ui.checkbox('visible', value=True)
        with ui.column().bind_visibility_from(v, 'value'):
            ui.slider(min=1, max=3).bind_value(demo, 'number')
            ui.toggle({1: 'A', 2: 'B', 3: 'C'}).bind_value(demo, 'number')
            ui.number().bind_value(demo, 'number')


def create_full() -> None:
    heading('Basic Elements')
    load_demo(ui.label)
    load_demo(ui.icon)
    load_demo(ui.avatar)
    load_demo(ui.link)
    load_demo(ui.button)
    load_demo(ui.badge)
    load_demo(ui.toggle)
    load_demo(ui.radio)
    load_demo(ui.select)
    load_demo(ui.checkbox)
    load_demo(ui.switch)
    load_demo(ui.slider)
    load_demo(ui.joystick)
    load_demo(ui.input)
    load_demo(ui.textarea)
    load_demo(ui.number)
    load_demo(ui.knob)
    load_demo(ui.color_input)
    load_demo(ui.color_picker)
    load_demo(ui.date)
    load_demo(ui.time)
    load_demo(ui.upload)
    load_demo(ui.chat_message)
    load_demo(ui.element)

    heading('Markdown and HTML')

    load_demo(ui.markdown)
    load_demo(ui.mermaid)
    load_demo(ui.html)

    @text_demo('SVG',
               'You can add Scalable Vector Graphics using the `ui.html` element.')
    def svg_demo():
        content = '''
            <svg viewBox="0 0 200 200" width="100" height="100" xmlns="http://www.w3.org/2000/svg">
            <circle cx="100" cy="100" r="78" fill="#ffde34" stroke="black" stroke-width="3" />
            <circle cx="80" cy="85" r="8" />
            <circle cx="120" cy="85" r="8" />
            <path d="m60,120 C75,150 125,150 140,120" style="fill:none; stroke:black; stroke-width:8; stroke-linecap:round" />
            </svg>'''
        ui.html(content)

    heading('Images, Audio and Video')

    load_demo(ui.image)

    @text_demo('Captions and Overlays', '''
        By nesting elements inside a `ui.image` you can create augmentations.

        Use [Quasar classes](https://quasar.dev/vue-components/img) for positioning and styling captions.
        To overlay an SVG, make the `viewBox` exactly the size of the image and provide `100%` width/height to match the actual rendered size.
    ''')
    def captions_and_overlays_demo():
        with ui.image('https://picsum.photos/id/29/640/360'):
            ui.label('Nice!').classes('absolute-bottom text-subtitle2 text-center')

        with ui.image('https://cdn.stocksnap.io/img-thumbs/960w/airplane-sky_DYPWDEEILG.jpg'):
            ui.html('''
                <svg viewBox="0 0 960 638" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
                <circle cx="445" cy="300" r="100" fill="none" stroke="red" stroke-width="20" />
                </svg>
            ''').classes('bg-transparent')

    load_demo(ui.interactive_image)
    load_demo(ui.audio)
    load_demo(ui.video)

    heading('Data Elements')

    load_demo(ui.table)
    load_demo(ui.aggrid)
    load_demo(ui.chart)
    load_demo(ui.echart)
    if 'matplotlib' in optional_features:
        load_demo(ui.pyplot)
        load_demo(ui.line_plot)
    if 'plotly' in optional_features:
        load_demo(ui.plotly)
    load_demo(ui.linear_progress)
    load_demo(ui.circular_progress)
    load_demo(ui.spinner)
    load_demo(ui.scene)
    load_demo(ui.tree)
    load_demo(ui.log)
    load_demo(ui.editor)
    load_demo(ui.code)
    load_demo(ui.json_editor)

    heading('Layout')

    load_demo(ui.card)
    load_demo(ui.column)
    load_demo(ui.row)
    load_demo(ui.grid)

    @text_demo('Clear Containers', '''
        To remove all elements from a row, column or card container, use can call
        ```py
        container.clear()
        ```

        Alternatively, you can remove individual elements by calling
        
        - `container.remove(element: Element)`,
        - `container.remove(index: int)`, or
        - `element.delete()`.
    ''')
    def clear_containers_demo():
        container = ui.row()

        def add_face():
            with container:
                ui.icon('face')
        add_face()

        ui.button('Add', on_click=add_face)
        ui.button('Remove', on_click=lambda: container.remove(0) if list(container) else None)
        ui.button('Clear', on_click=container.clear)

    load_demo(ui.expansion)
    load_demo(ui.scroll_area)
    load_demo(ui.separator)
    load_demo(ui.splitter)
    load_demo('tabs')
    load_demo(ui.stepper)
    load_demo(ui.timeline)
    load_demo(ui.carousel)
    load_demo(ui.menu)
    load_demo(ui.context_menu)

    @text_demo('Tooltips', '''
        Simply call the `tooltip(text:str)` method on UI elements to provide a tooltip.

        For more artistic control you can nest tooltip elements and apply props, classes and styles.
    ''')
    def tooltips_demo():
        ui.label('Tooltips...').tooltip('...are shown on mouse over')
        with ui.button(icon='thumb_up'):
            ui.tooltip('I like this').classes('bg-green')

    load_demo(ui.notify)
    load_demo(ui.dialog)

    heading('Appearance')

    @text_demo('Styling', '''
        NiceGUI uses the [Quasar Framework](https://quasar.dev/) version 1.0 and hence has its full design power.
        Each NiceGUI element provides a `props` method whose content is passed [to the Quasar component](https://justpy.io/quasar_tutorial/introduction/#props-of-quasar-components):
        Have a look at [the Quasar documentation](https://quasar.dev/vue-components/button#design) for all styling props.
        Props with a leading `:` can contain JavaScript expressions that are evaluated on the client.
        You can also apply [Tailwind CSS](https://tailwindcss.com/) utility classes with the `classes` method.

        If you really need to apply CSS, you can use the `style` method. Here the delimiter is `;` instead of a blank space.

        All three functions also provide `remove` and `replace` parameters in case the predefined look is not wanted in a particular styling.
    ''')
    def design_demo():
        ui.radio(['x', 'y', 'z'], value='x').props('inline color=green')
        ui.button(icon='touch_app').props('outline round').classes('shadow-lg')
        ui.label('Stylish!').style('color: #6E93D6; font-size: 200%; font-weight: 300')

    subheading('Try styling NiceGUI elements!')
    ui.markdown('''
        Try out how
        [Tailwind CSS classes](https://tailwindcss.com/),
        [Quasar props](https://justpy.io/quasar_tutorial/introduction/#props-of-quasar-components),
        and CSS styles affect NiceGUI elements.
    ''').classes('bold-links arrow-links mb-[-1rem]')
    with ui.row():
        ui.label('Select an element from those available and start styling it!').classes('mx-auto my-auto')
        select_element = ui.select({
            ui.label: 'ui.label',
            ui.checkbox: 'ui.checkbox',
            ui.switch: 'ui.switch',
            ui.input: 'ui.input',
            ui.textarea: 'ui.textarea',
            ui.button: 'ui.button',
        }, value=ui.button, on_change=lambda: live_demo_ui.refresh()).props('dense')

    @ui.refreshable
    def live_demo_ui():
        with ui.column().classes('w-full items-stretch gap-8 no-wrap min-[1500px]:flex-row'):
            with demo.python_window(classes='w-full max-w-[44rem]'):
                with ui.column().classes('w-full gap-4'):
                    ui.markdown(f'''
                        ```py
                        from nicegui import ui

                        element = {select_element.options[select_element.value]}('element')
                        ```
                    ''').classes('mb-[-0.25em]')
                    with ui.row().classes('items-center gap-0 w-full px-2'):
                        def handle_classes(e: events.ValueChangeEventArguments):
                            try:
                                element.classes(replace=e.value)
                            except ValueError:
                                pass
                        ui.markdown("`element.classes('`")
                        ui.input(on_change=handle_classes).classes('mt-[-0.5em] text-mono grow').props('dense')
                        ui.markdown("`')`")
                    with ui.row().classes('items-center gap-0 w-full px-2'):
                        def handle_props(e: events.ValueChangeEventArguments):
                            element._props = {'label': 'Button', 'color': 'primary'}
                            try:
                                element.props(e.value)
                            except ValueError:
                                pass
                            element.update()
                        ui.markdown("`element.props('`")
                        ui.input(on_change=handle_props).classes('mt-[-0.5em] text-mono grow').props('dense')
                        ui.markdown("`')`")
                    with ui.row().classes('items-center gap-0 w-full px-2'):
                        def handle_style(e: events.ValueChangeEventArguments):
                            try:
                                element.style(replace=e.value)
                            except ValueError:
                                pass
                        ui.markdown("`element.style('`")
                        ui.input(on_change=handle_style).classes('mt-[-0.5em] text-mono grow').props('dense')
                        ui.markdown("`')`")
                    ui.markdown('''
                        ```py
                        ui.run()
                        ```
                    ''')
            with demo.browser_window(classes='w-full max-w-[44rem] min-[1500px]:max-w-[20rem] min-h-[10rem] browser-window'):
                element: ui.element = select_element.value("element")
    live_demo_ui()

    @text_demo('Tailwind CSS', '''
        [Tailwind CSS](https://tailwindcss.com/) is a CSS framework for rapidly building custom user interfaces.
        NiceGUI provides a fluent, auto-complete friendly interface for adding Tailwind classes to UI elements.
        
        You can discover available classes by navigating the methods of the `tailwind` property.
        The builder pattern allows you to chain multiple classes together (as shown with "Label A").
        You can also call the `tailwind` property with a list of classes (as shown with "Label B").

        Although this is very similar to using the `classes` method, it is more convenient for Tailwind classes due to auto-completion.

        Last but not least, you can also predefine a style and apply it to multiple elements (labels C and D).
    ''')
    def tailwind_demo():
        from nicegui import Tailwind
        ui.label('Label A').tailwind.font_weight('extrabold').text_color('blue-600').background_color('orange-200')
        ui.label('Label B').tailwind('drop-shadow', 'font-bold', 'text-green-600')

        red_style = Tailwind().text_color('red-600').font_weight('bold')
        label_c = ui.label('Label C')
        red_style.apply(label_c)
        ui.label('Label D').tailwind(red_style)

    load_demo(ui.query)
    load_demo(ui.colors)
    load_demo(ui.dark_mode)

    heading('Action')

    load_demo(ui.timer)
    load_demo(ui.keyboard)
    load_demo('bindings')

    @text_demo('UI Updates', '''
        NiceGUI tries to automatically synchronize the state of UI elements with the client, e.g. when a label text, an input value or style/classes/props of an element have changed.
        In other cases, you can explicitly call `element.update()` or `ui.update(*elements)` to update.
        The demo code shows both methods for a `ui.chart`, where it is difficult to automatically detect changes in the `options` dictionary.
    ''')
    def ui_updates_demo():
        from random import randint

        chart = ui.chart({'title': False, 'series': [{'data': [1, 2]}]}).classes('w-full h-64')

        def add():
            chart.options['series'][0]['data'].append(randint(0, 100))
            chart.update()

        def clear():
            chart.options['series'][0]['data'].clear()
            ui.update(chart)

        with ui.row():
            ui.button('Add', on_click=add)
            ui.button('Clear', on_click=clear)

    load_demo(ui.refreshable)

    @text_demo('Async event handlers', '''
        Most elements also support asynchronous event handlers.

        Note: You can also pass a `functools.partial` into the `on_click` property to wrap async functions with parameters.
    ''')
    def async_handlers_demo():
        import asyncio

        async def async_task():
            ui.notify('Asynchronous task started')
            await asyncio.sleep(5)
            ui.notify('Asynchronous task finished')

        ui.button('start async task', on_click=async_task)

    @text_demo('Running CPU-bound tasks', '''
        NiceGUI provides a `cpu_bound` function for running CPU-bound tasks in a separate process.
        This is useful for long-running computations that would otherwise block the event loop and make the UI unresponsive.
        The function returns a future that can be awaited.
    ''')
    def cpu_bound_demo():
        import time

        from nicegui import run

        def compute_sum(a: float, b: float) -> float:
            time.sleep(1)  # simulate a long-running computation
            return a + b

        async def handle_click():
            result = await run.cpu_bound(compute_sum, 1, 2)
            ui.notify(f'Sum is {result}')

        # ui.button('Compute', on_click=handle_click)
        # END OF DEMO
        async def mock_click():
            import asyncio
            await asyncio.sleep(1)
            ui.notify('Sum is 3')
        ui.button('Compute', on_click=mock_click)

    @text_demo('Running I/O-bound tasks', '''
        NiceGUI provides an `io_bound` function for running I/O-bound tasks in a separate thread.
        This is useful for long-running I/O operations that would otherwise block the event loop and make the UI unresponsive.
        The function returns a future that can be awaited.
    ''')
    def io_bound_demo():
        import requests

        from nicegui import run

        async def handle_click():
            URL = 'https://httpbin.org/delay/1'
            response = await run.io_bound(requests.get, URL, timeout=3)
            ui.notify(f'Downloaded {len(response.content)} bytes')

        ui.button('Download', on_click=handle_click)

    heading('Pages')

    load_demo(ui.page)

    @text_demo('Auto-index page', '''
        Pages created with the `@ui.page` decorator are "private".
        Their content is re-created for each client.
        Thus, in the demo to the right, the displayed ID on the private page changes when the browser reloads the page.

        UI elements that are not wrapped in a decorated page function are placed on an automatically generated index page at route "/".
        This auto-index page is created once on startup and *shared* across all clients that might connect.
        Thus, each connected client will see the *same* elements.
        In the demo to the right, the displayed ID on the auto-index page remains constant when the browser reloads the page.
    ''')
    def auto_index_page():
        from uuid import uuid4

        @ui.page('/private_page')
        async def private_page():
            ui.label(f'private page with ID {uuid4()}')

        # ui.label(f'shared auto-index page with ID {uuid4()}')
        # ui.link('private page', private_page)
        # END OF DEMO
        ui.label(f'shared auto-index page with ID {CONSTANT_UUID}')
        ui.link('private page', private_page)

    @text_demo('Page Layout', '''
        With `ui.header`, `ui.footer`, `ui.left_drawer` and `ui.right_drawer` you can add additional layout elements to a page.
        The `fixed` argument controls whether the element should scroll or stay fixed on the screen.
        The `top_corner` and `bottom_corner` arguments indicate whether a drawer should expand to the top or bottom of the page.
        See <https://quasar.dev/layout/header-and-footer> and <https://quasar.dev/layout/drawer> for more information about possible props.
        With `ui.page_sticky` you can place an element "sticky" on the screen.
        See <https://quasar.dev/layout/page-sticky> for more information.
    ''')
    def page_layout_demo():
        @ui.page('/page_layout')
        def page_layout():
            ui.label('CONTENT')
            [ui.label(f'Line {i}') for i in range(100)]
            with ui.header(elevated=True).style('background-color: #3874c8').classes('items-center justify-between'):
                ui.label('HEADER')
                ui.button(on_click=lambda: right_drawer.toggle(), icon='menu').props('flat color=white')
            with ui.left_drawer(top_corner=True, bottom_corner=True).style('background-color: #d7e3f4'):
                ui.label('LEFT DRAWER')
            with ui.right_drawer(fixed=False).style('background-color: #ebf1fa').props('bordered') as right_drawer:
                ui.label('RIGHT DRAWER')
            with ui.footer().style('background-color: #3874c8'):
                ui.label('FOOTER')

        ui.link('show page with fancy layout', page_layout)

    load_demo(ui.open)
    load_demo(ui.download)

    load_demo('storage')

    @text_demo('Parameter injection', '''
        Thanks to FastAPI, a page function accepts optional parameters to provide
        [path parameters](https://fastapi.tiangolo.com/tutorial/path-params/), 
        [query parameters](https://fastapi.tiangolo.com/tutorial/query-params/) or the whole incoming
        [request](https://fastapi.tiangolo.com/advanced/using-request-directly/) for accessing
        the body payload, headers, cookies and more.
    ''')
    def parameter_demo():
        @ui.page('/icon/{icon}')
        def icons(icon: str, amount: int = 1):
            ui.label(icon).classes('text-h3')
            with ui.row():
                [ui.icon(icon).classes('text-h3') for _ in range(amount)]
        ui.link('Star', '/icon/star?amount=5')
        ui.link('Home', '/icon/home')
        ui.link('Water', '/icon/water_drop?amount=3')

    load_demo(ui.run_javascript)

    heading('Routes')

    subheading('Static files')

    @element_demo(app.add_static_files)
    def add_static_files_demo():
        from nicegui import app

        app.add_static_files('/examples', 'examples')
        ui.label('Some NiceGUI Examples').classes('text-h5')
        ui.link('AI interface', '/examples/ai_interface/main.py')
        ui.link('Custom FastAPI app', '/examples/fastapi/main.py')
        ui.link('Authentication', '/examples/authentication/main.py')

    subheading('Media files')

    @element_demo(app.add_media_files)
    def add_media_files_demo():
        from pathlib import Path

        import requests

        from nicegui import app

        media = Path('media')
        # media.mkdir(exist_ok=True)
        # r = requests.get('https://cdn.coverr.co/videos/coverr-cloudy-sky-2765/1080p.mp4')
        # (media  / 'clouds.mp4').write_bytes(r.content)
        # app.add_media_files('/my_videos', media)
        # ui.video('/my_videos/clouds.mp4')
        # END OF DEMO
        ui.video('https://cdn.coverr.co/videos/coverr-cloudy-sky-2765/1080p.mp4')

    @text_demo('API Responses', '''
        NiceGUI is based on [FastAPI](https://fastapi.tiangolo.com/).
        This means you can use all of FastAPI's features.
        For example, you can implement a RESTful API in addition to your graphical user interface.
        You simply import the `app` object from `nicegui`.
        Or you can run NiceGUI on top of your own FastAPI app by using `ui.run_with(app)` instead of starting a server automatically with `ui.run()`.

        You can also return any other FastAPI response object inside a page function.
        For example, you can return a `RedirectResponse` to redirect the user to another page if certain conditions are met.
        This is used in our [authentication demo](https://github.com/zauberzeug/nicegui/tree/main/examples/authentication/main.py).
    ''')
    def fastapi_demo():
        import random

        from nicegui import app

        @app.get('/random/{max}')
        def generate_random_number(max: int):
            return {'min': 0, 'max': max, 'value': random.randint(0, max)}

        max = ui.number('max', value=100)
        ui.button('generate random number', on_click=lambda: ui.open(f'/random/{max.value:.0f}'))

    heading('Lifecycle')

    @text_demo('Events', '''
        You can register coroutines or functions to be called for the following events:

        - `app.on_startup`: called when NiceGUI is started or restarted
        - `app.on_shutdown`: called when NiceGUI is shut down or restarted
        - `app.on_connect`: called for each client which connects (optional argument: nicegui.Client)
        - `app.on_disconnect`: called for each client which disconnects (optional argument: nicegui.Client)
        - `app.on_exception`: called when an exception occurs (optional argument: exception)

        When NiceGUI is shut down or restarted, all tasks still in execution will be automatically canceled.
    ''')
    def lifecycle_demo():
        from datetime import datetime

        from nicegui import app

        # dt = datetime.now()

        def handle_connection():
            global dt
            dt = datetime.now()
        app.on_connect(handle_connection)

        label = ui.label()
        ui.timer(1, lambda: label.set_text(f'Last new connection: {dt:%H:%M:%S}'))
        # END OF DEMO
        global dt
        dt = datetime.now()

    subheading('Shutdown')

    @element_demo(app.shutdown)
    def shutdown_demo():
        from nicegui import app

        # ui.button('shutdown', on_click=app.shutdown)
        #
        # ui.run(reload=False)
        # END OF DEMO
        ui.button('shutdown', on_click=lambda: ui.notify(
            'Nah. We do not actually shutdown the documentation server. Try it in your own app!'))

    @text_demo('URLs', '''
        You can access the list of all URLs on which the NiceGUI app is available via `app.urls`.
        The URLs are not available in `app.on_startup` because the server is not yet running.
        Instead, you can access them in a page function or register a callback with `app.urls.on_change`.
    ''')
    def urls_demo():
        from nicegui import app

        # @ui.page('/')
        # def index():
        #     for url in app.urls:
        #         ui.link(url, target=url)
        # END OF DEMO
        ui.link('https://nicegui.io', target='https://nicegui.io')

    heading('NiceGUI Fundamentals')

    @text_demo('Auto-context', '''
        In order to allow writing intuitive UI descriptions, NiceGUI automatically tracks the context in which elements are created.
        This means that there is no explicit `parent` parameter.
        Instead the parent context is defined using a `with` statement.
        It is also passed to event handlers and timers.

        In the demo, the label "Card content" is added to the card.
        And because the `ui.button` is also added to the card, the label "Click!" will also be created in this context.
        The label "Tick!", which is added once after one second, is also added to the card.

        This design decision allows for easily creating modular components that keep working after moving them around in the UI.
        For example, you can move label and button somewhere else, maybe wrap them in another container, and the code will still work.
    ''')
    def auto_context_demo():
        with ui.card():
            ui.label('Card content')
            ui.button('Add label', on_click=lambda: ui.label('Click!'))
            ui.timer(1.0, lambda: ui.label('Tick!'), once=True)

    load_demo('generic_events')

    heading('Configuration')

    load_demo(ui.run)

    @text_demo('Native Mode', '''
        You can enable native mode for NiceGUI by specifying `native=True` in the `ui.run` function.
        To customize the initial window size and display mode, use the `window_size` and `fullscreen` parameters respectively.
        Additionally, you can provide extra keyword arguments via `app.native.window_args` and `app.native.start_args`.
        Pick any parameter as it is defined by the internally used [pywebview module](https://pywebview.flowrl.com/guide/api.html)
        for the `webview.create_window` and `webview.start` functions.
        Note that these keyword arguments will take precedence over the parameters defined in `ui.run`.

        In native mode the `app.native.main_window` object allows you to access the underlying window.
        It is an async version of [`Window` from pywebview](https://pywebview.flowrl.com/guide/api.html#window-object).
    ''', tab=lambda: ui.label('NiceGUI'))
    def native_mode_demo():
        from nicegui import app

        app.native.window_args['resizable'] = False
        app.native.start_args['debug'] = True

        ui.label('app running in native mode')
        # ui.button('enlarge', on_click=lambda: app.native.main_window.resize(1000, 700))
        #
        # ui.run(native=True, window_size=(400, 300), fullscreen=False)
        # END OF DEMO
        ui.button('enlarge', on_click=lambda: ui.notify('window will be set to 1000x700 in native mode'))

    # Show a helpful workaround until issue is fixed upstream.
    # For more info see: https://github.com/r0x0r/pywebview/issues/1078
    ui.markdown('''
        If webview has trouble finding required libraries, you may get an error relating to "WebView2Loader.dll".
        To work around this issue, try moving the DLL file up a directory, e.g.:
        
        * from `.venv/Lib/site-packages/webview/lib/x64/WebView2Loader.dll`
        * to `.venv/Lib/site-packages/webview/lib/WebView2Loader.dll`
    ''')

    @text_demo('Environment Variables', '''
        You can set the following environment variables to configure NiceGUI:

        - `MATPLOTLIB` (default: true) can be set to `false` to avoid the potentially costly import of Matplotlib.
            This will make `ui.pyplot` and `ui.line_plot` unavailable.
        - `NICEGUI_STORAGE_PATH` (default: local ".nicegui") can be set to change the location of the storage files.
        - `MARKDOWN_CONTENT_CACHE_SIZE` (default: 1000): The maximum number of Markdown content snippets that are cached in memory.
        - `NO_NETIFACES` (default: `false`): Can be set to `true` to hide the netifaces startup warning (e.g. in docker container).
    ''')
    def env_var_demo():
        from nicegui.elements import markdown

        ui.label(f'Markdown content cache size is {markdown.prepare_content.cache_info().maxsize}')

    heading('Deployment')

    subheading('Server Hosting')

    ui.markdown('''
        To deploy your NiceGUI app on a server, you will need to execute your `main.py` (or whichever file contains your `ui.run(...)`) on your cloud infrastructure.
        You can, for example, just install the [NiceGUI python package via pip](https://pypi.org/project/nicegui/) and use systemd or similar service to start the main script.
        In most cases, you will set the port to 80 (or 443 if you want to use HTTPS) with the `ui.run` command to make it easily accessible from the outside.

        A convenient alternative is the use of our [pre-built multi-arch Docker image](https://hub.docker.com/r/zauberzeug/nicegui) which contains all necessary dependencies.
        With this command you can launch the script `main.py` in the current directory on the public port 80:
    ''').classes('bold-links arrow-links')
    with demo.bash_window(classes='max-w-lg w-full h-44'):
        ui.markdown('''
            ```bash
            docker run -it --restart always \\
              -p 80:8080 \\
              -e PUID=$(id -u) \\
              -e PGID=$(id -g) \\
              -v $(pwd)/:/app/ \\
              zauberzeug/nicegui:latest
            ```
        ''')
    ui.markdown('''
        The demo assumes `main.py` uses the port 8080 in the `ui.run` command (which is the default).
        The `-d` tells docker to run in background and `--restart always` makes sure the container is restarted if the app crashes or the server reboots.
        Of course this can also be written in a Docker compose file:
    ''')
    with demo.python_window('docker-compose.yml', classes='max-w-lg w-full h-60'):
        ui.markdown('''
            ```yaml
            app:
                image: zauberzeug/nicegui:latest
                restart: always
                ports:
                    - 80:8080
                environment:
                    - PUID=1000 # change this to your user id
                    - PGID=1000 # change this to your group id
                volumes:
                    - ./:/app/
            ```
        ''')
    ui.markdown('''
        There are other handy features in the Docker image like non-root user execution and signal pass-through.
        For more details we recommend to have a look at our [Docker example](https://github.com/zauberzeug/nicegui/tree/main/examples/docker_image).
    ''').classes('bold-links arrow-links')

    ui.markdown('''
        You can provide SSL certificates directly using [FastAPI](https://fastapi.tiangolo.com/deployment/https/).
        In production we also like using reverse proxies like [Traefik](https://doc.traefik.io/traefik/) or [NGINX](https://www.nginx.com/) to handle these details for us.
        See our development [docker-compose.yml](https://github.com/zauberzeug/nicegui/blob/main/docker-compose.yml) as an example.

        You may also have a look at [our demo for using a custom FastAPI app](https://github.com/zauberzeug/nicegui/tree/main/examples/fastapi).
        This will allow you to do very flexible deployments as described in the [FastAPI documentation](https://fastapi.tiangolo.com/deployment/).
        Note that there are additional steps required to allow multiple workers.
    ''').classes('bold-links arrow-links')

    subheading('Package for Installation')

    ui.markdown('''
        NiceGUI apps can also be bundled into an executable with [PyInstaller](https://www.pyinstaller.org/).
        This allows you to distribute your app as a single file that can be executed on any computer.

        Just take care your `ui.run` command does not use the `reload` argument.
        Running the `build.py` below will create an executable `myapp` in the `dist` folder:
    ''').classes('bold-links arrow-links')

    with ui.row().classes('w-full items-stretch'):
        with demo.python_window(classes='max-w-lg w-full'):
            ui.markdown('''
                ```python
                from nicegui import native_mode, ui

                ui.label('Hello from PyInstaller')

                ui.run(reload=False, port=native_mode.find_open_port())
                ```
            ''')
        with demo.python_window('build.py', classes='max-w-lg w-full'):
            ui.markdown('''
                ```python
                import os
                import subprocess
                from pathlib import Path
                import nicegui

                cmd = [
                    'python',
                    '-m', 'PyInstaller',
                    'main.py', # your main file with ui.run()
                    '--name', 'myapp', # name of your app
                    '--onefile',
                    #'--windowed', # prevent console appearing, only use with ui.run(native=True, ...)
                    '--add-data', f'{Path(nicegui.__file__).parent}{os.pathsep}nicegui'
                ]
                subprocess.call(cmd)
                ```
            ''')

    ui.markdown('''
        **Packaging Tips**

        - When building a PyInstaller app, your main script can use a native window (rather than a browser window) by
          using `ui.run(reload=False, native=True)`.
          The `native` parameter can be `True` or `False` depending on whether you want a native window or to launch a
          page in the user's browser - either will work in the PyInstaller generated app.

        - Specifying `--windowed` to PyInstaller will prevent a terminal console from appearing.
          However you should only use this option if you have also specified `native=True` in your `ui.run` command.
          Without a terminal console the user won't be able to exit the app by pressing Ctrl-C.
          With the `native=True` option, the app will automatically close when the window is closed, as expected.

        - Specifying `--windowed` to PyInstaller will create an `.app` file on Mac which may be more convenient to distribute.
          When you double-click the app to run it, it will not show any console output.
          You can also run the app from the command line with `./myapp.app/Contents/MacOS/myapp` to see the console output.

        - Specifying `--onefile` to PyInstaller will create a single executable file.
          Whilst convenient for distribution, it will be slower to start up.
          This is not NiceGUI's fault but just the way Pyinstaller zips things into a single file, then unzips everything
          into a temporary directory before running.
          You can mitigate this by removing `--onefile` from the PyInstaller command,
          and zip up the generated `dist` directory yourself, distribute it,
          and your end users can unzip once and be good to go,
          without the constant expansion of files due to the `--onefile` flag.
          
        - Summary of user experience for different options:

            | PyInstaller              | `ui.run(...)`  | Explanation |
            | :---                     | :---           | :---        |
            | `onefile`                | `native=False` | Single executable generated in `dist/`, runs in browser |
            | `onefile`                | `native=True`  | Single executable generated in `dist/`, runs in popup window |
            | `onefile` and `windowed` | `native=True`  | Single executable generated in `dist/` (on Mac a proper `dist/myapp.app` generated incl. icon), runs in popup window, no console appears |
            | `onefile` and `windowed` | `native=False` | Avoid (no way to exit the app) |
            | Specify neither          |                | A `dist/myapp` directory created which can be zipped manually and distributed; run with `dist/myapp/myapp` |

        - If you are using a Python virtual environment, ensure you `pip install pyinstaller` within your virtual environment
          so that the correct PyInstaller is used, or you may get broken apps due to the wrong version of PyInstaller being picked up.
          That is why the build script invokes PyInstaller using `python -m PyInstaller` rather than just `pyinstaller`.
    ''').classes('bold-links arrow-links')

    with demo.bash_window(classes='max-w-lg w-full h-42 self-center'):
        ui.markdown('''
            ```bash
            python -m venv venv
            source venv/bin/activate
            pip install nicegui
            pip install pyinstaller
            ```
        ''')

    ui.markdown('''
        **Note:**
        If you're getting an error "TypeError: a bytes-like object is required, not 'str'", try adding the following lines to the top of your `main.py` file:
        ```py
        import sys
        sys.stdout = open('logs.txt', 'w')
        ```
        See <https://github.com/zauberzeug/nicegui/issues/681> for more information.
    ''').classes('bold-links arrow-links')

    subheading('NiceGUI On Air')

    ui.markdown('''
        By using `ui.run(on_air=True)` you can share your local app with others over the internet 🧞.

        When accessing the on-air URL, all libraries (like Vue, Quasar, ...) are loaded from our CDN.
        Thereby only the raw content and events need to be transmitted by your local app.
        This makes it blazing fast even if your app only has a poor internet connection (e.g. a mobile robot in the field).

        By setting `on_air=True` you will get a random URL which is valid for 1 hour.
        If you sign-up at <https://on-air.nicegui.io> you get a token which could be used to identify your device: `ui.run(on_air='<your token>'`).
        This will give you a fixed URL and the possibility to protect remote access with a passphrase.

        Currently On Air is available as a tech preview and can be used free of charge (for now).
        We will gradually improve stability, introduce payment options and extend the service with multi-device management, remote terminal access and more.
        Please let us know your feedback on [GitHub](https://github.com/zauberzeug/nicegui/discussions),
        [Reddit](https://www.reddit.com/r/nicegui/), or [Discord](https://discord.gg/TEpFeAaF4f).

        **Data Privacy:**
        We take your privacy very serious.
        NiceGUI On Air does not log or store any content of the relayed data.
    ''').classes('bold-links arrow-links')

    ui.element('div').classes('h-32')
