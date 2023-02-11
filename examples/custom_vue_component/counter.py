from typing import Callable, Optional

from nicegui.dependencies import register_component
from nicegui.element import Element

register_component('counter', __file__, 'counter.js')


class Counter(Element):

    def __init__(self, title: str, *, on_change: Optional[Callable] = None) -> None:
        super().__init__('counter')
        self._props['title'] = title
        self.on('change', on_change)

    def reset(self) -> None:
        self.run_method('reset')
