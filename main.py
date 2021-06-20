#!/usr/bin/env python3
from nicegui import ui, wp
from contextlib import contextmanager
import inspect
from nicegui.elements.markdown import Markdown
from nicegui.elements.element import Element
import sys
from typing import Union
import docutils.core
import re
import asyncio

# add docutils css to webpage
wp.head_html += docutils.core.publish_parts('', writer_name='html')['stylesheet']

@contextmanager
def example(content: Union[Element, str]):

    callFrame = inspect.currentframe().f_back.f_back
    begin = callFrame.f_lineno
    with ui.row().classes('flex w-full'):

        if isinstance(content, str):
            ui.markdown(content).classes('mr-8 w-4/12')
        else:
            doc = content.__init__.__doc__
            if doc:
                html = docutils.core.publish_parts(doc, writer_name='html')['html_body']
                html = html.replace('<p>', '<h3>', 1)
                html = html.replace('</p>', '</h3>', 1)
                html = Markdown.apply_tailwind(html)
                ui.html(html).classes('mr-8 w-4/12')
            else:
                ui.label(content.__name__).classes('text-h5')

        with ui.card().classes('mt-12 w-2/12'):
            yield
        callFrame = inspect.currentframe().f_back.f_back
        end = callFrame.f_lineno
        code = inspect.getsource(sys.modules[__name__])
        code = code.splitlines()[begin:end]
        code = [l[4:] for l in code]
        code.insert(0, '```python')
        code.insert(1, 'from nicegui import ui')
        code.append('```')
        code = '\n'.join(code)
        ui.markdown(code).classes('mt-12 w-5/12 overflow-auto')

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

design = '''### Styling & Design

NiceGUI uses the [Quasar Framework](https://quasar.dev/) and hence has its full design power.
Each NiceGUI element provides a `props` method whose content is passed [to the Quasar component](https://justpy.io/quasar_tutorial/introduction/#props-of-quasar-components):
Have a look at [the Quasar documentation](https://quasar.dev/vue-components/button#design) for all styling props.
You can also apply [Tailwind](https://tailwindcss.com/) utility classes with the `classes` method. 

If you really need to apply css you can use the `styles` method. Here the delimer is `;` instad of a blank space.
'''
with (example(design)):

    ui.radio(['x', 'y', 'z']).props('inline color=green')
    ui.button().props('icon=touch_app outline round').classes('shadow-lg ml-14')

binding = '''### Bindings

With help of the [binding](https://pypi.org/project/binding/) package NiceGUI is able to directly bind UI elements to models.
Binding is possible for UI element properties like text, value or visibility and for model properties that are (nested) class attributes.

Each element provides methods like `bind_value` and `bind_visibility` to create a two-way binding with the corresponding property.
To define a one-way binding use the `_from` and `_to` variants of these methods.
Just pass a property of the model as parameter to these methods to create the binding.
'''
with (example(binding)):

    class Demo:

        def __init__(self):
            self.number = 1

    demo = Demo()
    v = ui.checkbox('visible', value=True)
    with ui.column().bind_visibility_from(v.value):
        ui.slider(min=1, max=3).bind_value(demo.number)
        ui.toggle({1: 'a', 2: 'b', 3: 'c'}).bind_value(demo.number)
        ui.number().bind_value(demo.number)

lifecycle = '''### Lifecycle

You can run a function or coroutine on startup as a parallel task by passing it to `ui.on_startup`.
If NiceGui is shut down or restarted the tasks will be automatically canceled (for example when you make a code change).
You can also execude cleanup code with `ui.on_shutdown`.
'''
with (example(lifecycle)):

    count_label = ui.label('count: 0')
    count = 0

    async def update_count():
        global count
        while True:
            count_label.text = f'count: {count}'
            count += 1
            await asyncio.sleep(1)

    ui.on_startup(update_count())


with example(ui.timer):
    from datetime import datetime

    clock = ui.label()
    t = ui.timer(interval=0.1, callback=lambda: clock.set_text(datetime.now().strftime("%X")))
    ui.checkbox('active').bind_value(t.active)

with example(ui.label):

    ui.label('some label')

with example(ui.markdown):

    ui.markdown('### Headline\nWith hyperlink to [GitHub](https://github.com/zauberzeug/nicegui).')

with example(ui.html):

    ui.html('<p>demo paragraph in <strong>html</strong></p>')

with example(ui.button):

    def button_increment():
        global button_count
        button_count += 1
        button_result.set_text(f'pressed: {button_count}')

    button_count = 0
    ui.button('Button', on_click=button_increment)
    button_result = ui.label('pressed: 0')

with example(ui.checkbox):

    ui.checkbox('check me', on_change=lambda e: checkbox_state.set_text(e.value))
    with ui.row():
        ui.label('the checkbox is:')
        checkbox_state = ui.label('False')

with example(ui.switch):

    ui.switch('switch me', on_change=lambda e: switch_state.set_text("ON" if e.value else'OFF'))
    with ui.row():
        ui.label('the switch is:')
        switch_state = ui.label('OFF')

with example(ui.slider):

    slider = ui.slider(min=0, max=100, value=50).props('label')
    ui.label().bind_text_from(slider.value)

with example(ui.input):

    ui.input(
        label='Text',
        placeholder='press ENTER to apply',
        on_change=lambda e: result.set_text('you typed: ' + e.value),
    ).classes('w-full')
    result = ui.label('')

with example(ui.number):

    number_input = ui.number(label='Number', value=3.1415927, format='%.2f')
    with ui.row():
        ui.label('underlying value: ')
        ui.label().bind_text_from(number_input.value)

with example(ui.radio):

    radio = ui.radio([1, 2, 3], value=1).props('inline')
    ui.radio({1: 'A', 2: 'B', 3: 'C'}, value=1).props('inline').bind_value(radio.value)

with example(ui.toggle):

    toggle = ui.toggle([1, 2, 3], value=1)
    ui.toggle({1: 'A', 2: 'B', 3: 'C'}, value=1).bind_value(toggle.value)

with example(ui.select):

    with ui.row():
        select = ui.select([1, 2, 3], value=1).props('inline')
        ui.select({1: 'One', 2: 'Two', 3: 'Three'}, value=1).props('inline').bind_value(select.value)

with example(ui.plot):
    from matplotlib import pyplot as plt
    import numpy as np

    with ui.plot(figsize=(2.5, 1.8)):
        x = np.linspace(0.0, 5.0)
        y = np.cos(2 * np.pi * x) * np.exp(-x)
        plt.plot(x, y, '-')
        plt.xlabel('time (s)')
        plt.ylabel('Damped oscillation')

with example(ui.line_plot):

    lines = ui.line_plot(n=2, limit=20, figsize=(2.5, 1.8)).with_legend(['sin', 'cos'], loc='upper center', ncol=2)
    line_updates = ui.timer(0.1, lambda: lines.push([datetime.now()], [
        [np.sin(datetime.now().timestamp()) + 0.02 * np.random.randn()],
        [np.cos(datetime.now().timestamp()) + 0.02 * np.random.randn()],
    ]), active=False)
    ui.checkbox('active').bind_value(line_updates.active)

with example(ui.joystick):

    ui.joystick(
        color='blue',
        size=50,
        on_move=lambda msg: coordinates.set_text(f'{msg.data.vector.x:.3f}, {msg.data.vector.y:.3f}'),
        on_end=lambda _: coordinates.set_text('0, 0'))
    coordinates = ui.label('0, 0')
