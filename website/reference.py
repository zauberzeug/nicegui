from typing import Dict

from nicegui import ui

from .example import example


def create_intro() -> None:
    @example('''#### Hello, World!

Creating a user interface with NiceGUI is as simple as writing a single line of code.
''', tight=True)
    def hello_world_example():
        ui.label('Hello, world!')
        ui.markdown('Have a look at the full <br/> [API reference](reference)!')

    @example('''#### Common UI Elements

NiceGUI comes with a collection of commonly used UI elements.
''', tight=True)
    def common_elements_example():
        ui.button('Button', on_click=lambda: ui.notify('Click'))
        ui.checkbox('Checkbox', on_change=lambda e: ui.notify('Checked' if e.value else 'Unchecked'))
        ui.switch('Switch', on_change=lambda e: ui.notify('Switched' if e.value else 'Unswitched'))
        ui.input('Text input', on_change=lambda e: ui.notify(e.value))
        ui.radio(['A', 'B'], value='A', on_change=lambda e: ui.notify(e.value)).props('inline')
        ui.select(['One', 'Two'], value='One', on_change=lambda e: ui.notify(e.value))
        ui.link('And many more...', '/reference').classes('text-lg')

    @example('''#### Value Binding

Binding values between UI elements or [to data models](http://127.0.0.1:8080/reference#bindings) is built into NiceGUI.
''', tight=True)
    def binding_example():
        slider = ui.slider(min=0, max=100, value=50)
        ui.number('Value').bind_value(slider, 'value').classes('fit')


