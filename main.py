
#!/usr/bin/env python3
from nicegui import ui, wp
from contextlib import contextmanager
import inspect
from nicegui.elements.markdown import Markdown
from nicegui.elements.element import Element
import sys
from typing import Union
import docutils.core
import icecream
icecream.install()

# add docutils css to webpage
wp.head_html += docutils.core.publish_parts('', writer_name='html')['stylesheet']

@contextmanager
def example(content: Union[Element, str]):

    callFrame = inspect.currentframe().f_back.f_back
    begin = callFrame.f_lineno
    with ui.row(classes='flex w-full'):

        if isinstance(content, str):
            ui.markdown(content, classes='mr-8 w-4/12')
        else:
            doc = content.__init__.__doc__
            if doc:
                html = docutils.core.publish_parts(doc, writer_name='html')['html_body']
                html = html.replace('<p>', '<h3>', 1)
                html = html.replace('</p>', '</h3>', 1)
                html = Markdown.apply_tailwind(html)
                ui.html(html, classes='mr-8 w-4/12')
            else:
                ui.label(content.__name__, 'h5')

        with ui.card(classes='mt-12 w-2/12'):
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
        ui.markdown(code, classes='mt-12 w-5/12 overflow-auto')


with open('README.md', 'r') as file:
    ui.markdown(file.read())


design = '''### Styling & Design

NiceGUI use the [Quasar Framework](https://quasar.dev/) and hence has their full design power. Each NiceGUI element provides a `design` property which content is passed [as props the Quasar component](https://justpy.io/quasar_tutorial/introduction/#props-of-quasar-components):
Have a look at [the Quasar documentation](https://quasar.dev/vue-components/button#design) for all styling "props".

You can also apply [Tailwind](https://tailwindcss.com/) utility classes with the `classes` property.
'''
with (example(design)):
    ui.radio(['x', 'y', 'z'], design='inline color=green')
    ui.button(icon='touch_app', design='outline round', classes='shadow-lg ml-14')


with example(ui.timer):
    from datetime import datetime

    clock = ui.label()
    t = ui.timer(interval=0.1, callback=lambda: clock.set_text(datetime.now().strftime("%X")))
    ui.checkbox('active').bind_value(t.active)

with example(ui.button):

    def button_increment():
        global button_count
        button_count += 1
        button_result.set_text(f'pressed: {button_count}')

    button_count = 0
    ui.button('Button', on_click=button_increment)
    button_result = ui.label('pressed: 0')

with example(ui.input):

    ui.input(
        label='Text',
        placeholder='press ENTER to apply',
        on_change=lambda e: result.set_text('you typed: ' + e.value)
    )
    result = ui.label('')

with example(ui.plot):
    from matplotlib import pyplot as plt
    import numpy as np

    with ui.plot(figsize=(2.5, 1.6)):
        x = np.linspace(0.0, 5.0)
        y = np.cos(2 * np.pi * x) * np.exp(-x)
        plt.plot(x, y, '-')
        plt.xlabel('time (s)')
        plt.ylabel('Damped oscillation')
