
#!/usr/bin/env python3
from nicegui import ui, wp
from contextlib import contextmanager
from icecream import ic
import inspect
from executing import Source
import sys

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

wp.css = HtmlFormatter().get_style_defs('.highlight')

@contextmanager
def example():
    callFrame = inspect.currentframe().f_back.f_back
    begin = callFrame.f_lineno
    with ui.card():
        with ui.row():
            with ui.column():
                yield
            callFrame = inspect.currentframe().f_back.f_back
            end = callFrame.f_lineno
            code = inspect.getsource(sys.modules[__name__])
            code = code.splitlines()[begin:end]
            code = '\n'.join(code)
            html = highlight(code, PythonLexer(), HtmlFormatter())
            label = ui.label()
            label.view.inner_html = html
            ic(html)

with example():

    ui.input(label='Text', on_change=lambda e: result.set_text(e.value))
    ui.number(label='Number', format='%.2f', on_change=lambda e: result.set_text(e.value))

    result = ui.label('result', typography='bold')
