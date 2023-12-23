from typing import Callable, Literal, Optional, Union

from nicegui import ui

WindowType = Literal['python', 'bash', 'browser']

WINDOW_BG_COLORS = {
    'python': ('#eef5fb', '#2b323b'),
    'bash': ('#e8e8e8', '#2b323b'),
    'browser': ('#ffffff', '#181c21'),
}


def _dots() -> None:
    with ui.row().classes('gap-1 relative left-[1px] top-[1px]'):
        ui.icon('circle').classes('text-[13px] text-red-400')
        ui.icon('circle').classes('text-[13px] text-yellow-400')
        ui.icon('circle').classes('text-[13px] text-green-400')


def _window(type_: WindowType, *, title: str = '', tab: Union[str, Callable] = '', classes: str = '') -> ui.column:
    bar_color = ('#00000010', '#ffffff10')
    color = WINDOW_BG_COLORS[type_]
    with ui.card().classes(f'no-wrap bg-[{color[0]}] dark:bg-[{color[1]}] rounded-xl p-0 gap-0 {classes}') \
            .style('box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1)'):
        with ui.row().classes(f'w-full h-8 p-2 bg-[{bar_color[0]}] dark:bg-[{bar_color[1]}]'):
            _dots()
            if title:
                ui.label(title) \
                    .classes('text-sm text-gray-600 dark:text-gray-400 absolute left-1/2 top-[6px]') \
                    .style('transform: translateX(-50%)')
            if tab:
                with ui.row().classes('gap-0'):
                    with ui.label().classes(f'w-2 h-[24px] bg-[{color[0]}] dark:bg-[{color[1]}]'):
                        ui.label().classes(
                            f'w-full h-full bg-[{bar_color[0]}] dark:bg-[{bar_color[1]}] rounded-br-[6px]')
                    with ui.row().classes(f'text-sm text-gray-600 dark:text-gray-400 px-6 py-1 h-[24px] rounded-t-[6px] bg-[{color[0]}] dark:bg-[{color[1]}] items-center gap-2'):
                        if callable(tab):
                            tab()
                        else:
                            ui.label(tab)
                    with ui.label().classes(f'w-2 h-[24px] bg-[{color[0]}] dark:bg-[{color[1]}]'):
                        ui.label().classes(
                            f'w-full h-full bg-[{bar_color[0]}] dark:bg-[{bar_color[1]}] rounded-bl-[6px]')
        return ui.column().classes('w-full h-full overflow-auto')


def python_window(title: Optional[str] = None, *, classes: str = '') -> ui.column:
    """Create a window for Python code."""
    return _window('python', title=title or 'main.py', classes=classes).classes('px-4 py-2 python-window')


def bash_window(*, classes: str = '') -> ui.column:
    """Create a window for Bash code."""
    return _window('bash', title='bash', classes=classes).classes('px-4 py-2 bash-window')


def browser_window(title: Optional[Union[str, Callable]] = None, *, classes: str = '') -> ui.column:
    """Create a browser window."""
    return _window('browser', tab=title or 'NiceGUI', classes=classes).classes('p-4 browser-window')
