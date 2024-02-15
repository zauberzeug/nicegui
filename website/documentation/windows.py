from typing import Callable, Literal, Optional, Union

from nicegui import ui

WindowType = Literal['python', 'bash', 'browser']

WINDOW_BG_COLORS = {
    'python': ('#eef5fb', '#2b323b'),
    'bash': ('#e8e8e8', '#2b323b'),
    'browser': ('#ffffff', '#181c21'),
}


def _dots() -> None:
    """
    Display three colored dots in a row.

    This function creates a row of three dots, each with a different color.
    The dots are represented by circle icons, with the colors red, yellow, and green.

    Example usage:
    _dots()

    """
    with ui.row().classes('gap-1 relative left-[1px] top-[1px]'):
        ui.icon('circle').classes('text-[13px] text-red-400')
        ui.icon('circle').classes('text-[13px] text-yellow-400')
        ui.icon('circle').classes('text-[13px] text-green-400')


def _window(type_: WindowType, *, title: str = '', tab: Union[str, Callable] = '', classes: str = '') -> ui.column:
    """
    Create a window with a specific type, title, tab, and classes.

    Args:
        type_ (WindowType): The type of the window.
        title (str, optional): The title of the window. Defaults to ''.
        tab (Union[str, Callable], optional): The tab of the window. Defaults to ''.
        classes (str, optional): Additional CSS classes for the window. Defaults to ''.

    Returns:
        ui.column: The created window as a column.

    Raises:
        None

    Example:
        # Create a window with type 'main', title 'My Window', and no tab
        window = _window(WindowType.MAIN, title='My Window')

        # Create a window with type 'dialog', title 'Dialog Window', tab 'Tab 1', and additional classes 'my-class'
        window = _window(WindowType.DIALOG, title='Dialog Window', tab='Tab 1', classes='my-class')
    """

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
    """
    Create a window for Python code.

    Args:
        title (Optional[str]): The title of the window. If not provided, the default title will be 'main.py'.
        classes (str): Additional CSS classes to apply to the window.

    Returns:
        ui.column: A column element representing the Python window.

    Example:
        To create a Python window with a custom title and additional CSS classes:

        >>> python_window(title='My Python Window', classes='custom-class')

    This function creates a window specifically designed for displaying Python code. It returns a column element
    that can be added to a UI layout. The window is styled with the 'python-window' class and can be further
    customized by providing additional CSS classes.

    Note:
        The 'python-window' class is automatically applied to the window to provide default styling. If you want
        to override the default styling, you can provide your own CSS classes using the 'classes' argument.

    """
    return _window('python', title=title or 'main.py', classes=classes).classes('px-4 py-2 python-window')


def bash_window(*, classes: str = '') -> ui.column:
    """
    Create a window for Bash code.

    This function creates a window specifically designed for displaying and interacting with Bash code.
    It returns a `ui.column` object representing the Bash window.

    Parameters:
        classes (str, optional): Additional CSS classes to apply to the Bash window. Defaults to an empty string.

    Returns:
        ui.column: The created Bash window.

    Example:
        # Create a Bash window with custom CSS classes
        bash_win = bash_window(classes='my-custom-class')

    Note:
        The `bash_window` function internally calls the `_window` function to create the window.
        The title of the window is set to 'bash', and additional CSS classes are applied to customize its appearance.
        The resulting Bash window is a `ui.column` object that can be further customized or added to a UI layout.
    """
    return _window('bash', title='bash', classes=classes).classes('px-4 py-2 bash-window')


def browser_window(title: Optional[Union[str, Callable]] = None, *, classes: str = '') -> ui.column:
    """
    Create a browser window.

    Args:
        title (Optional[Union[str, Callable]], optional): The title of the browser window. 
            It can be a string or a callable that returns a string. Defaults to None.
        classes (str, optional): Additional CSS classes to apply to the browser window. 
            Defaults to ''.

    Returns:
        ui.column: A column element representing the browser window.

    Example:
        # Create a browser window with a custom title
        window = browser_window(title='My Browser Window')

        # Create a browser window with custom CSS classes
        window = browser_window(classes='my-custom-class')
    """
    return _window('browser', tab=title or 'NiceGUI', classes=classes).classes('p-4 browser-window')
