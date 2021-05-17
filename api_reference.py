
#!/usr/bin/env python3
from nicegui import ui, wp
from contextlib import contextmanager
from icecream import ic
import inspect
from executing import Source
import sys
import docutils.core

@contextmanager
def example():
    callFrame = inspect.currentframe().f_back.f_back
    begin = callFrame.f_lineno
    with ui.row():
        with ui.card():
            yield
        callFrame = inspect.currentframe().f_back.f_back
        end = callFrame.f_lineno
        code = inspect.getsource(sys.modules[__name__])
        code = code.splitlines()[begin:end]
        code.insert(0, '```python')
        code.append('```')
        code = '\n'.join(code)
        ui.markdown(code)

def describe(element, headline):
    doc = element.__init__.__doc__
    html = docutils.core.publish_parts(doc, writer_name='html')['html_body']
    ui.html(html)

describe(ui.input, 'Text Input')
with example():
    ui.input(label='Text', on_change=lambda e: result.set_text(e.value))
    ui.number(label='Number', format='%.2f', on_change=lambda e: result.set_text(e.value))

    result = ui.label('result', typography='bold')
