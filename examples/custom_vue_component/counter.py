from pathlib import Path
from typing import Callable, Optional

from nicegui.dependencies import register_vue_component
from nicegui.element import Element

component = register_vue_component(Path('counter.js'), base_path=Path(__file__).parent)


class Counter(Element):

    def __init__(self, title: str, *, on_change: Optional[Callable] = None) -> None:
        super().__init__(component.tag)
        self._props['title'] = title
        self.on('change', on_change)
        self.use_component(component)

    def reset(self) -> None:
        self.run_method('reset')
