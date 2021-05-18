
#!/usr/bin/env python3
from nicegui import ui, wp
from contextlib import contextmanager
import inspect
from nicegui.elements.element import Element
import sys
import docutils.core

# add docutils css to webpage
wp.head_html += docutils.core.publish_parts('', writer_name='html')['stylesheet']

@contextmanager
def example(element: Element):

    callFrame = inspect.currentframe().f_back.f_back
    begin = callFrame.f_lineno
    with ui.row(classes='flex w-full'):

        doc = element.__init__.__doc__
        if doc:
            html = docutils.core.publish_parts(doc, writer_name='html')['html_body']
            html = html.replace('<p>', '<h3>', 1)
            html = html.replace('</p>', '</h3>', 1)
            ui.html(html, classes='mr-8 w-4/12')
        else:
            ui.label(element.__name__, 'h5')

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
