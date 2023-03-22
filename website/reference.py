import uuid
from typing import Dict

from nicegui import app, ui
from nicegui.elements.markdown import prepare_content

from .example import add_html_with_anchor_link, bash_window, example, python_window

CONSTANT_UUID = str(uuid.uuid4())


def create_intro() -> None:
    @example('''#### Styling

While having reasonable defaults, you can still modify the look of your app with CSS as well as Tailwind and Quasar classes.
''', None)
    def formatting_example():
        ui.icon('thumb_up')
        ui.markdown('This is **Markdown**.')
        ui.html('This is <strong>HTML</strong>.')
        with ui.row():
            ui.label('CSS').style('color: #888; font-weight: bold')
            ui.label('Tailwind').classes('font-serif')
            ui.label('Quasar').classes('q-ml-xl')
        ui.link('NiceGUI on GitHub', 'https://github.com/zauberzeug/nicegui')

    @example('''#### Common UI Elements

NiceGUI comes with a collection of commonly used UI elements.
''', None)
    def common_elements_example():
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
        ui.link('And many more...', '/reference').classes('mt-8')

    @example('''#### Value Binding

Binding values between UI elements and data models is built into NiceGUI.
''', None)
    def binding_example():
        class Demo:
            def __init__(self):
                self.number = 1

        demo = Demo()
        v = ui.checkbox('visible', value=True)
        with ui.column().bind_visibility_from(v, 'value'):
            ui.slider(min=1, max=3).bind_value(demo, 'number')
            ui.toggle({1: 'A', 2: 'B', 3: 'C'}).bind_value(demo, 'number')
            ui.number().bind_value(demo, 'number')


