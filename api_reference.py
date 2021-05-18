
#!/usr/bin/env python3
from nicegui import ui, wp
from contextlib import contextmanager
from icecream import ic
import inspect
from executing import Source
from nicegui.elements.element import Element
import sys
import docutils.core

# add docutils css to webpage
wp.head_html += docutils.core.publish_parts('', writer_name='html')['stylesheet']

@contextmanager
def example(element: Element):

    callFrame = inspect.currentframe().f_back.f_back
    begin = callFrame.f_lineno
    with ui.row():

        doc = element.__init__.__doc__
        html = docutils.core.publish_parts(doc, writer_name='html')['html_body']
        html = html.replace('<p>', '<h3>', 1)
        html = html.replace('</p>', '</h3>', 1)
        ui.html(html)

        with ui.card(classes='mt-12'):
            yield
        callFrame = inspect.currentframe().f_back.f_back
        end = callFrame.f_lineno
        code = inspect.getsource(sys.modules[__name__])
        code = code.splitlines()[begin:end]
        code.insert(0, '```python')
        code.append('```')
        code = '\n'.join(code)
        ui.markdown(code, classes='mt-12')

with open('README.md', 'r') as file:
    ui.markdown(file.read())

with example(ui.input):
    ui.input(
        label='Text',
        placeholder='some placeholder',
        on_change=lambda e: result.set_text('you typed: ' + e.value)
    )
    result = ui.label('', typography='bold')
