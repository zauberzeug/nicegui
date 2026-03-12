from collections.abc import Callable

from nicegui.element import Element


class Counter(Element, component='counter.js'):

    def __init__(self, title: str, *, on_change: Callable | None = None) -> None:
        super().__init__()
        self._props['title'] = title
        self.on('change', on_change)

    def reset(self) -> None:
        self.run_method('reset')