def create_full(menu: ui.element) -> None:
    def h3(text: str) -> None:
        ui.html(f'<em>{text}</em>').classes('mt-8 text-3xl font-weight-500')
        with menu:
            ui.label(text).classes('font-bold mt-4')

    def add_markdown_with_headline(content: str):
        add_html_with_anchor_link(prepare_content(content, 'fenced-code-blocks'), menu)

    h3('Basic Elements')

    @example(ui.label, menu)
    def label_example():
        ui.label('some label')

    @example(ui.icon, menu)
    def icon_example():
        ui.icon('thumb_up')

    @example(ui.avatar, menu)
    def avatar_example():
        ui.avatar('favorite_border', text_color='grey-11', square=True)
        ui.avatar('img:https://nicegui.io/logo_square.png', color='blue-2')

    @example(ui.link, menu)
    def link_example():
        ui.link('NiceGUI on GitHub', 'https://github.com/zauberzeug/nicegui')

    @example(ui.button, menu)
    def button_example():
        ui.button('Click me!', on_click=lambda: ui.notify(f'You clicked me!'))

    @example(ui.badge, menu)
    def badge_example():
        with ui.button('Click me!', on_click=lambda: badge.set_text(int(badge.text) + 1)):
            badge = ui.badge('0', color='red').props('floating')

    @example(ui.toggle, menu)
    def toggle_example():
        toggle1 = ui.toggle([1, 2, 3], value=1)
        toggle2 = ui.toggle({1: 'A', 2: 'B', 3: 'C'}).bind_value(toggle1, 'value')

    @example(ui.radio, menu)
    def radio_example():
        radio1 = ui.radio([1, 2, 3], value=1).props('inline')
        radio2 = ui.radio({1: 'A', 2: 'B', 3: 'C'}).props('inline').bind_value(radio1, 'value')

    @example(ui.select, menu)
    def select_example():
        select1 = ui.select([1, 2, 3], value=1)
        select2 = ui.select({1: 'One', 2: 'Two', 3: 'Three'}).bind_value(select1, 'value')

    @example(ui.checkbox, menu)
    def checkbox_example():
        checkbox = ui.checkbox('check me')
        ui.label('Check!').bind_visibility_from(checkbox, 'value')

    @example(ui.switch, menu)
    def switch_example():
        switch = ui.switch('switch me')
        ui.label('Switch!').bind_visibility_from(switch, 'value')

    @example(ui.slider, menu)
    def slider_example():
        slider = ui.slider(min=0, max=100, value=50)
        ui.label().bind_text_from(slider, 'value')

    @example(ui.joystick, menu)
    def joystick_example():
        ui.joystick(color='blue', size=50,
                    on_move=lambda e: coordinates.set_text(f"{e.x:.3f}, {e.y:.3f}"),
                    on_end=lambda _: coordinates.set_text('0, 0'))
        coordinates = ui.label('0, 0')

    @example(ui.input, menu)
    def input_example():
        ui.input(label='Text', placeholder='start typing',
                 on_change=lambda e: result.set_text('you typed: ' + e.value),
                 validation={'Input too long': lambda value: len(value) < 20})
        result = ui.label()

    @example(ui.textarea, menu)
    def textarea_example():
        ui.textarea(label='Text', placeholder='start typing',
                    on_change=lambda e: result.set_text('you typed: ' + e.value))
        result = ui.label()

    @example(ui.number, menu)
    def number_example():
        ui.number(label='Number', value=3.1415927, format='%.2f',
                  on_change=lambda e: result.set_text(f'you entered: {e.value}'))
        result = ui.label()

    @example(ui.knob, menu)
    def knob_example():
        knob = ui.knob(0.3, show_value=True)

        with ui.knob(color='orange', track_color='grey-2').bind_value(knob, 'value'):
            ui.icon('volume_up')

    @example(ui.color_input, menu)
    def color_input_example():
        label = ui.label('Change my color!')
        ui.color_input(label='Color', value='#000000',
                       on_change=lambda e: label.style(f'color:{e.value}'))

    @example(ui.color_picker, menu)
    def color_picker_example():
        picker = ui.color_picker(on_pick=lambda e: button.style(f'background-color:{e.color}!important'))
        button = ui.button(on_click=picker.open).props('icon=colorize')

    @example(ui.date, menu)
    def date_example():
        ui.date(value='2023-01-01', on_change=lambda e: result.set_text(e.value))
        result = ui.label()

    @example(ui.time, menu)
    def time_example():
        ui.time(value='12:00', on_change=lambda e: result.set_text(e.value))
        result = ui.label()

    @example(ui.upload, menu)
    def upload_example():
        ui.upload(on_upload=lambda e: ui.notify(f'Uploaded {e.name}')).classes('max-w-full')

    h3('Markdown and HTML')

    @example(ui.markdown, menu)
    def markdown_example():
        ui.markdown('''This is **Markdown**.''')

    @example(ui.mermaid, menu)
    def mermaid_example():
        ui.mermaid('''
        graph LR;
            A --> B;
            A --> C;
        ''')

    @example(ui.html, menu)
    def html_example():
        ui.html('This is <strong>HTML</strong>.')

    @example('''#### SVG

You can add Scalable Vector Graphics using the `ui.html` element.
''', menu)
    def svg_example():
        content = '''
            <svg viewBox="0 0 200 200" width="100" height="100" xmlns="http://www.w3.org/2000/svg">
            <circle cx="100" cy="100" r="78" fill="#ffde34" stroke="black" stroke-width="3" />
            <circle cx="80" cy="85" r="8" />
            <circle cx="120" cy="85" r="8" />
            <path d="m60,120 C75,150 125,150 140,120" style="fill:none; stroke:black; stroke-width:8; stroke-linecap:round" />
            </svg>'''
        ui.html(content)

    h3('Images, Audio and Video')

    @example(ui.image, menu)
    def image_example():
        ui.image('https://picsum.photos/id/377/640/360')

    @example('''#### Captions and Overlays

By nesting elements inside a `ui.image` you can create augmentations.

Use [Quasar classes](https://quasar.dev/vue-components/img) for positioning and styling captions.
To overlay an SVG, make the `viewBox` exactly the size of the image and provide `100%` width/height to match the actual rendered size.
''', menu)
    def captions_and_overlays_example():
        with ui.image('https://picsum.photos/id/29/640/360'):
            ui.label('Nice!').classes('absolute-bottom text-subtitle2 text-center')

        with ui.image('https://cdn.stocksnap.io/img-thumbs/960w/airplane-sky_DYPWDEEILG.jpg'):
            ui.html('''
                <svg viewBox="0 0 960 638" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
                <circle cx="445" cy="300" r="100" fill="none" stroke="red" stroke-width="20" />
                </svg>
            ''').classes('bg-transparent')

    @example(ui.interactive_image, menu)
    def interactive_image_example():
        from nicegui.events import MouseEventArguments

        def mouse_handler(e: MouseEventArguments):
            color = 'SkyBlue' if e.type == 'mousedown' else 'SteelBlue'
            ii.content += f'<circle cx="{e.image_x}" cy="{e.image_y}" r="15" fill="none" stroke="{color}" stroke-width="4" />'
            ui.notify(f'{e.type} at ({e.image_x:.1f}, {e.image_y:.1f})')

        src = 'https://picsum.photos/id/565/640/360'
        ii = ui.interactive_image(src, on_mouse=mouse_handler, events=['mousedown', 'mouseup'], cross=True)

    @example(ui.audio, menu)
    def image_example():
        a = ui.audio('https://cdn.pixabay.com/download/audio/2022/02/22/audio_d1718ab41b.mp3')
        a.on('ended', lambda _: ui.notify('Audio playback completed'))

        ui.button(on_click=lambda: a.props('muted')).props('outline icon=volume_off')
        ui.button(on_click=lambda: a.props(remove='muted')).props('outline icon=volume_up')

    @example(ui.video, menu)
    def image_example():
        v = ui.video('https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/360/Big_Buck_Bunny_360_10s_1MB.mp4')
        v.on('ended', lambda _: ui.notify('Video playback completed'))

    h3('Data Elements')

    @example(ui.aggrid, menu)
    def aggrid_example():
        grid = ui.aggrid({
            'columnDefs': [
                {'headerName': 'Name', 'field': 'name'},
                {'headerName': 'Age', 'field': 'age'},
            ],
            'rowData': [
                {'name': 'Alice', 'age': 18},
                {'name': 'Bob', 'age': 21},
                {'name': 'Carol', 'age': 42},
            ],
            'rowSelection': 'multiple',
        }).classes('max-h-40')

        def update():
            grid.options['rowData'][0]['age'] += 1
            grid.update()

        ui.button('Update', on_click=update)
        ui.button('Select all', on_click=lambda: grid.call_api_method('selectAll'))

    @example(ui.table, menu)
    def table_example():
        columns = [
            {'name': 'name', 'label': 'Name', 'field': 'name', 'required': True, 'align': 'left'},
            {'name': 'age', 'label': 'Age', 'field': 'age', 'sortable': True},
        ]
        rows = [
            {'name': 'Alice', 'age': 18},
            {'name': 'Bob', 'age': 21},
            {'name': 'Carol'},
        ]
        ui.table(columns=columns, rows=rows, row_key='name')

    @example(ui.chart, menu)
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

    @example(ui.pyplot, menu)
    def plot_example():
        import numpy as np
        from matplotlib import pyplot as plt

        with ui.pyplot(figsize=(3, 2)):
            x = np.linspace(0.0, 5.0)
            y = np.cos(2 * np.pi * x) * np.exp(-x)
            plt.plot(x, y, '-')

    @example(ui.line_plot, menu)
    def line_plot_example():
        from datetime import datetime

        import numpy as np

        line_plot = ui.line_plot(n=2, limit=20, figsize=(3, 2), update_every=5) \
            .with_legend(['sin', 'cos'], loc='upper center', ncol=2)

        def update_line_plot() -> None:
            now = datetime.now()
            x = now.timestamp()
            y1 = np.sin(x)
            y2 = np.cos(x)
            line_plot.push([now], [[y1], [y2]])

        line_updates = ui.timer(0.1, update_line_plot, active=False)
        line_checkbox = ui.checkbox('active').bind_value(line_updates, 'active')

        # END OF EXAMPLE
        def handle_change(msg: Dict) -> None:
            def turn_off() -> None:
                line_checkbox.set_value(False)
                ui.notify('Turning off that line plot to save resources on our live demo server. 😎')
            line_checkbox.value = msg['args']
            if line_checkbox.value:
                ui.timer(10.0, turn_off, once=True)
        line_checkbox.on('update:model-value', handle_change)

    @example(ui.plotly, menu)
    def plotly_example():
        import plotly.graph_objects as go

        fig = go.Figure(go.Scatter(x=[1, 2, 3, 4], y=[1, 2, 3, 2.5]))
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
        ui.plotly(fig).classes('w-full h-40')

    @example(ui.linear_progress, menu)
    def linear_progress_example():
        slider = ui.slider(min=0, max=1, step=0.01, value=0.5)
        ui.linear_progress().bind_value_from(slider, 'value')

    @example(ui.circular_progress, menu)
    def circular_progress_example():
        slider = ui.slider(min=0, max=1, step=0.01, value=0.5)
        ui.circular_progress().bind_value_from(slider, 'value')

    @example(ui.spinner, menu)
    def spinner_example():
        with ui.row():
            ui.spinner(size='lg')
            ui.spinner('audio', size='lg', color='green')
            ui.spinner('dots', size='lg', color='red')

    @example(ui.scene, menu)
    def scene_example():
        with ui.scene(width=285, height=285) as scene:
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

    @example(ui.tree, menu)
    def tree_example():
        ui.tree([
            {'id': 'numbers', 'children': [{'id': '1'}, {'id': '2'}]},
            {'id': 'letters', 'children': [{'id': 'A'}, {'id': 'B'}]},
        ], label_key='id', on_select=lambda e: ui.notify(e.value))

    @example(ui.log, menu)
    def log_example():
        from datetime import datetime

        log = ui.log(max_lines=10).classes('w-full h-20')
        ui.button('Log time', on_click=lambda: log.push(datetime.now().strftime('%X.%f')[:-5]))

    h3('Layout')

    @example(ui.card, menu)
    def card_example():
        with ui.card().tight() as card:
            ui.image('https://picsum.photos/id/684/640/360')
            with ui.card_section():
                ui.label('Lorem ipsum dolor sit amet, consectetur adipiscing elit, ...')

    @example(ui.column, menu)
    def column_example():
        with ui.column():
            ui.label('label 1')
            ui.label('label 2')
            ui.label('label 3')

    @example(ui.row, menu)
    def row_example():
        with ui.row():
            ui.label('label 1')
            ui.label('label 2')
            ui.label('label 3')

    @example('''#### Clear Containers

To remove all elements from a row, column or card container, use the `clear()` method.

Alternatively, you can remove individual elements with `remove(element)`, where `element` is an Element or an index.
''', menu)
    def clear_containers_example():
        container = ui.row()

        def add_face():
            with container:
                ui.icon('face')
        add_face()

        ui.button('Add', on_click=add_face)
        ui.button('Remove', on_click=lambda: container.remove(0))
        ui.button('Clear', on_click=container.clear)

    @example(ui.expansion, menu)
    def expansion_example():
        with ui.expansion('Expand!', icon='work').classes('w-full'):
            ui.label('inside the expansion')

    @example('''#### Tabs

The elements `ui.tabs`, `ui.tab`, `ui.tab_panels`, and `ui.tab_panel` resemble
[Quasar's tabs](https://quasar.dev/vue-components/tabs)
and [tab panels](https://quasar.dev/vue-components/tab-panels) API.

`ui.tabs` creates a container for the tabs. This could be placed in a `ui.header` for example.
`ui.tab_panels` creates a container for the tab panels with the actual content.
''', menu)
    def tabs_example():
        with ui.tabs() as tabs:
            ui.tab('Home', icon='home')
            ui.tab('About', icon='info')

        with ui.tab_panels(tabs, value='Home'):
            with ui.tab_panel('Home'):
                ui.label('This is the first tab')
            with ui.tab_panel('About'):
                ui.label('This is the second tab')

    @example(ui.menu, menu)
    def menu_example():
        with ui.row().classes('w-full items-center'):
            result = ui.label().classes('mr-auto')
            with ui.button(on_click=lambda: menu.open()).props('icon=menu'):
                with ui.menu() as menu:
                    ui.menu_item('Menu item 1', lambda: result.set_text('Selected item 1'))
                    ui.menu_item('Menu item 2', lambda: result.set_text('Selected item 2'))
                    ui.menu_item('Menu item 3 (keep open)',
                                 lambda: result.set_text('Selected item 3'), auto_close=False)
                    ui.separator()
                    ui.menu_item('Close', on_click=menu.close)

    @example('''#### Tooltips

Simply call the `tooltip(text:str)` method on UI elements to provide a tooltip.

For more artistic control you can nest tooltip elements and apply props, classes and styles.
''', menu)
    def tooltips_example():
        ui.label('Tooltips...').tooltip('...are shown on mouse over')
        with ui.button().props('icon=thumb_up'):
            ui.tooltip('I like this').classes('bg-green')

    @example(ui.notify, menu)
    def notify_example():
        ui.button('Say hi!', on_click=lambda: ui.notify('Hi!', close_button='OK'))

    @example(ui.dialog, menu)
    def dialog_example():
        with ui.dialog() as dialog, ui.card():
            ui.label('Hello world!')
            ui.button('Close', on_click=dialog.close)

        ui.button('Open a dialog', on_click=dialog.open)

    @example('''#### Awaitable dialog

Dialogs can be awaited.
Use the `submit` method to close the dialog and return a result.
Canceling the dialog by clicking in the background or pressing the escape key yields `None`.
''', menu)
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
''', menu)
    def design_example():
        ui.radio(['x', 'y', 'z'], value='x').props('inline color=green')
        ui.button().props('icon=touch_app outline round').classes('shadow-lg')
        ui.label('Stylish!').style('color: #6E93D6; font-size: 200%; font-weight: 300')

    @example(ui.colors, menu)
    def colors_example():
        ui.button('Default', on_click=lambda: ui.colors())
        ui.button('Gray', on_click=lambda: ui.colors(primary='#555'))

    h3('Action')

    @example(ui.timer, menu)
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

    @example(ui.keyboard, menu)
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
''', menu)
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
''', menu)
    def ui_updates_example():
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

    @example('''#### Async event handlers

