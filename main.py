#!/usr/bin/env python3
import asyncio
import inspect
import re
from contextlib import contextmanager
from typing import Callable, Union

import docutils.core

from nicegui import ui

# add docutils css to webpage
ui.add_head_html(docutils.core.publish_parts('', writer_name='html')['stylesheet'])

# avoid display:block for PyPI/Docker/GitHub badges
ui.add_head_html('<style>p a img {display: inline; vertical-align: baseline}</style>')


@contextmanager
def example(content: Union[Callable, type, str]):
    callFrame = inspect.currentframe().f_back.f_back
    begin = callFrame.f_lineno

    def add_html_anchor(element: ui.html):
        html = element.content
        match = re.search(r'<h4.*?>(.*?)</h4>', html)
        if not match:
            return

        headline_id = re.sub('[^(a-z)(A-Z)(0-9)-]', '_', match.groups()[0].strip()).lower()
        if not headline_id:
            return

        icon = '<span class="material-icons">link</span>'
        anchor = f'<a href="#{headline_id}" class="text-gray-300 hover:text-black">{icon}</a>'
        html = html.replace('<h4', f'<h4 id="{headline_id}"', 1)
        html = html.replace('</h4>', f' {anchor}</h4>', 1)
        element.view.inner_html = html

    with ui.row().classes('flex w-full'):
        if isinstance(content, str):
            add_html_anchor(ui.markdown(content).classes('mr-8 w-4/12'))
        else:
            doc = content.__doc__ or content.__init__.__doc__
            html = docutils.core.publish_parts(doc, writer_name='html')['html_body']
            html = html.replace('<p>', '<h4>', 1)
            html = html.replace('</p>', '</h4>', 1)
            html = ui.markdown.apply_tailwind(html)
            add_html_anchor(ui.html(html).classes('mr-8 w-4/12'))

        try:
            with ui.card().classes('mt-12 w-2/12'):
                with ui.column().classes('flex w-full'):
                    yield
        finally:
            code = inspect.getsource(callFrame)
            end = begin + 1
            lines = code.splitlines()
            while True:
                end += 1
                if end >= len(lines):
                    break
                if inspect.indentsize(lines[end]) < inspect.indentsize(lines[begin]) and lines[end]:
                    break
            code = lines[begin:end]
            code = [l[4:] for l in code]
            code.insert(0, '```python')
            code.insert(1, 'from nicegui import ui')
            if code[2].split()[0] not in ['from', 'import']:
                code.insert(2, '')
            code.append('ui.run()')
            code.append('```')
            code = '\n'.join(code)
            ui.markdown(code).classes('mt-12 w-5/12 overflow-auto')


ui.html(
    '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-fork-ribbon-css/0.2.3/gh-fork-ribbon.min.css" />'
    '<style>.github-fork-ribbon:before { background-color: #999; }</style>'
    '<a class="github-fork-ribbon" href="https://github.com/zauberzeug/nicegui" data-ribbon="Fork me on GitHub" title="Fork me on GitHub">Fork me on GitHub</a>'
)

with ui.row().classes('flex w-full'):
    with open('README.md', 'r') as file:
        content = file.read()
        content = re.sub(r'(?m)^\<img.*\n?', '', content)
        ui.markdown(content).classes('w-6/12')

    with ui.card().classes('mx-auto mt-24'):
        with ui.row():
            with ui.column():
                ui.button('Click me!', on_click=lambda: output.set_text('Click'))
                ui.checkbox('Check me!', on_change=lambda e: output.set_text('Checked' if e.value else 'Unchecked'))
                ui.switch('Switch me!', on_change=lambda e: output.set_text('Switched' if e.value else 'Unswitched'))
                ui.input('Text', value='abc', on_change=lambda e: output.set_text(e.value))
                ui.number('Number', value=3.1415927, format='%.2f', on_change=lambda e: output.set_text(e.value))

            with ui.column():
                ui.slider(min=0, max=100, value=50, step=0.1, on_change=lambda e: output.set_text(e.value))
                ui.radio(['A', 'B', 'C'], value='A', on_change=lambda e: output.set_text(e.value)).props('inline')
                ui.toggle(['1', '2', '3'], value='1', on_change=lambda e: output.set_text(e.value)).classes('mx-auto')
                ui.select({1: 'One', 2: 'Two', 3: 'Three'}, value=1,
                          on_change=lambda e: output.set_text(e.value)).classes('mx-auto')

            with ui.column().classes('w-24'):
                ui.label('Output:')
                output = ui.label('').classes('text-bold')

