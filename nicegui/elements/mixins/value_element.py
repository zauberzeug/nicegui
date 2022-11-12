from typing import Any, Callable, Dict

from ...binding import BindableProperty, bind, bind_from, bind_to
from ...element import Element
from ...events import ValueChangeEventArguments, handle_event


class ValueElement(Element):
    value = BindableProperty(on_change=lambda sender, value: sender.on_value_change(value))

    def init_value(self, value: Any, on_change: Callable) -> None:
        self.value = value
        self._props['model-value'] = value
        self.change_handler = on_change

        def handle_change(msg: Dict) -> None:
            self.value = msg['args']
        self.on('update:model-value', handle_change)

    def bind_value_to(self, target_object: Any, target_name: str = 'value', forward: Callable = lambda x: x):
        bind_to(self, 'value', target_object, target_name, forward)
        return self

    def bind_value_from(self, target_object: Any, target_name: str = 'value', backward: Callable = lambda x: x):
        bind_from(self, 'value', target_object, target_name, backward)
        return self

    def bind_value(self, target_object: Any, target_name: str = 'value', *,
                   forward: Callable = lambda x: x, backward: Callable = lambda x: x):
        bind(self, 'value', target_object, target_name, forward=forward, backward=backward)
        return self

    def set_value(self, value: str) -> None:
        self.value = value

    def on_value_change(self, value: str) -> None:
        self._props['model-value'] = value
        self.update()
        handle_event(self.change_handler, ValueChangeEventArguments(sender=self, client=self.client, value=value))
