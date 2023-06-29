import inspect
import re
from typing import Callable, Optional, Union

import isort

from nicegui import ui

from .intersection_observer import IntersectionObserver as intersection_observer

PYTHON_BGCOLOR = '#00000010'
PYTHON_COLOR = '#eef5fb'
BASH_BGCOLOR = '#00000010'
BASH_COLOR = '#e8e8e8'
BROWSER_BGCOLOR = '#00000010'
BROWSER_COLOR = '#ffffff'


uncomment_pattern = re.compile(r'^(\s*)# ?')


def uncomment(text: str) -> str:
    """non-executed lines should be shown in the code examples"""
    return uncomment_pattern.sub(r'\1', text)


def demo(f: Callable) -> Callable:
    with ui.column().classes('w-full items-stretch gap-8 no-wrap min-[1500px]:flex-row'):
        code = inspect.getsource(f).split('# END OF DEMO')[0].strip().splitlines()
        code = [line for line in code if not line.endswith("# HIDE")]
        while not code[0].strip().startswith('def') and not code[0].strip().startswith('async def'):
            del code[0]
        del code[0]
        if code[0].strip().startswith('"""'):
            while code[0].strip() != '"""':
                del code[0]
            del code[0]
        indentation = len(code[0]) - len(code[0].lstrip())
        code = [line[indentation:] for line in code]
        code = ['from nicegui import ui'] + [uncomment(line) for line in code]
        code = ['' if line == '#' else line for line in code]
        if not code[-1].startswith('ui.run('):
            code.append('')
            code.append('ui.run()')
        code = isort.code('\n'.join(code), no_sections=True, lines_after_imports=1)
        with python_window(classes='w-full max-w-[44rem]'):
            async def copy_code():
                await ui.run_javascript('navigator.clipboard.writeText(`' + code + '`)', respond=False)
                ui.notify('Copied to clipboard', type='positive', color='primary')
            ui.markdown(f'````python\n{code}\n````')
            ui.icon('content_copy', size='xs') \
                .classes('absolute right-2 top-10 opacity-10 hover:opacity-80 cursor-pointer') \
                .on('click', copy_code, [])
        with browser_window(title=getattr(f, 'tab', None),
                            classes='w-full max-w-[44rem] min-[1500px]:max-w-[20rem] min-h-[10rem] browser-window'):
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


def _tab(content: Union[str, Callable], color: str, bgcolor: str) -> None:
    with ui.row().classes('gap-0'):
        with ui.label().classes(f'w-2 h-[24px] bg-[{color}]'):
            ui.label().classes(f'w-full h-full bg-[{bgcolor}] rounded-br-[6px]')
        with ui.row().classes(f'text-sm text-gray-600 px-6 py-1 h-[24px] rounded-t-[6px] bg-[{color}] items-center gap-2'):
            if callable(content):
                content()
            else:
                ui.label(content)
        with ui.label().classes(f'w-2 h-[24px] bg-[{color}]'):
            ui.label().classes(f'w-full h-full bg-[{bgcolor}] rounded-bl-[6px]')


def window(color: str, bgcolor: str, *,
           title: str = '', tab: Union[str, Callable] = '', classes: str = '') -> ui.column:
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


def browser_window(title: Optional[Union[str, Callable]] = None, *, classes: str = '') -> ui.card:
    return window(BROWSER_COLOR, BROWSER_BGCOLOR, tab=title or 'NiceGUI', classes=classes).classes('p-4 browser-window')