ui.markdown('## API Documentation and Examples')


def h3(text: str) -> None:
    ui.label(text).style('width: 100%; border-bottom: 1px solid silver; font-size: 200%; font-weight: 200')


h3('Basic Elements')

with example(ui.label):
    ui.label('some label')

with example(ui.icon):
    ui.icon('thumb_up')

with example(ui.link):
    ui.link('NiceGUI on GitHub', 'https://github.com/zauberzeug/nicegui')

with example(ui.button):
    ui.button('Click me!', on_click=lambda: ui.notify(f'You clicked me!'))

with example(ui.toggle):
    toggle1 = ui.toggle([1, 2, 3], value=1)
    toggle2 = ui.toggle({1: 'A', 2: 'B', 3: 'C'}).bind_value(toggle1, 'value')

with example(ui.radio):
    radio1 = ui.radio([1, 2, 3], value=1).props('inline')
    radio2 = ui.radio({1: 'A', 2: 'B', 3: 'C'}).props('inline').bind_value(radio1, 'value')

with example(ui.select):
    select1 = ui.select([1, 2, 3], value=1)
    select2 = ui.select({1: 'One', 2: 'Two', 3: 'Three'}).bind_value(select1, 'value')

with example(ui.checkbox):
    checkbox = ui.checkbox('check me')
    ui.label('Check!').bind_visibility_from(checkbox, 'value')

with example(ui.switch):
    switch = ui.switch('switch me')
    ui.label('Switch!').bind_visibility_from(switch, 'value')

with example(ui.slider):
    slider = ui.slider(min=0, max=100, value=50).props('label')
    ui.label().bind_text_from(slider, 'value')

with example(ui.joystick):
    ui.joystick(color='blue', size=50,
                on_move=lambda msg: coordinates.set_text(f'{msg.data.vector.x:.3f}, {msg.data.vector.y:.3f}'),
                on_end=lambda msg: coordinates.set_text('0, 0'))
    coordinates = ui.label('0, 0')

with example(ui.input):
    ui.input(label='Text', placeholder='press ENTER to apply',
             on_change=lambda e: input_result.set_text('you typed: ' + e.value))
    input_result = ui.label()

with example(ui.number):
    ui.number(label='Number', value=3.1415927, format='%.2f',
              on_change=lambda e: number_result.set_text(f'you entered: {e.value}'))
    number_result = ui.label()

with example(ui.color_input):
    color_label = ui.label('Change my color!')
    ui.color_input(label='Color', value='#000000',
                   on_change=lambda e: color_label.style(f'color:{e.value}'))

with example(ui.color_picker):
    picker = ui.color_picker(on_pick=lambda e: button.style(f'background-color:{e.color}!important'))
    button = ui.button(on_click=picker.open).props('icon=colorize')

with example(ui.upload):
    ui.upload(on_upload=lambda e: upload_result.set_text(e.files))
    upload_result = ui.label()

h3('Markdown and HTML')

with example(ui.markdown):
    ui.markdown('''This is **Markdown**.''')

with example(ui.html):
    ui.html('This is <strong>HTML</strong>.')

