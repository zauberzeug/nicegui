from typing import Any, Callable, Dict, Optional

from ...binding import BindableProperty, bind, bind_from, bind_to
from ...element import Element
from ...events import ValueChangeEventArguments, handle_event


class ValueElement(Element):
    VALUE_PROP = 'model-value'
    value = BindableProperty(on_change=lambda sender, value: sender.on_value_change(value))

    def __init__(self, *, value: Any, on_value_change: Optional[Callable], throttle: float = 0, **kwargs) -> None:
        super().__init__(**kwargs)
        self.set_value(value)
        self._props[self.VALUE_PROP] = self._value_to_model_value(value)
        self.change_handler = on_value_change

        def handle_change(msg: Dict) -> None:
            self.set_value(self._msg_to_value(msg))
        self.on(f'update:{self.VALUE_PROP}', handle_change, ['value'], throttle=throttle)

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

    def set_value(self, value: Any) -> None:
        self.value = value

    def on_value_change(self, value: Any) -> None:
        self._props[self.VALUE_PROP] = self._value_to_model_value(value)
        self.update()
        args = ValueChangeEventArguments(sender=self, client=self.client, value=self._value_to_event_value(value))
        handle_event(self.change_handler, args)

    def _msg_to_value(self, msg: Dict) -> Any:
        return msg['args']

    def _value_to_model_value(self, value: Any) -> Any:
        return value

    def _value_to_event_value(self, value: Any) -> Any:
        return value