def create_full() -> None:
    def h3(text: str) -> None:
        ui.label(text).style('width: 100%; border-bottom: 1px solid silver; font-size: 200%; font-weight: 200')

    h3('Basic Elements')

    @example(ui.label)
    def label_example():
        ui.label('some label')

    @example(ui.icon)
    def icon_example():
        ui.icon('thumb_up')

    @example(ui.link)
    def link_example():
        ui.link('NiceGUI on GitHub', 'https://github.com/zauberzeug/nicegui')

    @example(ui.button)
    def button_example():
        ui.button('Click me!', on_click=lambda: ui.notify(f'You clicked me!'))

    @example(ui.badge)
    def badge_example():
        with ui.button('Click me!', on_click=lambda: badge.set_text(int(badge.text) + 1)):
            badge = ui.badge('0', color='red').props('floating')

    @example(ui.toggle)
    def toggle_example():
        toggle1 = ui.toggle([1, 2, 3], value=1)
        toggle2 = ui.toggle({1: 'A', 2: 'B', 3: 'C'}).bind_value(toggle1, 'value')

    @example(ui.radio)
    def radio_example():
        radio1 = ui.radio([1, 2, 3], value=1).props('inline')
        radio2 = ui.radio({1: 'A', 2: 'B', 3: 'C'}).props('inline').bind_value(radio1, 'value')

    @example(ui.select)
    def select_example():
        select1 = ui.select([1, 2, 3], value=1)
        select2 = ui.select({1: 'One', 2: 'Two', 3: 'Three'}).bind_value(select1, 'value')

    @example(ui.checkbox)
    def checkbox_example():
        checkbox = ui.checkbox('check me')
        ui.label('Check!').bind_visibility_from(checkbox, 'value')

    @example(ui.switch)
    def switch_example():
        switch = ui.switch('switch me')
        ui.label('Switch!').bind_visibility_from(switch, 'value')

    @example(ui.slider)
    def slider_example():
        slider = ui.slider(min=0, max=100, value=50).props('label')
        ui.label().bind_text_from(slider, 'value')

    @example(ui.joystick)
    def joystick_example():
        ui.joystick(color='blue', size=50,
                    on_move=lambda e: coordinates.set_text(f"{e.x:.3f}, {e.y:.3f}"),
                    on_end=lambda _: coordinates.set_text('0, 0'))
        coordinates = ui.label('0, 0')

    @example(ui.input)
    def input_example():
        ui.input(label='Text', placeholder='start typing',
                 on_change=lambda e: input_result.set_text('you typed: ' + e.value))
        input_result = ui.label()

    @example(ui.number)
    def number_example():
        ui.number(label='Number', value=3.1415927, format='%.2f',
                  on_change=lambda e: number_result.set_text(f'you entered: {e.value}'))
        number_result = ui.label()

    @example(ui.color_input)
    def color_input_example():
        color_label = ui.label('Change my color!')
        ui.color_input(label='Color', value='#000000',
                       on_change=lambda e: color_label.style(f'color:{e.value}'))

    @example(ui.color_picker)
    def color_picker_example():
        picker = ui.color_picker(on_pick=lambda e: button.style(f'background-color:{e.color}!important'))
        button = ui.button(on_click=picker.open).props('icon=colorize')

    @example(ui.upload)
    def upload_example():
        ui.upload(on_upload=lambda e: ui.notify(f'{e.files[0].size} bytes'))

    h3('Markdown and HTML')

    @example(ui.markdown)
    def markdown_example():
        ui.markdown('''This is **Markdown**.''')

    @example(ui.html)
    def html_example():
        ui.html('This is <strong>HTML</strong>.')

    @example('''#### SVG

You can add Scalable Vector Graphics using the `ui.html` element.
''')
    def svg_example():
        content = '''
            <svg viewBox="0 0 200 200" width="100" height="100" xmlns="http://www.w3.org/2000/svg">
            <circle cx="100" cy="100" r="78" fill="#ffde34" stroke="black" stroke-width="3" />
            <circle cx="80" cy="85" r="8" />
            <circle cx="120" cy="85" r="8" />
            <path d="m60,120 C75,150 125,150 140,120" style="fill:none; stroke:black; stroke-width:8; stroke-linecap:round" />
            </svg>'''
        ui.html(content)

    h3('Images')

    @example(ui.image)
    def image_example():
        ui.image('http://placeimg.com/640/360/tech')

    @example('''#### Captions and Overlays

By nesting elements inside a `ui.image` you can create augmentations.

Use [Quasar classes](https://quasar.dev/vue-components/img) for positioning and styling captions.
To overlay an SVG, make the `viewBox` exactly the size of the image and provide `100%` width/height to match the actual rendered size.
''')
    def captions_and_overlays_example():
        with ui.image('http://placeimg.com/640/360/nature'):
            ui.label('Nice!').classes('absolute-bottom text-subtitle2 text-center')

        with ui.image('https://cdn.stocksnap.io/img-thumbs/960w/airplane-sky_DYPWDEEILG.jpg'):
            ui.html('''
                <svg viewBox="0 0 960 638" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
                <circle cx="445" cy="300" r="100" fill="none" stroke="red" stroke-width="20" />
                </svg>
            ''').classes('bg-transparent')

    @example(ui.interactive_image)
    def interactive_image_example():
        from nicegui.events import MouseEventArguments

        def mouse_handler(e: MouseEventArguments):
            color = 'SkyBlue' if e.type == 'mousedown' else 'SteelBlue'
            ii.content += f'<circle cx="{e.image_x}" cy="{e.image_y}" r="20" fill="{color}"/>'
            ui.notify(f'{e.type} at ({e.image_x:.1f}, {e.image_y:.1f})')

        src = 'https://cdn.stocksnap.io/img-thumbs/960w/corn-cob_YSZZZEC59W.jpg'
        ii = ui.interactive_image(src, on_mouse=mouse_handler, events=['mousedown', 'mouseup'], cross=True)

    h3('Data Elements')

    @example(ui.table)
    def table_example():
        table = ui.table({
            'columnDefs': [
                {'headerName': 'Name', 'field': 'name'},
                {'headerName': 'Age', 'field': 'age'},
            ],
            'rowData': [
                {'name': 'Alice', 'age': 18},
                {'name': 'Bob', 'age': 21},
                {'name': 'Carol', 'age': 42},
            ],
        }).classes('max-h-40')

        def update():
            table.options['rowData'][0]['age'] += 1
            table.update()

        ui.button('Update', on_click=update)

    @example(ui.chart)
    def chart_example():
        from numpy.random import random

        chart = ui.chart({
            'title': False,
            'chart': {'type': 'bar'},
            'xAxis': {'categories': ['A', 'B']},
            'series': [
                {'name': 'Alpha', 'data': [0.1, 0.2]},
                {'name': 'Beta', 'data': [0.3, 0.4]},
            ],
        }).classes('w-full h-64')

        def update():
            chart.options['series'][0]['data'][:] = random(2)
            chart.update()

        ui.button('Update', on_click=update)

    @example(ui.plot)
    def plot_example():
        import numpy as np
        from matplotlib import pyplot as plt

        with ui.plot(figsize=(2.5, 1.8)):
            x = np.linspace(0.0, 5.0)
            y = np.cos(2 * np.pi * x) * np.exp(-x)
            plt.plot(x, y, '-')

    @example(ui.line_plot)
    def line_plot_example():
        global line_checkbox
        from datetime import datetime

        import numpy as np

        line_plot = ui.line_plot(n=2, limit=20, figsize=(2.5, 1.8), update_every=5) \
            .with_legend(['sin', 'cos'], loc='upper center', ncol=2)

        def update_line_plot() -> None:
            now = datetime.now()
            x = now.timestamp()
            y1 = np.sin(x)
            y2 = np.cos(x)
            line_plot.push([now], [[y1], [y2]])

        line_updates = ui.timer(0.1, update_line_plot, active=False)
        line_checkbox = ui.checkbox('active').bind_value(line_updates, 'active')

    @example(ui.linear_progress)
    def linear_progress_example():
        slider = ui.slider(min=0, max=1, step=0.01, value=0.5)
        ui.linear_progress().bind_value_from(slider, 'value')

    @example(ui.circular_progress)
    def circular_progress_example():
        slider = ui.slider(min=0, max=1, step=0.01, value=0.5)
        ui.circular_progress().bind_value_from(slider, 'value')

    @example(ui.scene)
    def scene_example():
        with ui.scene(width=225, height=225) as scene:
            scene.sphere().material('#4488ff')
            scene.cylinder(1, 0.5, 2, 20).material('#ff8800', opacity=0.5).move(-2, 1)
            scene.extrusion([[0, 0], [0, 1], [1, 0.5]], 0.1).material('#ff8888').move(-2, -2)

            with scene.group().move(z=2):
                scene.box().move(x=2)
                scene.box().move(y=2).rotate(0.25, 0.5, 0.75)
                scene.box(wireframe=True).material('#888888').move(x=2, y=2)

            scene.line([-4, 0, 0], [-4, 2, 0]).material('#ff0000')
            scene.curve([-4, 0, 0], [-4, -1, 0], [-3, -1, 0], [-3, -2, 0]).material('#008800')

            logo = 'https://avatars.githubusercontent.com/u/2843826'
            scene.texture(logo, [[[0.5, 2, 0], [2.5, 2, 0]],
                                 [[0.5, 0, 0], [2.5, 0, 0]]]).move(1, -2)

            teapot = 'https://upload.wikimedia.org/wikipedia/commons/9/93/Utah_teapot_(solid).stl'
            scene.stl(teapot).scale(0.2).move(-3, 4)

            scene.text('2D', 'background: rgba(0, 0, 0, 0.2); border-radius: 5px; padding: 5px').move(z=2)
            scene.text3d('3D', 'background: rgba(0, 0, 0, 0.2); border-radius: 5px; padding: 5px').move(y=-2).scale(.05)

    @example(ui.tree)
    def tree_example():
        ui.tree([
            {'id': 'numbers', 'children': [{'id': '1'}, {'id': '2'}]},
            {'id': 'letters', 'children': [{'id': 'A'}, {'id': 'B'}]},
        ], label_key='id', on_select=lambda e: ui.notify(e.value))

    @example(ui.log)
    def log_example():
        from datetime import datetime

        log = ui.log(max_lines=10).classes('w-full h-16')
        ui.button('Log time', on_click=lambda: log.push(datetime.now().strftime('%X.%f')[:-5]))

    h3('Layout')

    @example(ui.card)
    def card_example():
        with ui.card().tight() as card:
            ui.image('http://placeimg.com/640/360/nature')
            with ui.card_section():
                ui.label('Lorem ipsum dolor sit amet, consectetur adipiscing elit, ...')

    @example(ui.column)
    def column_example():
        with ui.column():
            ui.label('label 1')
            ui.label('label 2')
            ui.label('label 3')

    @example(ui.row)
    def row_example():
        with ui.row():
            ui.label('label 1')
            ui.label('label 2')
            ui.label('label 3')

    @example('''#### Clear Containers

To remove all elements from a row, column or card container, use the `clear()` method.

Alternatively, you can remove individual elements with `remove(element)`, where `element` is an Element or an index.
''')
    def clear_containers_example():
        container = ui.row()

        def add_face():
            with container:
                ui.icon('face')
        add_face()

        ui.button('Add', on_click=add_face)
        ui.button('Remove', on_click=lambda: container.remove(0))
        ui.button('Clear', on_click=container.clear)

    @example(ui.expansion)
    def expansion_example():
        with ui.expansion('Expand!', icon='work').classes('w-full'):
            ui.label('inside the expansion')

    @example(ui.menu)
    def menu_example():
        choice = ui.label('Try the menu.')
        with ui.menu() as menu:
            ui.menu_item('Menu item 1', lambda: choice.set_text('Selected item 1.'))
            ui.menu_item('Menu item 2', lambda: choice.set_text('Selected item 2.'))
            ui.menu_item('Menu item 3 (keep open)', lambda: choice.set_text('Selected item 3.'), auto_close=False)
            ui.separator()
            ui.menu_item('Close', on_click=menu.close)

        ui.button('Open menu', on_click=menu.open)

    @example('''#### Tooltips

Simply call the `tooltip(text:str)` method on UI elements to provide a tooltip.

For more artistic control you can nest tooltip elements and apply props, classes and styles.
''')
    def tooltips_example():
        ui.label('Tooltips...').tooltip('...are shown on mouse over')
        with ui.button().props('icon=thumb_up'):
            ui.tooltip('I like this').classes('bg-green')

    @example(ui.notify)
    def notify_example():
        ui.button('Say hi!', on_click=lambda: ui.notify('Hi!', close_button='OK'))

    @example(ui.dialog)
    def dialog_example():
        with ui.dialog() as dialog, ui.card():
            ui.label('Hello world!')
            ui.button('Close', on_click=dialog.close)

        ui.button('Open a dialog', on_click=dialog.open)

    @example('''#### Awaitable dialog

Dialogs can be awaited.
Use the `submit` method to close the dialog and return a result.
Canceling the dialog by clicking in the background or pressing the escape key yields `None`.
''')
    def async_dialog_example():
        with ui.dialog() as dialog, ui.card():
            ui.label('Are you sure?')
            with ui.row():
                ui.button('Yes', on_click=lambda: dialog.submit('Yes'))
                ui.button('No', on_click=lambda: dialog.submit('No'))

        async def show():
            result = await dialog
            ui.notify(f'You chose {result}')

        ui.button('Await a dialog', on_click=show)

    h3('Appearance')

    @example('''#### Styling

NiceGUI uses the [Quasar Framework](https://quasar.dev/) version 1.0 and hence has its full design power.
Each NiceGUI element provides a `props` method whose content is passed [to the Quasar component](https://justpy.io/quasar_tutorial/introduction/#props-of-quasar-components):
Have a look at [the Quasar documentation](https://quasar.dev/vue-components/button#design) for all styling props.
You can also apply [Tailwind](https://tailwindcss.com/) utility classes with the `classes` method.

If you really need to apply CSS, you can use the `styles` method. Here the delimiter is `;` instead of a blank space.

All three functions also provide `remove` and `replace` parameters in case the predefined look is not wanted in a particular styling.
''')
    def design_example():
        ui.radio(['x', 'y', 'z'], value='x').props('inline color=green')
        ui.button().props('icon=touch_app outline round').classes('shadow-lg')
        ui.label('Stylish!').style('color: #6E93D6; font-size: 200%; font-weight: 300')

    @example(ui.colors)
    def colors_example():
        ui.button('Default', on_click=lambda: ui.colors())
        ui.button('Gray', on_click=lambda: ui.colors(primary='#555'))

    h3('Action')

    @example('''#### Lifecycle

You can run a function or coroutine as a parallel task by passing it to one of the following register methods:

- `ui.on_startup`: Called when NiceGUI is started or restarted.
- `ui.on_shutdown`: Called when NiceGUI is shut down or restarted.
- `ui.on_connect`: Called when a client connects to NiceGUI. (Optional argument: Starlette request)
- `ui.on_disconnect`: Called when a client disconnects from NiceGUI. (Optional argument: socket)

When NiceGUI is shut down or restarted, the startup tasks will be automatically canceled.
''')
    def lifecycle_example():
        import asyncio

        l = ui.label()

        async def countdown():
            for i in [5, 4, 3, 2, 1, 0]:
                l.text = f'{i}...' if i else 'Take-off!'
                await asyncio.sleep(1)

        ui.on_connect(countdown)

    @example(ui.timer)
    def timer_example():
        from datetime import datetime

        with ui.row().classes('items-center'):
            clock = ui.label()
            t = ui.timer(interval=0.1, callback=lambda: clock.set_text(datetime.now().strftime('%X.%f')[:-5]))
            ui.checkbox('active').bind_value(t, 'active')

        with ui.row():
            def lazy_update() -> None:
                new_text = datetime.now().strftime('%X.%f')[:-5]
                if lazy_clock.text[:8] == new_text[:8]:
                    return
                lazy_clock.text = new_text
            lazy_clock = ui.label()
            ui.timer(interval=0.1, callback=lazy_update)

    @example(ui.keyboard)
    def keyboard_example():
        from nicegui.events import KeyEventArguments

        def handle_key(e: KeyEventArguments):
            if e.key == 'f' and not e.action.repeat:
                if e.action.keyup:
                    ui.notify('f was just released')
                elif e.action.keydown:
                    ui.notify('f was just pressed')
            if e.modifiers.shift and e.action.keydown:
                if e.key.arrow_left:
                    ui.notify('going left')
                elif e.key.arrow_right:
                    ui.notify('going right')
                elif e.key.arrow_up:
                    ui.notify('going up')
                elif e.key.arrow_down:
                    ui.notify('going down')

        keyboard = ui.keyboard(on_key=handle_key)
        ui.label('Key events can be caught globally by using the keyboard element.')
        ui.checkbox('Track key events').bind_value_to(keyboard, 'active')

    @example('''#### Bindings

NiceGUI is able to directly bind UI elements to models.
Binding is possible for UI element properties like text, value or visibility and for model properties that are (nested) class attributes.

Each element provides methods like `bind_value` and `bind_visibility` to create a two-way binding with the corresponding property.
To define a one-way binding use the `_from` and `_to` variants of these methods.
Just pass a property of the model as parameter to these methods to create the binding.
''')
    def bindings_example():
        class Demo:
            def __init__(self):
                self.number = 1

        demo = Demo()
        v = ui.checkbox('visible', value=True)
        with ui.column().bind_visibility_from(v, 'value'):
            ui.slider(min=1, max=3).bind_value(demo, 'number')
            ui.toggle({1: 'A', 2: 'B', 3: 'C'}).bind_value(demo, 'number')
            ui.number().bind_value(demo, 'number')

    @example('''#### UI Updates

NiceGUI tries to automatically synchronize the state of UI elements with the client, e.g. when a label text, an input value or style/classes/props of an element have changed.
In other cases, you can explicitly call `element.update()` or `ui.update(*elements)` to update.
The example code shows both methods for a `ui.chart`, where it is difficult to automatically detect changes in the `options` dictionary.
''')
    def ui_updates_example():
        from random import randint

        chart = ui.chart({'title': False, 'series': [{'data': [1, 2]}]}).classes('w-full h-64')

        def add():
            chart.options['series'][0]['data'].append(randint(0, 100))
            chart.update()

        def clear():
            chart.options['series'][0]['data'].clear()
            ui.update(chart)

        ui.button('Add', on_click=add)
        ui.button('Clear', on_click=clear)

    @example('''#### Async event handlers

Most elements also support asynchronous event handlers.

Note: You can also pass a `functools.partial` into the `on_click` property to wrap async functions with parameters.
''')
    def async_handlers_example():
        import asyncio

        async def async_task():
            ui.notify('Asynchronous task started')
            await asyncio.sleep(5)
            ui.notify('Asynchronous task finished')

        ui.button('start async task', on_click=async_task)

    h3('Pages')

    @example(ui.page)
    def page_example():
        @ui.page('/other_page')
        def other_page():
            ui.label('Welcome to the other side')
            ui.link('Back to main page', '/#page')

        @ui.page('/dark_page', dark=True)
        def dark_page():
            ui.label('Welcome to the dark side')
            ui.link('Back to main page', '/#page')

        ui.link('Visit other page', other_page)
        ui.link('Visit dark page', dark_page)

    @example('''#### Auto-index page

Pages created with the `@ui.page` decorator are "private".
Their content is re-created for each client.
Thus, in the example to the right, the displayed ID on the private page changes when the browser reloads the page.

UI elements that are not wrapped in a decorated page function are placed on an automatically generated index page at route "/".
This auto-index page is created once on startup and *shared* across all clients that might connect.
Thus, each connected client will see the *same* elements.
In the example to the right, the displayed ID on the auto-index page remains constant when the browser reloads the page.
''')
    def auto_index_page():
        from uuid import uuid4

        @ui.page('/private_page')
        async def private_page():
            ui.label(f'private page with ID {uuid4()}')

        ui.label(f'shared auto-index page with ID {uuid4()}')
        ui.link('private page', private_page)

    @example('''#### Pages with Path Parameters

Page routes can contain parameters like [FastAPI](https://fastapi.tiangolo.com/tutorial/path-params/>).
If type-annotated, they are automatically converted to bool, int, float and complex values.
If the page function expects a `request` argument, the request object is automatically provided.
''')
    def page_with_path_parameters_example():
        @ui.page('/repeat/{word}/{count}')
        def page(word: str, count: int):
            ui.label(word * count)

        ui.link('Say hi to Santa!', 'repeat/Ho! /3')

    @example('''#### Wait for Handshake with Client

To wait for a client connection, you can add a `client` argument to the decorated page function
and await `client.handshake()`.
All code below that statement is executed after the websocket connection between server and client has been established.

For example, this allows you to run JavaScript commands; which is only possible with a client connection (see [#112](https://github.com/zauberzeug/nicegui/issues/112)).
Also it is possible to do async stuff while the user already sees some content.
    ''')
    def wait_for_handshake_example():
        import asyncio

        from nicegui import Client

        @ui.page('/wait_for_handshake')
        async def wait_for_handshake(client: Client):
            ui.label('This text is displayed immediately.')
            await client.handshake()
            await asyncio.sleep(2)
            ui.label('This text is displayed 2 seconds after the page has been fully loaded.')
            ui.label(f'The IP address {client.ip} was obtained from the websocket.')

        ui.link('wait for handshake', wait_for_handshake)

    @example('''#### Page Layout

With `ui.header`, `ui.footer`, `ui.left_drawer` and `ui.right_drawer` you can add additional layout elements to a page.
The `fixed` argument controls whether the element should scroll or stay fixed on the screen.
The `top_corner` and `bottom_corner` arguments indicate whether a drawer should expand to the top or bottom of the page.
See <https://quasar.dev/layout/header-and-footer> and <https://quasar.dev/layout/drawer> for more information about possible props like
`elevated`, `bordered` and many more.
With `ui.page_sticky` you can place an element "sticky" on the screen.
See <https://quasar.dev/layout/page-sticky> for more information.
    ''')
    def page_layout_example():
        @ui.page('/page_layout')
        async def page_layout():
            ui.label('CONTENT')
            [ui.label(f'Line {i}') for i in range(100)]
            with ui.header().style('background-color: #3874c8').props('elevated'):
                ui.label('HEADER')
            with ui.left_drawer(top_corner=True, bottom_corner=True).style('background-color: #d7e3f4'):
                ui.label('LEFT DRAWER')
            with ui.right_drawer(fixed=False).style('background-color: #ebf1fa').props('bordered'):
                ui.label('RIGHT DRAWER')
            with ui.footer().style('background-color: #3874c8'):
                ui.label('FOOTER')

        ui.link('show page with fancy layout', page_layout)

    @example(ui.open)
    def ui_open_example():
        @ui.page('/yet_another_page')
        def yet_another_page():
            ui.label('Welcome to yet another page')
            ui.button('RETURN', on_click=lambda: ui.open('/#open'))

        ui.button('REDIRECT', on_click=lambda: ui.open(yet_another_page))

    @example('''#### Sessions

`ui.page` provides an optional `on_connect` argument to register a callback.
It is invoked for each new connection to the page.

The optional `request` argument provides insights about the clients URL parameters etc. (see [the JustPy docs](https://justpy.io/tutorial/request_object/) for more details).
It also enables you to identify sessions over [longer time spans by configuring cookies](https://justpy.io/tutorial/sessions/).
''', skip=True)
    def sessions_example():
        from collections import Counter
        from datetime import datetime

        from starlette.requests import Request

        id_counter = Counter()
        creation = datetime.now().strftime('%H:%M, %d %B %Y')

        def handle_connection(request: Request):
            id_counter[request.session_id] += 1
            visits.set_text(f'{len(id_counter)} unique views ({sum(id_counter.values())} overall) since {creation}')

        @ui.page('/session_demo', on_connect=handle_connection)
        def session_demo():
            global visits
            visits = ui.label()

        ui.link('Visit session demo', session_demo)

    @example('''#### JavaScript

With `ui.run_javascript()` you can run arbitrary JavaScript code on a page that is executed in the browser.
The asynchronous function will return after the command(s) are executed.
You can also set `respond=False` to send a command without waiting for a response.
''')
    def javascript_example():
        async def alert():
            await ui.run_javascript('alert("Hello!")', respond=False)

        async def get_date():
            time = await ui.run_javascript('Date()')
            ui.notify(f'Browser time: {time}')

        ui.button('fire and forget', on_click=alert)
        ui.button('receive result', on_click=get_date)

    h3('Configuration')

    @example('''#### ui.run

You can call `ui.run()` with optional arguments:

- `host` (default: `'0.0.0.0'`)
- `port` (default: `8080`)
- `title` (default: `'NiceGUI'`)
- `favicon`: relative filepath to a favicon (default: `None`, NiceGUI icon will be used)
- `dark`: whether to use Quasar's dark mode (default: `False`, use `None` for "auto" mode)
- `main_page_classes`: configure Quasar classes of main page (default: `'q-pa-md column items-start'`)
- `binding_refresh_interval`: time between binding updates (default: `0.1` seconds, bigger is more cpu friendly)
- `show`: automatically open the ui in a browser tab (default: `True`)
- `reload`: automatically reload the ui on file changes (default: `True`)
- `uvicorn_logging_level`: logging level for uvicorn server (default: `'warning'`)
- `uvicorn_reload_dirs`: string with comma-separated list for directories to be monitored (default is current working directory only)
- `uvicorn_reload_includes`: string with comma-separated list of glob-patterns which trigger reload on modification (default: `'.py'`)
- `uvicorn_reload_excludes`: string with comma-separated list of glob-patterns which should be ignored for reload (default: `'.*, .py[cod], .sw.*, ~*'`)
- `exclude`: comma-separated string to exclude elements (with corresponding JavaScript libraries) to save bandwidth
  (possible entries: chart, colors, interactive_image, joystick, keyboard, log, scene, upload, table)

The environment variables `HOST` and `PORT` can also be used to configure NiceGUI.

To avoid the potentially costly import of Matplotlib, you set the environment variable `MATPLOTLIB=false`.
This will make `ui.plot` and `ui.line_plot` unavailable.
''')
    def ui_run_example():
        ui.label('dark page on port 7000 without reloading')

        # ui.run(dark=True, port=7000, reload=False)

    # HACK: turn expensive line plot off after 10 seconds
    def handle_change(msg: Dict) -> None:
        def turn_off() -> None:
            line_checkbox.set_value(False)
            ui.notify('Turning off that line plot to save resources on our live demo server. 😎')
        line_checkbox.value = msg['args']
        if line_checkbox.value:
            ui.timer(10.0, turn_off, once=True)
    line_checkbox.on('update:model-value', handle_change)
