from collections.abc import Callable

from nicegui import ui

from .code_extraction import get_full_code
from .windows import browser_window, python_window

GRID_CLASSES = 'w-full grid-cols-[1fr_20rem] max-lg:grid-cols-1 gap-4 items-stretch'
BROWSER_CLASSES = 'min-h-[10rem]'


def demo(f: Callable, *, lazy: bool = True, tab: str | Callable | None = None) -> Callable:
    """Render a callable as a demo with Python code and browser window."""
    with ui.grid().classes(GRID_CLASSES):
        full_code = get_full_code(f)
        python_window(full_code)
        browser_window(f, tab=tab, lazy=lazy).classes(BROWSER_CLASSES)

    return f