svg = '''#### SVG

You can add Scalable Vector Graphics using the `ui.html` element.
'''
with example(svg):
    content = '''
        <svg viewBox="0 0 200 200" width="100" height="100" xmlns="http://www.w3.org/2000/svg">
        <circle cx="100" cy="100" r="78" fill="#ffde34" stroke="black" stroke-width="3" />
        <circle cx="80" cy="85" r="8" />
        <circle cx="120" cy="85" r="8" />
        <path d="m60,120 C75,150 125,150 140,120" style="fill:none; stroke:black; stroke-width:8; stroke-linecap:round" />
        </svg>'''
    ui.html(content)

h3('Images')

with example(ui.image):
    ui.image('http://placeimg.com/640/360/tech')

captions_and_overlays = '''#### Captions and Overlays

By nesting elements inside a `ui.image` you can create augmentations.

Use [Quasar classes](https://quasar.dev/vue-components/img) for positioning and styling captions.
To overlay an SVG, make the `viewBox` exactly the size of the image and provide `100%` width/height to match the actual rendered size.
'''
with example(captions_and_overlays):
    with ui.image('http://placeimg.com/640/360/nature'):
        ui.label('Nice!').classes('absolute-bottom text-subtitle2 text-center')

    with ui.image('https://cdn.stocksnap.io/img-thumbs/960w/airplane-sky_DYPWDEEILG.jpg'):
        content = '''
            <svg viewBox="0 0 960 638" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <circle cx="445" cy="300" r="100" fill="none" stroke="red" stroke-width="20" />
            </svg>'''
        ui.html(content).style('background:transparent')

with example(ui.interactive_image):
    from nicegui.events import MouseEventArguments

    def mouse_handler(e: MouseEventArguments):
        color = 'SkyBlue' if e.type == 'mousedown' else 'SteelBlue'
        ii.svg_content += f'<circle cx="{e.image_x}" cy="{e.image_y}" r="20" fill="{color}"/>'
        ui.notify(f'{e.type} at ({e.image_x:.1f}, {e.image_y:.1f})')

    src = 'https://cdn.stocksnap.io/img-thumbs/960w/corn-cob_YSZZZEC59W.jpg'
    ii = ui.interactive_image(src, on_mouse=mouse_handler, events=['mousedown', 'mouseup'], cross=True)

h3('Data Elements')

with example(ui.table):
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
        table.options.rowData[0].age += 1
        table.update()

    ui.button('Update', on_click=update)

with example(ui.chart):
    from numpy.random import random

    chart = ui.chart({
        'title': False,
        'chart': {'type': 'bar'},
        'xAxis': {'categories': ['A', 'B']},
        'series': [
            {'name': 'Alpha', 'data': [0.1, 0.2]},
            {'name': 'Beta', 'data': [0.3, 0.4]},
        ],
    }).classes('max-w-full h-64')

    def update():
        chart.options.series[0].data[:] = random(2)
        chart.update()

    ui.button('Update', on_click=update)

with example(ui.plot):
    import numpy as np
    from matplotlib import pyplot as plt

    with ui.plot(figsize=(2.5, 1.8)):
        x = np.linspace(0.0, 5.0)
        y = np.cos(2 * np.pi * x) * np.exp(-x)
        plt.plot(x, y, '-')
        plt.xlabel('time (s)')
        plt.ylabel('Damped oscillation')

with example(ui.line_plot):
    from datetime import datetime

    import numpy as np

    line_plot = ui.line_plot(n=2, limit=20, figsize=(2.5, 1.8)) \
        .with_legend(['sin', 'cos'], loc='upper center', ncol=2)

    def update_line_plot() -> None:
        now = datetime.now()
        x = now.timestamp()
        y1 = np.sin(x)
        y2 = np.cos(x)
        line_plot.push([now], [[y1], [y2]])

    line_updates = ui.timer(0.1, update_line_plot, active=False)
    ui.checkbox('active').bind_value(line_updates, 'active')

