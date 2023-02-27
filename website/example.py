import contextlib
import inspect
import re
from typing import Callable, Optional, Union

import docutils.core
import isort

from nicegui import ui
from nicegui.elements.markdown import apply_tailwind, prepare_content

from .intersection_observer import IntersectionObserver as intersection_observer

REGEX_H4 = re.compile(r'<h4.*?>(.*?)</h4>')
SPECIAL_CHARACTERS = re.compile('[^(a-z)(A-Z)(0-9)-]')
PYTHON_BGCOLOR = '#00000010'
PYTHON_COLOR = '#eef5fb'
BASH_BGCOLOR = '#00000010'
BASH_COLOR = '#e8e8e8'
BROWSER_BGCOLOR = '#00000010'
BROWSER_COLOR = '#ffffff'


def remove_prefix(text: str, prefix: str) -> str:
    return text[len(prefix):] if text.startswith(prefix) else text


def add_html_with_anchor_link(html: str, menu: Optional[ui.drawer]) -> str:
    match = REGEX_H4.search(html)
    headline = match.groups()[0].strip()
    headline_id = SPECIAL_CHARACTERS.sub('_', headline).lower()
    icon = '<span class="material-icons">link</span>'
    link = f'<a href="#{headline_id}" class="hover:text-black auto-link" style="color: #ddd">{icon}</a>'
    target = f'<div id="{headline_id}" style="position: relative; top: -90px"></div>'
    html = html.replace('<h4', f'{target}<h4', 1)
    html = html.replace('</h4>', f' {link}</h4>', 1)

    ui.html(html).classes('documentation bold-links arrow-links')
    with menu or contextlib.nullcontext():
        async def click():
            if await ui.run_javascript(f'!!document.querySelector("div.q-drawer__backdrop")'):
                menu.hide()
                ui.open(f'#{headline_id}')
        ui.link(headline, f'#{headline_id}').props('data-close-overlay').on('click', click)


class example:

    def __init__(self,
                 content: Union[Callable, type, str],
                 menu: Optional[ui.drawer],
                 browser_title: Optional[str] = None,
                 immediate: bool = False) -> None:
        self.content = content
        self.menu = menu
        self.browser_title = browser_title
        self.immediate = immediate

    def __call__(self, f: Callable) -> Callable:
        with ui.column().classes('w-full mb-8'):
            if isinstance(self.content, str):
                html = prepare_content(self.content, 'fenced-code-blocks tables')
            else:
                doc = self.content.__doc__ or self.content.__init__.__doc__
                html: str = docutils.core.publish_parts(doc, writer_name='html5_polyglot')['html_body']
                html = html.replace('<p>', '<h4>', 1)
                html = html.replace('</p>', '</h4>', 1)
                html = html.replace('param ', '')
                html = apply_tailwind(html)
            add_html_with_anchor_link(html, self.menu)

            with ui.column().classes('w-full items-stretch gap-8 no-wrap min-[1500px]:flex-row'):
                code = inspect.getsource(f).split('# END OF EXAMPLE')[0].strip().splitlines()
                while not code[0].startswith(' ' * 8):
                    del code[0]
                code = ['from nicegui import ui'] + [remove_prefix(line[8:], '# ') for line in code]
                code = ['' if line == '#' else line for line in code]
                if not code[-1].startswith('ui.run('):
                    code.append('')
                    code.append('ui.run()')
                code = isort.code('\n'.join(code), no_sections=True, lines_after_imports=1)
                with python_window(classes='w-full max-w-[44rem]'):
                    ui.markdown(f'```python\n{code}\n```')
                with browser_window(self.browser_title,
                                    classes='w-full max-w-[44rem] min-[1500px]:max-w-[20rem] min-h-[10rem] browser-window'):
                    if self.immediate:
                        f()
                    else:
                        intersection_observer(on_intersection=f)

        return f


def _window_header(bgcolor: str) -> ui.row():
    return ui.row().classes(f'w-full h-8 p-2 bg-[{bgcolor}]')


def _dots() -> None:
    with ui.row().classes('gap-1 relative left-[1px] top-[1px]'):
        ui.icon('circle').classes('text-[13px] text-red-400')
        ui.icon('circle').classes('text-[13px] text-yellow-400')
        ui.icon('circle').classes('text-[13px] text-green-400')


def _title(title: str) -> None:
    ui.label(title).classes('text-sm text-gray-600 absolute left-1/2 top-[6px]').style('transform: translateX(-50%)')


def _tab(name: str, color: str, bgcolor: str) -> None:
    with ui.row().classes('gap-0'):
        with ui.label().classes(f'w-2 h-[24px] bg-[{color}]'):
            ui.label().classes(f'w-full h-full bg-[{bgcolor}] rounded-br-[6px]')
        ui.label(name).classes(f'text-sm text-gray-600 px-6 py-1 h-[24px] rounded-t-[6px] bg-[{color}]')
        with ui.label().classes(f'w-2 h-[24px] bg-[{color}]'):
            ui.label().classes(f'w-full h-full bg-[{bgcolor}] rounded-bl-[6px]')


def window(color: str, bgcolor: str, *, title: str = '', tab: str = '', classes: str = '') -> ui.column:
    with ui.card().classes(f'no-wrap bg-[{color}] rounded-xl p-0 gap-0 {classes}') \
            .style('box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1)'):
        with _window_header(bgcolor):
            _dots()
            if title:
                _title(title)
            if tab:
                _tab(tab, color, bgcolor)
        return ui.column().classes('w-full h-full overflow-auto')


def python_window(title: Optional[str] = None, *, classes: str = '') -> ui.card:
    return window(PYTHON_COLOR, PYTHON_BGCOLOR, title=title or 'main.py', classes=classes).classes('p-2 python-window')


def bash_window(*, classes: str = '') -> ui.card:
    return window(BASH_COLOR, BASH_BGCOLOR, title='bash', classes=classes).classes('p-2 bash-window')


def browser_window(title: Optional[str] = None, *, classes: str = '') -> ui.card:
    return window(BROWSER_COLOR, BROWSER_BGCOLOR, tab=title or 'NiceGUI', classes=classes).classes('p-4 browser-window')
