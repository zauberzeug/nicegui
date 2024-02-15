from typing import Callable, Optional

from nicegui.element import Element


class Counter(Element, component='counter.js'):
    """
    A custom Vue component representing a counter.

    Args:
        title (str): The title of the counter.
        on_change (Optional[Callable]): Optional callback function to be called when the counter value changes.

    Attributes:
        _props (dict): A dictionary containing the properties of the counter.

    Methods:
        reset(): Resets the counter to its initial value.

    Example:
        counter = Counter(title='My Counter', on_change=handle_change)
        counter.reset()
    """

    def __init__(self, title: str, *, on_change: Optional[Callable] = None) -> None:
        super().__init__()
        self._props['title'] = title
        self.on('change', on_change)

    def reset(self) -> None:
        """
        Resets the counter to its initial value.
        """
        self.run_method('reset')