Most elements also support asynchronous event handlers.

Note: You can also pass a `functools.partial` into the `on_click` property to wrap async functions with parameters.
''', menu)
    def async_handlers_example():
        import asyncio

        async def async_task():
            ui.notify('Asynchronous task started')
            await asyncio.sleep(5)
            ui.notify('Asynchronous task finished')

        ui.button('start async task', on_click=async_task)

    h3('Pages')

    @example(ui.page, menu)
    def page_example():
        @ui.page('/other_page')
        def other_page():
            ui.label('Welcome to the other side')
            ui.link('Back to main page', '/reference#page')

        @ui.page('/dark_page', dark=True)
        def dark_page():
            ui.label('Welcome to the dark side')
            ui.link('Back to main page', '/reference#page')

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
''', menu)
    def auto_index_page():
        from uuid import uuid4

        @ui.page('/private_page')
        async def private_page():
            ui.label(f'private page with ID {uuid4()}')

        # ui.label(f'shared auto-index page with ID {uuid4()}')
        # ui.link('private page', private_page)
        # END OF EXAMPLE
        ui.label(f'shared auto-index page with ID {CONSTANT_UUID}')
        ui.link('private page', private_page)

    @example('''#### Pages with Path Parameters

Page routes can contain parameters like [FastAPI](https://fastapi.tiangolo.com/tutorial/path-params/>).
If type-annotated, they are automatically converted to bool, int, float and complex values.
If the page function expects a `request` argument, the request object is automatically provided.
The `client` argument provides access to the websocket connection, layout, etc.
''', menu)
    def page_with_path_parameters_example():
        @ui.page('/repeat/{word}/{count}')
        def page(word: str, count: int):
            ui.label(word * count)

        ui.link('Say hi to Santa!', 'repeat/Ho! /3')

    @example('''#### Wait for Client Connection

To wait for a client connection, you can add a `client` argument to the decorated page function
and await `client.connected()`.
All code below that statement is executed after the websocket connection between server and client has been established.

For example, this allows you to run JavaScript commands; which is only possible with a client connection (see [#112](https://github.com/zauberzeug/nicegui/issues/112)).
Also it is possible to do async stuff while the user already sees some content.
''', menu)
    def wait_for_connected_example():
        import asyncio

        from nicegui import Client

        @ui.page('/wait_for_connection')
        async def wait_for_connection(client: Client):
            ui.label('This text is displayed immediately.')
            await client.connected()
            await asyncio.sleep(2)
            ui.label('This text is displayed 2 seconds after the page has been fully loaded.')
            ui.label(f'The IP address {client.ip} was obtained from the websocket.')

        ui.link('wait for connection', wait_for_connection)

    @example('''#### Page Layout

With `ui.header`, `ui.footer`, `ui.left_drawer` and `ui.right_drawer` you can add additional layout elements to a page.
The `fixed` argument controls whether the element should scroll or stay fixed on the screen.
The `top_corner` and `bottom_corner` arguments indicate whether a drawer should expand to the top or bottom of the page.
See <https://quasar.dev/layout/header-and-footer> and <https://quasar.dev/layout/drawer> for more information about possible props.
With `ui.page_sticky` you can place an element "sticky" on the screen.
See <https://quasar.dev/layout/page-sticky> for more information.
''', menu)
    def page_layout_example():
        @ui.page('/page_layout')
        async def page_layout():
            ui.label('CONTENT')
            [ui.label(f'Line {i}') for i in range(100)]
            with ui.header(elevated=True).style('background-color: #3874c8').classes('items-center justify-between'):
                ui.label('HEADER')
                ui.button(on_click=lambda: right_drawer.toggle()).props('flat color=white icon=menu')
            with ui.left_drawer(top_corner=True, bottom_corner=True).style('background-color: #d7e3f4'):
                ui.label('LEFT DRAWER')
            with ui.right_drawer(fixed=False).style('background-color: #ebf1fa').props('bordered') as right_drawer:
                ui.label('RIGHT DRAWER')
            with ui.footer().style('background-color: #3874c8'):
                ui.label('FOOTER')

        ui.link('show page with fancy layout', page_layout)

    @example(ui.open, menu)
    def ui_open_example():
        @ui.page('/yet_another_page')
        def yet_another_page():
            ui.label('Welcome to yet another page')
            ui.button('RETURN', on_click=lambda: ui.open('reference#open'))

        ui.button('REDIRECT', on_click=lambda: ui.open(yet_another_page))

    @example('''#### Sessions

The optional `request` argument provides insights about the client's URL parameters etc.
It also enables you to identify sessions using a [session middleware](https://www.starlette.io/middleware/#sessionmiddleware).
''', menu)
    def sessions_example():
        import uuid
        from collections import Counter
        from datetime import datetime

        from starlette.middleware.sessions import SessionMiddleware
        from starlette.requests import Request

        from nicegui import app

        # app.add_middleware(SessionMiddleware, secret_key='some_random_string')

        counter = Counter()
        start = datetime.now().strftime('%H:%M, %d %B %Y')

        @ui.page('/session_demo')
        def session_demo(request: Request):
            if 'id' not in request.session:
                request.session['id'] = str(uuid.uuid4())
            counter[request.session['id']] += 1
            ui.label(f'{len(counter)} unique views ({sum(counter.values())} overall) since {start}')

        ui.link('Visit session demo', session_demo)

    @example(ui.run_javascript, menu)
    def javascript_example():
        async def alert():
            await ui.run_javascript('alert("Hello!")', respond=False)

        async def get_date():
            time = await ui.run_javascript('Date()')
            ui.notify(f'Browser time: {time}')

        async def access_elements():
            await ui.run_javascript(f'getElement({label.id}).innerText += " Hello!"')

        ui.button('fire and forget', on_click=alert)
        ui.button('receive result', on_click=get_date)
        ui.button('access elements', on_click=access_elements)
        label = ui.label()

    h3('Routes')

    @example(app.add_static_files, menu)
    def add_static_files_example():
        from nicegui import app

        app.add_static_files('/examples', 'examples')
        ui.label('Some NiceGUI Examples').classes('text-h5')
        ui.link('AI interface', '/examples/ai_interface/main.py')
        ui.link('Custom FastAPI app', '/examples/fastapi/main.py')
        ui.link('Authentication', '/examples/authentication/main.py')

    @example('''#### API Responses

NiceGUI is based on [FastAPI](https://fastapi.tiangolo.com/).
This means you can use all of FastAPI's features.
For example, you can implement a RESTful API in addition to your graphical user interface.
You simply import the `app` object from `nicegui`.
Or you can run NiceGUI on top of your own FastAPI app by using `ui.run_with(app)` instead of starting a server automatically with `ui.run()`.

You can also return any other FastAPI response object inside a page function.
For example, you can return a `RedirectResponse` to redirect the user to another page if certain conditions are met.
This is used in our [authentication demo](https://github.com/zauberzeug/nicegui/tree/main/examples/authentication/main.py).
''', menu)
    def fastapi_example():
        import random

        from nicegui import app

        @app.get('/random/{max}')
        def generate_random_number(max: int):
            return {'min': 0, 'max': max, 'value': random.randint(0, max)}

        max = ui.number('max', value=100)
        ui.button('generate random number', on_click=lambda: ui.open(f'/random/{max.value:.0f}'))

    h3('Lifecycle')

    @example('''#### Events

You can register coroutines or functions to be called for the following events:

- `app.on_startup`: called when NiceGUI is started or restarted
- `app.on_shutdown`: called when NiceGUI is shut down or restarted
- `app.on_connect`: called for each client which connects (optional argument: nicegui.Client)
- `app.on_disconnect`: called for each client which disconnects (optional argument: nicegui.Client)
- `app.on_exception`: called when an exception occurs (optional argument: exception)

When NiceGUI is shut down or restarted, all tasks still in execution will be automatically canceled.
''', menu)
    def lifecycle_example():
        from datetime import datetime

        from nicegui import app

        # dt = datetime.now()

        def handle_connection():
            global dt
            dt = datetime.now()
        app.on_connect(handle_connection)

        label = ui.label()
        ui.timer(1, lambda: label.set_text(f'Last new connection: {dt:%H:%M:%S}'))
        # END OF EXAMPLE
        global dt
        dt = datetime.now()

    @example(app.shutdown, menu)
    def shutdown_example():
        from nicegui import app

        # ui.button('shutdown', on_click=app.shutdown)
        #
        # ui.run(reload=False)
        # END OF EXAMPLE
        ui.button('shutdown', on_click=lambda: ui.notify(
            'Nah. We do not actually shutdown the documentation server. Try it in your own app!'))

    h3('NiceGUI Fundamentals')

    @example('''#### Auto-context

In order to allow writing intuitive UI descriptions, NiceGUI automatically tracks the context in which elements are created.
This means that there is no explicit `parent` parameter.
Instead the parent context is defined using a `with` statement.
It is also passed to event handlers and timers.

In the example, the label "Card content" is added to the card.
And because the `ui.button` is also added to the card, the label "Click!" will also be created in this context.
The label "Tick!", which is added once after one second, is also added to the card.

This design decision allows for easily creating modular components that keep working after moving them around in the UI.
For example, you can move label and button somewhere else, maybe wrap them in another container, and the code will still work.
''', menu)
    def auto_context_example():
        with ui.card():
            ui.label('Card content')
            ui.button('Add label', on_click=lambda: ui.label('Click!'))
            ui.timer(1.0, lambda: ui.label('Tick!'), once=True)

    @example('''#### Generic Events

Most UI elements come with predefined events.
For example, a `ui.button` like "A" in the example has an `on_click` parameter that expects a coroutine or function.
But you can also use the `on` method to register a generic event handler like for "B".
This allows you to register handlers for any event that is supported by JavaScript and Quasar.

For example, you can register a handler for the `mousemove` event like for "C", even though there is no `on_mousemove` parameter for `ui.button`.
Some events, like `mousemove`, are fired very often.
To avoid performance issues, you can use the `throttle` parameter to only call the handler every `throttle` seconds ("D").

The generic event handler can be synchronous or asynchronous and optionally takes an event dictionary as argument ("E").
You can also specify which attributes of the JavaScript or Quasar event should be passed to the handler ("F").
This can reduce the amount of data that needs to be transferred between the server and the client.

You can also include [key modifiers](https://vuejs.org/guide/essentials/event-handling.html#key-modifiers) ("G"),
modifier combinations ("H"),
and [event modifiers](https://vuejs.org/guide/essentials/event-handling.html#mouse-button-modifiers) ("I").
    ''', menu)
    def generic_events_example():
        with ui.row():
            ui.button('A', on_click=lambda: ui.notify('You clicked the button A.'))
            ui.button('B').on('click', lambda: ui.notify('You clicked the button B.'))
        with ui.row():
            ui.button('C').on('mousemove', lambda: ui.notify('You moved on button C.'))
            ui.button('D').on('mousemove', lambda: ui.notify('You moved on button D.'), throttle=0.5)
        with ui.row():
            ui.button('E').on('mousedown', lambda e: ui.notify(str(e)))
            ui.button('F').on('mousedown', lambda e: ui.notify(str(e)), ['ctrlKey', 'shiftKey'])
        with ui.row():
            ui.input('G').classes('w-12').on('keydown.space', lambda: ui.notify('You pressed space.'))
            ui.input('H').classes('w-12').on('keydown.y.shift', lambda: ui.notify('You pressed Shift+Y'))
            ui.input('I').classes('w-12').on('keydown.once', lambda: ui.notify('You started typing.'))
    h3('Configuration')

    @example(ui.run, menu, browser_title='My App')
    def ui_run_example():
        ui.label('page with custom title')

        # ui.run(title='My App')

    @example('''#### Environment Variables

You can set the following environment variables to configure NiceGUI:

- `MATPLOTLIB` (default: true) can be set to `false` to avoid the potentially costly import of Matplotlib. This will make `ui.pyplot` and `ui.line_plot` unavailable.
- `MARKDOWN_CONTENT_CACHE_SIZE` (default: 1000): The maximum number of Markdown content snippets that are cached in memory.
''', menu)
    def env_var_example():
        from nicegui.elements import markdown

        ui.label(f'Markdown content cache size is {markdown.prepare_content.cache_info().maxsize}')

    h3('Deployment')

    with ui.column().classes('w-full mb-8 bold-links arrow-links'):
        add_markdown_with_headline('''#### Server Hosting

To deploy your NiceGUI app on a server, you will need to execute your `main.py` (or whichever file contains your `ui.run(...)`) on your cloud infrastructure.
You can, for example, just install the [NiceGUI python package via pip](https://pypi.org/project/nicegui/) and use systemd or similar service to start the main script.
In most cases, you will set the port to 80 (or 443 if you want to use HTTPS) with the `ui.run` command to make it easily accessible from the outside.

A convenient alternative is the use of our [pre-built multi-arch Docker image](https://hub.docker.com/r/zauberzeug/nicegui) which contains all necessary dependencies.
With this command you can launch the script `main.py` in the current directory on the public port 80:
''')

        with bash_window(classes='max-w-lg w-full h-52'):
            ui.markdown('```bash\ndocker run -p 80:8080 -v $(pwd)/:/app/ \\\n    -d --restart always zauberzeug/nicegui:latest\n```')

        ui.markdown(
            '''The example assumes `main.py` uses the port 8080 in the `ui.run` command (which is the default).
The `-d` tells docker to run in background and `--restart always` makes sure the container is restarted if the app crashes or the server reboots.
Of course this can also be written in a Docker compose file:
''')
        with python_window('docker-compose.yml', classes='max-w-lg w-full h-52'):
            ui.markdown('''```yaml
app:
    image: zauberzeug/nicegui:latest
    restart: always
    ports:
        - 80:8080
    volumes:
        - ./:/app/
```
            ''')

        ui.markdown('''
You can provide SSL certificates directly using [FastAPI](https://fastapi.tiangolo.com/deployment/https/).
In production we also like using reverse proxies like [Traefik](https://doc.traefik.io/traefik/) or [NGINX](https://www.nginx.com/) to handle these details for us.
See our [docker-compose.yml](https://github.com/zauberzeug/nicegui/blob/main/docker-compose.yml) as an example.

You may also have a look at [our demo for using a custom FastAPI app](https://github.com/zauberzeug/nicegui/tree/main/examples/fastapi).
This will allow you to do very flexible deployments as described in the [FastAPI documentation](https://fastapi.tiangolo.com/deployment/).
Note that there are additional steps required to allow multiple workers.
''')

        with ui.column().classes('w-full mt-8 arrow-links'):
            add_markdown_with_headline('''#### Package for Installation

NiceGUI apps can also be bundled into an executable with [PyInstaller](https://www.pyinstaller.org/).
This allows you to distribute your app as a single file that can be executed on any computer.

Just take care your `ui.run` command does not use the `reload` argument.
Running the `build.py` below will create an executable `myapp` in the `dist` folder:
''')

        with ui.row().classes('w-full items-stretch'):
            with python_window(classes='max-w-lg w-full'):
                ui.markdown('''```python
from nicegui import ui

ui.label('Hello from Pyinstaller')

ui.run(reload=False)
```''')
            with python_window('build.py', classes='max-w-lg w-full'):
                ui.markdown('''```python
import os
import subprocess
from pathlib import Path
import nicegui

cmd = [
    'pyinstaller',
    'main.py', # your main file with ui.run()
    '--name', 'myapp', # name of your app
    '--onefile',
    '--add-data', f'{Path(nicegui.__file__).parent}{os.pathsep}nicegui'       
]
subprocess.call(cmd)
        ```''')

        ui.markdown('''

        ''')
