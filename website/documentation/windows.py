from collections.abc import Callable

from nicegui import helpers, ui
from nicegui.elements.markdown import remove_indentation

from .. import design as d
from ..utils import phosphor_icon
from .intersection_observer import IntersectionObserver as intersection_observer

ICONS = {
    'python': 'ph-file-py',
    'bash': 'ph-terminal-window',
    'ini': 'ph-file-ini',
}


def code_window(code: str = '', *, title: str = 'main.py', language: str = 'python') -> ui.column:
    """Create a window for code. If code is empty, returns the body column for use as context manager."""
    with ui.column().classes(f'rounded-xl gap-0 min-w-0 {d.BG_CODE} code-window') as window:
        with ui.row().classes(f'w-full px-4 h-16 gap-2 items-center {d.TEXT_13PX} {d.TEXT_MUTED} {d.BORDER_B}'):
            phosphor_icon(ICONS.get(language, 'ph-file')).classes('text-base')
            ui.label(title)
            if code:
                ui.space()
                with ui.button(on_click=lambda: ui.clipboard.write(code)) \
                        .props('flat round size=sm').classes('opacity-30 hover:opacity-100 transition-opacity'):
                    phosphor_icon('ph-copy').classes('text-lg')
        if code:
            ui.markdown(f'````{language}\n{remove_indentation(code)}\n````') \
                .classes('w-full h-full px-4 py-2 overflow-auto')
    return window


def bash_window(code: str = '', *, title: str = 'bash') -> ui.column:
    """Create a window for bash code."""
    return code_window(code, title=title, language='bash')


def python_window(code: str = '', *, title: str = 'main.py') -> ui.column:
    """Create a window for Python code."""
    return code_window(code, title=title, language='python')


def browser_window(content: Callable, *, tab: str | Callable | None = None, lazy: bool = True) -> ui.column:
    """Create a browser window."""
    with ui.column().classes(f'rounded-xl gap-0 {d.BG_SURFACE} {d.BORDER} browser-window') as window:
        with ui.row().classes(f'w-full px-4 h-16 gap-2 items-center {d.TEXT_13PX} {d.TEXT_MUTED} {d.BORDER_B}'):
            if callable(tab):
                tab()
            else:
                phosphor_icon('ph-globe').classes('text-base')
                ui.label(tab or 'localhost:8080')

        with ui.column().classes('w-full h-full p-4'):
            if lazy:
                spinner = ui.image('/static/loading.gif').classes('w-8 h-8').props('no-spinner no-transition')

                @intersection_observer
                async def handle_intersection():
                    window.remove(spinner)
                    if helpers.is_coroutine_function(content):
                        result = await content()
                    else:
                        result = content()
                    if callable(result):
                        if helpers.is_coroutine_function(result):
                            await result()
                        else:
                            result()
            else:
                result = content()
                if callable(result):
                    assert not helpers.is_coroutine_function(result), \
                        'async functions are not supported in non-lazy demos'
                    result()
    return window