with example(ui.scene):
    with ui.scene(width=200, height=200) as scene:
        scene.sphere().material('#4488ff')
        scene.cylinder(1, 0.5, 2, 20).material('#ff8800', opacity=0.5).move(-2, 1)
        scene.extrusion([[0, 0], [0, 1], [1, 0.5]], 0.1).material('#ff8888').move(-2, -2)

        with scene.group().move(z=2):
            box1 = scene.box().move(x=2)
            scene.box().move(y=2).rotate(0.25, 0.5, 0.75)
            scene.box(wireframe=True).material('#888888').move(x=2, y=2)

        scene.line([-4, 0, 0], [-4, 2, 0]).material('#ff0000')
        scene.curve([-4, 0, 0], [-4, -1, 0], [-3, -1, 0], [-3, -2, 0]).material('#008800')

        logo = "https://avatars.githubusercontent.com/u/2843826"
        scene.texture(logo, [[[0.5, 2, 0], [2.5, 2, 0]],
                             [[0.5, 0, 0], [2.5, 0, 0]]]).move(1, -2)

        teapot = 'https://upload.wikimedia.org/wikipedia/commons/9/93/Utah_teapot_(solid).stl'
        scene.stl(teapot).scale(0.2).move(-3, 4)

        scene.text('2D', 'background: rgba(0, 0, 0, 0.2); border-radius: 5px; padding: 5px').move(z=2)
        scene.text3d('3D', 'background: rgba(0, 0, 0, 0.2); border-radius: 5px; padding: 5px').move(y=-2).scale(.05)

with example(ui.tree):
    ui.tree([
        {'id': 'numbers', 'children': [{'id': '1'}, {'id': '2'}]},
        {'id': 'letters', 'children': [{'id': 'A'}, {'id': 'B'}]},
    ], label_key='id', on_select=lambda e: ui.notify(e.value))

with example(ui.log):
    from datetime import datetime

    log = ui.log(max_lines=10).classes('h-16')
    ui.button('Log time', on_click=lambda: log.push(datetime.now().strftime("%X.%f")[:-5]))

h3('Layout')

with example(ui.card):
    with ui.card().tight():
        ui.image('http://placeimg.com/640/360/nature')
        with ui.card_section():
            ui.label('Lorem ipsum dolor sit amet, consectetur adipiscing elit, ...')

with example(ui.column):
    with ui.column():
        ui.label('label 1')
        ui.label('label 2')
        ui.label('label 3')

with example(ui.row):
    with ui.row():
        ui.label('label 1')
        ui.label('label 2')
        ui.label('label 3')

clear_containers = '''#### Clear Containers

To remove all elements from a row, column or card container, use the `clear()` method.
'''
with example(clear_containers):
    container = ui.row()

    def add_face():
        with container:
            ui.icon('face')
    add_face()

    ui.button('Add', on_click=add_face)
    ui.button('Clear', on_click=container.clear)

with example(ui.expansion):
    with ui.expansion('Expand!', icon='work').classes('w-full'):
        ui.label('inside the expansion')

with example(ui.menu):
    choice = ui.label('Try the menu.')
    with ui.menu() as menu:
        ui.menu_item('Menu item 1', lambda: choice.set_text('Selected item 1.'))
        ui.menu_item('Menu item 2', lambda: choice.set_text('Selected item 2.'))
        ui.menu_item('Menu item 3 (keep open)', lambda: choice.set_text('Selected item 3.'), auto_close=False)
        ui.menu_separator()
        ui.menu_item('Close', on_click=menu.close)

    ui.button('Open menu', on_click=menu.open)

tooltips = '''#### Tooltips

Simply call the `tooltip(text:str)` method on UI elements to provide a tooltip.
'''
with example(tooltips):
    ui.label('Tooltips...').tooltip('...are shown on mouse over')
    ui.button().props('icon=thumb_up').tooltip('I like this')

with example(ui.notify):
    ui.button('Say hi!', on_click=lambda: ui.notify('Hi!', close_button='OK'))

with example(ui.dialog):
    with ui.dialog() as dialog, ui.card():
        ui.label('Hello world!')
        ui.button('Close', on_click=dialog.close)

    ui.button('Open a dialog', on_click=dialog.open)

