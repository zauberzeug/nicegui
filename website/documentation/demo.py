import inspect
import re
from typing import Callable, Optional, Union

import isort

from nicegui import helpers, json, ui

from .intersection_observer import IntersectionObserver as intersection_observer
from .windows import browser_window, python_window

UNCOMMENT_PATTERN = re.compile(r'^(\s*)# ?')


def _uncomment(text: str) -> str:
    return UNCOMMENT_PATTERN.sub(r'\1', text)  # NOTE: non-executed lines should be shown in the code examples


def demo(f: Callable, *, lazy: bool = True, tab: Optional[Union[str, Callable]] = None) -> Callable:
    """Render a callable as a demo with Python code and browser window."""
    with ui.column().classes('w-full items-stretch gap-8 no-wrap min-[1500px]:flex-row'):
        code = inspect.getsource(f).split('# END OF DEMO', 1)[0].strip().splitlines()
        code = [line for line in code if not line.endswith('# HIDE')]
        while not code[0].strip().startswith('def') and not code[0].strip().startswith('async def'):
            del code[0]
        del code[0]
        if code[0].strip().startswith('"""'):
            while code[0].strip() != '"""':
                del code[0]
            del code[0]
        indentation = len(code[0]) - len(code[0].lstrip())
        code = [line[indentation:] for line in code]
        code = ['from nicegui import ui'] + [_uncomment(line) for line in code]
        code = ['' if line == '#' else line for line in code]
        if not code[-1].startswith('ui.run('):
            code.append('')
            code.append('ui.run()')
        full_code = isort.code('\n'.join(code), no_sections=True, lines_after_imports=1)
        with python_window(classes='w-full max-w-[44rem]'):
            ui.markdown(f'````python\n{full_code}\n````')
            ui.icon('content_copy', size='xs') \
                .classes('absolute right-2 top-10 opacity-10 hover:opacity-80 cursor-pointer') \
                .on('click', js_handler=f'() => navigator.clipboard.writeText({json.dumps(full_code)})') \
                .on('click', lambda: ui.notify('Copied to clipboard', type='positive', color='primary'), [])
        with browser_window(title=tab,
                            classes='w-full max-w-[44rem] min-[1500px]:max-w-[20rem] min-h-[10rem] browser-window') as window:
            if lazy:
                spinner = ui.spinner(size='lg').props('thickness=2')

                async def handle_intersection():
                    window.remove(spinner)
                    if helpers.is_coroutine_function(f):
                        await f()
                    else:
                        f()
                intersection_observer(on_intersection=handle_intersection)
            else:
                assert not helpers.is_coroutine_function(f), 'async functions are not supported in non-lazy demos'
                f()

    return f
