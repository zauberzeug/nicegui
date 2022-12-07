import inspect
import re
from typing import Callable, Union

import docutils.core

from nicegui import ui
from nicegui.elements.markdown import apply_tailwind

REGEX_H4 = re.compile(r'<h4.*?>(.*?)</h4>')
SPECIAL_CHARACTERS = re.compile('[^(a-z)(A-Z)(0-9)-]')
PYTHON_BGCOLOR = '#e3e9f2'
PYTHON_COLOR = '#eff5ff'
BASH_BGCOLOR = '#dcdcdc'
BASH_COLOR = '#e8e8e8'
BROWSER_BGCOLOR = '#f2f2f2'
BROWSER_COLOR = '#ffffff'


class example:

    def __init__(self, content: Union[Callable, type, str]) -> None:
        self.content = content

    def __call__(self, f: Callable) -> Callable:
        with ui.row().classes('q-mb-xl'):
            if isinstance(self.content, str):
                documentation = ui.markdown(self.content)
            else:
                doc = self.content.__doc__ or self.content.__init__.__doc__
                html: str = docutils.core.publish_parts(doc, writer_name='html5_polyglot')['html_body']
                html = html.replace('<p>', '<h4>', 1)
                html = html.replace('</p>', '</h4>', 1)
                html = html.replace('param ', '')
                html = apply_tailwind(html)
                documentation = ui.html(html)
            _add_html_anchor(documentation)

            with ui.row().classes('items-stretch'):
                code = inspect.getsource(f).splitlines()
                indentation = len(code[0].split('@example')[0]) + 4
                while not code[0].startswith(' ' * indentation):
                    del code[0]
                code = [l[indentation:] for l in code]
                while code[0].startswith('global '):
                    del code[0]
                code.insert(0, '```python')
                code.insert(1, 'from nicegui import ui')
                if code[2].split()[0] not in ['from', 'import']:
                    code.insert(2, '')
                for l, line in enumerate(code):
                    if line.startswith('# ui.'):
                        code[l] = line[2:]
                    if line.startswith('# ui.run('):
                        break
                else:
                    code.append('')
                    code.append('ui.run()')
                code.append('```')
                code = '\n'.join(code)
                with python_window().classes(f'w-[43rem] overflow-auto'):
                    ui.markdown(code)
                with browser_window().classes('w-80'):
                    f()
        return f


def _add_html_anchor(element: ui.html) -> None:
    html = element.content
    match = REGEX_H4.search(html)
    if not match:
        return
    headline = match.groups()[0].strip()
    headline_id = SPECIAL_CHARACTERS.sub('_', headline).lower()
    if not headline_id:
        return

    icon = '<span class="material-icons">link</span>'
    link = f'<a href="reference#{headline_id}" class="hover:text-black" style="color: #ddd">{icon}</a>'
    target = f'<div id="{headline_id}" style="position: relative; top: -90px"></div>'
    html = html.replace('<h4', f'{target}<h4', 1)
    html = html.replace('</h4>', f' {link}</h4>', 1)
    element.content = html


def _window_header(bgcolor: str) -> ui.row():
    return ui.row().classes('h-8 p-2') \
        .style(f'background-color: {bgcolor}; margin: -16px -16px 0 -16px; width: calc(100% + 32px)')


def _dots() -> None:
    with ui.row().classes('gap-1 absolute').style('left: 10px; top: 10px'):
        ui.icon('circle').style('font-size: 75%').classes('text-red-400')
        ui.icon('circle').style('font-size: 75%').classes('text-yellow-400')
        ui.icon('circle').style('font-size: 75%').classes('text-green-400')


def _title(title: str) -> None:
    ui.label(title).classes('text-sm text-gray-600 absolute').style('left: 50%; top: 6px; transform: translateX(-50%)')


def _tab(name: str, color: str, bgcolor: str) -> None:
    with ui.row().classes('absolute gap-0').style('left: 80px; top: 6px'):
        with ui.label().classes('w-2 h-[26px]').style(f'background-color: {color}'):
            ui.label().classes('w-full h-full').style(f'background-color: {bgcolor}; border-radius: 0 0 6px 0')
        ui.label(name).classes('text-sm text-gray-600 px-6 py-1') \
            .style(f'height: 26px; border-radius: 6px 6px 0 0; background-color: {color}')
        with ui.label().classes('w-2 h-[26px]').style(f'background-color: {color}'):
            ui.label().classes('w-full h-full').style(f'background-color: {bgcolor}; border-radius: 0 0 0 6px')


def window(color: str, bgcolor: str, *, title: str = '', tab: str = '') -> ui.card:
    with ui.card().classes('no-wrap rounded-xl').style(f'box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1); background: {color}') as card:
        with _window_header(bgcolor):
            _dots()
            if title:
                _title(title)
            if tab:
                _tab(tab, color, bgcolor)
    return card


def python_window() -> ui.card:
    return window(PYTHON_COLOR, PYTHON_BGCOLOR, title='main.py')


def bash_window() -> ui.card:
    return window(BASH_COLOR, BASH_BGCOLOR, title='bash')


def browser_window() -> ui.card:
    return window(BROWSER_COLOR, BROWSER_BGCOLOR, tab='NiceGUI')