async_dialog = '''#### Awaitable dialog

Dialogs can be awaited.
Use the `submit` method to close the dialog and return a result.
Canceling the dialog by clicking in the background or pressing the escape key yields `None`.
'''
with example(async_dialog):
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

design = '''#### Styling

NiceGUI uses the [Quasar Framework](https://quasar.dev/) version 1.0 and hence has its full design power.
Each NiceGUI element provides a `props` method whose content is passed [to the Quasar component](https://justpy.io/quasar_tutorial/introduction/#props-of-quasar-components):
Have a look at [the Quasar documentation](https://quasar.dev/vue-components/button#design) for all styling props.
You can also apply [Tailwind](https://tailwindcss.com/) utility classes with the `classes` method.

If you really need to apply CSS, you can use the `styles` method. Here the delimiter is `;` instead of a blank space.

All three functions also provide `remove` and `replace` parameters in case the predefined look is not wanted in a particular styling.
'''
with example(design):
    ui.radio(['x', 'y', 'z'], value='x').props('inline color=green')
    ui.button().props('icon=touch_app outline round').classes('shadow-lg')
    ui.label('Stylish!').style('color: #6E93D6; font-size: 200%; font-weight: 300')

with example(ui.colors):
    ui.colors()
    ui.button('Default', on_click=lambda: ui.colors())
    ui.button('Gray', on_click=lambda: ui.colors(primary='#555'))

h3('Action')

lifecycle = '''#### Lifecycle

You can run a function or coroutine as a parallel task by passing it to one of the following register methods:

- `ui.on_startup`: Called when NiceGUI is started or restarted.
- `ui.on_shutdown`: Called when NiceGUI is shut down or restarted.
- `ui.on_connect`: Called when a client connects to NiceGUI. (Optional argument: Starlette request)
- `ui.on_page_ready`: Called when the page is ready and the websocket is connected. (Optional argument: socket)
- `ui.on_disconnect`: Called when a client disconnects from NiceGUI.

When NiceGUI is shut down or restarted, the startup tasks will be automatically canceled.
'''
with example(lifecycle):
    import asyncio
    import time

    l = ui.label()

    async def run_clock():
        while True:
            l.text = f'unix time: {time.time():.1f}'
            await asyncio.sleep(1)

    ui.on_startup(run_clock)
    ui.on_connect(lambda: l.set_text('new connection'))

with example(ui.timer):
    from datetime import datetime

    with ui.row().classes('items-center'):
        clock = ui.label()
        t = ui.timer(interval=0.1, callback=lambda: clock.set_text(datetime.now().strftime("%X.%f")[:-5]))
        ui.checkbox('active').bind_value(t, 'active')

    with ui.row():
        def lazy_update() -> None:
            new_text = datetime.now().strftime('%X.%f')[:-5]
            if lazy_clock.text[:8] == new_text[:8]:
                return
            lazy_clock.text = new_text
        lazy_clock = ui.label()
        ui.timer(interval=0.1, callback=lazy_update)

with example(ui.keyboard):
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

bindings = '''#### Bindings

NiceGUI is able to directly bind UI elements to models.
Binding is possible for UI element properties like text, value or visibility and for model properties that are (nested) class attributes.

Each element provides methods like `bind_value` and `bind_visibility` to create a two-way binding with the corresponding property.
To define a one-way binding use the `_from` and `_to` variants of these methods.
Just pass a property of the model as parameter to these methods to create the binding.
'''
with example(bindings):
    class Demo:
        def __init__(self):
            self.number = 1

    demo = Demo()
    v = ui.checkbox('visible', value=True)
    with ui.column().bind_visibility_from(v, 'value'):
        ui.slider(min=1, max=3).bind_value(demo, 'number')
        ui.toggle({1: 'a', 2: 'b', 3: 'c'}).bind_value(demo, 'number')
        ui.number().bind_value(demo, 'number')

