from pathlib import Path
from typing import Callable, Optional

from nicegui.dependencies import register_vue_component
from nicegui.element import Element

register_vue_component(name='counter', path=Path(__file__).parent / 'counter.js')


class Counter(Element):

    def __init__(self, title: str, *, on_change: Optional[Callable] = None) -> None:
        super().__init__('counter')
        self._props['title'] = title
        self.on('change', on_change)
        self.use_component('counter')

    def reset(self) -> None:
        self.run_method('reset')
