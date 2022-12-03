import inspect
import re
from typing import Callable, Union

import docutils.core

from nicegui import ui
from nicegui.elements.markdown import apply_tailwind

REGEX_H4 = re.compile(r'<h4.*?>(.*?)</h4>')
SPECIAL_CHARACTERS = re.compile('[^(a-z)(A-Z)(0-9)-]')


class example:

    def __init__(self, content: Union[Callable, type, str], tight: bool = False) -> None:
        self.content = content
        self.markdown_classes = f'mr-8 w-full flex-none lg:w-{48 if tight else 80} xl:w-80'
        self.rendering_classes = f'w-{48 if tight else 64} flex-none lg:mt-12'
        self.source_classes = f'w-80 flex-grow overflow-auto lg:mt-12'

    def __call__(self, f: Callable) -> Callable:
        with ui.row().classes('mb-2 flex w-full'):
            if isinstance(self.content, str):
                _add_html_anchor(ui.markdown(self.content).classes(self.markdown_classes))
            else:
                doc = self.content.__doc__ or self.content.__init__.__doc__
                html: str = docutils.core.publish_parts(doc, writer_name='html')['html_body']
                html = html.replace('<p>', '<h4>', 1)
                html = html.replace('</p>', '</h4>', 1)
                html = apply_tailwind(html)
                _add_html_anchor(ui.html(html).classes(self.markdown_classes))

            with browser_window().classes(self.rendering_classes):
                f()

            code = inspect.getsource(f).splitlines()
            while not code[0].startswith(' ' * 8):
                del code[0]
            code = [l[8:] for l in code]
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
            with python_window().classes(self.source_classes):
                ui.markdown(code)
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
    anchor = f'<a href="reference#{headline_id}" class="text-gray-300 hover:text-black">{icon}</a>'
    html = html.replace('<h4', f'<h4 id="{headline_id}"', 1)
    html = html.replace('</h4>', f' {anchor}</h4>', 1)
    element.content = html


def _add_dots() -> None:
    with ui.row().classes('gap-1').style('transform: translate(-6px, -6px)'):
        ui.icon('circle').style('font-size: 75%').classes('text-red-400')
        ui.icon('circle').style('font-size: 75%').classes('text-yellow-400')
        ui.icon('circle').style('font-size: 75%').classes('text-green-400')


def window(color: str) -> ui.card:
    with ui.card().style(f'box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1); background: {color}') as card:
        _add_dots()
    return card


def python_window() -> ui.card:
    return window('#eff5ff')


def browser_window() -> ui.card:
    return window('white')


def bash_window() -> ui.card:
    return window('#e8e8e8')
