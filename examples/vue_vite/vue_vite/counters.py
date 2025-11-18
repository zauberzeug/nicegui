from __future__ import annotations

from typing import Callable

from nicegui import ui


class CounterOptions(ui.element, component='components/CounterOptions.js'):

    def __init__(self, title: str, *, on_change: Callable | None = None) -> None:
        super().__init__()
        self._props['title'] = title
        self.on('change', on_change)

    def reset(self) -> None:
        self.run_method('reset')


class CounterComposition(ui.element, component='components/CounterComposition.js'):

    def __init__(self, title: str, *, on_change: Callable | None = None) -> None:
        super().__init__()
        self._props['title'] = title
        self.on('change', on_change)

    def reset(self) -> None:
        self.run_method('reset')