ui_updates = '''#### UI Updates

NiceGUI tries to automatically synchronize the state of UI elements with the client, e.g. when a label text, an input value or style/classes/props of an element have changed.
In other cases, you can explicitly call `element.update()` or `ui.update(*elements)` to update.
The example code shows both methods for a `ui.table`, where it is difficult to automatically detect changes in the `options` dictionary.
'''
with example(ui_updates):
    from random import randint

    def add():
        numbers.options.rowData.append({'numbers': randint(0, 100)})
        numbers.update()

    def clear():
        numbers.options.rowData.clear()
        ui.update(numbers)

    numbers = ui.table({'columnDefs': [{'field': 'numbers'}], 'rowData': []}).classes('max-h-40')
    ui.button('Add', on_click=add)
    ui.button('Clear', on_click=clear)

async_handlers = '''#### Async event handlers

Most elements also support asynchronous event handlers.

Note: You can also pass a `functools.partial` into the `on_click` property to wrap async functions with parameters.
'''
with example(async_handlers):
    async def async_task():
        ui.notify('Asynchronous task started')
        await asyncio.sleep(5)
        ui.notify('Asynchronous task finished')

    ui.button('start async task', on_click=async_task)

h3('Pages and Routes')

with example(ui.page):
    with ui.page('/other_page'):
        ui.label('Welcome to the other side')
        ui.link('Back to main page', '#page')

    with ui.page('/dark_page', dark=True):
        ui.label('Welcome to the dark side')
        ui.link('Back to main page', '#page')

    ui.link('Visit other page', 'other_page')
    ui.link('Visit dark page', 'dark_page')

with example(ui.open):
    with ui.page('/yet_another_page') as other:
        ui.label('Welcome to yet another page')
        ui.button('RETURN', on_click=lambda e: ui.open('#open', e.socket))

    ui.button('REDIRECT', on_click=lambda e: ui.open(other, e.socket))

add_route = '''#### Route

Add a new route by calling `ui.add_route` with a starlette route including a path and a function to be called.
Routed paths must start with a `'/'`.
'''
with example(add_route):
    import starlette

    ui.add_route(starlette.routing.Route(
        '/new/route', lambda _: starlette.responses.PlainTextResponse('Response')
    ))

    ui.link('Try the new route!', 'new/route')

get_decorator = '''#### Get decorator

Syntactic sugar to add routes.
Decorating a function with the `@ui.get` makes it available at the specified endpoint, e.g. `'/another/route/<id>'`.

Path parameters can be passed to the request handler like with [FastAPI](https://fastapi.tiangolo.com/tutorial/path-params/).
If type-annotated, they are automatically converted to `bool`, `int`, `float` and `complex` values.
An optional `request` argument gives access to the complete request object.
'''
with example(get_decorator):
    from starlette import requests, responses

    @ui.get('/another/route/{id}')
    def produce_plain_response(id: str, request: requests.Request):
        return responses.PlainTextResponse(f'{request.client.host} asked for id={id}')

    ui.link('Try yet another route!', 'another/route/42')

sessions = '''#### Sessions

`ui.page` provides an optional `on_connect` argument to register a callback.
It is invoked for each new connection to the page.

The optional `request` argument provides insights about the clients URL parameters etc. (see [the JustPy docs](https://justpy.io/tutorial/request_object/) for more details).
It also enables you to identify sessions over [longer time spans by configuring cookies](https://justpy.io/tutorial/sessions/).
'''
with example(sessions):
    from collections import Counter
    from datetime import datetime

    from starlette.requests import Request

    id_counter = Counter()
    creation = datetime.now().strftime('%H:%M, %d %B %Y')

    def handle_connection(request: Request):
        id_counter[request.session_id] += 1
        visits.set_text(f'{len(id_counter)} unique views ({sum(id_counter.values())} overall) since {creation}')

    with ui.page('/session_demo', on_connect=handle_connection) as page:
        visits = ui.label()

    ui.link('Visit session demo', page)

ui.run()
