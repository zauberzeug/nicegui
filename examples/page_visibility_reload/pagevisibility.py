from typing import Callable, Optional

from nicegui.dependencies import register_component
from nicegui.element import Element

register_component('pagevisibility', __file__, 'pagevisibility.js')


class AutoReloader(Element):

    def __init__(self, title: str, *, on_change: Optional[Callable] = None) -> None:
        super().__init__('pagevisibility')
        self._props['title'] = title
        self.on('change', on_change)
