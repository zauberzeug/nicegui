from typing import Any, Callable, Dict, Optional

from ..element import Element
from ..events import ValueChangeEventArguments, handle_event
from .binding_mixins import BindValueMixin


class ValueElement(Element, BindValueMixin):

    def __init__(self, tag: str, *, value: Any, on_change: Optional[Callable]) -> None:
        super().__init__(tag)
        self.change_handler = on_change

        self.value = value
        self._props['model-value'] = value

        def handle_change(msg: Dict) -> None:
            self.value = msg['args']
        self.on('update:model-value', handle_change)

    def on_value_change(self, value: str) -> None:
        self._props['model-value'] = value
        self.update()
        handle_event(self.change_handler, ValueChangeEventArguments(sender=self, client=self.client, value=value))
