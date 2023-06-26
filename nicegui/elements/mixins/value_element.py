from typing import Any, Callable, Dict, List, Optional

from typing_extensions import Self

from ...binding import BindableProperty, bind, bind_from, bind_to
from ...element import Element
from ...events import ValueChangeEventArguments, handle_event


class ValueElement(Element):
    VALUE_PROP: str = 'model-value'
    EVENT_ARGS: Optional[List[str]] = ['value']
    LOOPBACK: bool = True
    value = BindableProperty(on_change=lambda sender, value: sender.on_value_change(value))

    def __init__(self, *,
                 value: Any,
                 on_value_change: Optional[Callable[..., Any]],
                 throttle: float = 0,
                 **kwargs: Any,
                 ) -> None:
        super().__init__(**kwargs)
        self.set_value(value)
        self._props[self.VALUE_PROP] = self._value_to_model_value(value)
        self._props['loopback'] = self.LOOPBACK
        self._send_update_on_value_change = True
        self.change_handler = on_value_change

        def handle_change(msg: Dict) -> None:
            self._send_update_on_value_change = self.LOOPBACK
            self.set_value(self._msg_to_value(msg))
            self._send_update_on_value_change = True
        self.on(f'update:{self.VALUE_PROP}', handle_change, self.EVENT_ARGS, throttle=throttle)

    def bind_value_to(self,
                      target_object: Any,
                      target_name: str = 'value',
                      forward: Callable[..., Any] = lambda x: x,
                      ) -> Self:
        """Bind the value of this element to the target object's target_name property.

        The binding works one way only, from this element to the target.

        :param target_object: The object to bind to.
        :param target_name: The name of the property to bind to.
        :param forward: A function to apply to the value before applying it to the target.
        """
        bind_to(self, 'value', target_object, target_name, forward)
        return self

    def bind_value_from(self,
                        target_object: Any,
                        target_name: str = 'value',
                        backward: Callable[..., Any] = lambda x: x,
                        ) -> Self:
        """Bind the value of this element from the target object's target_name property.

        The binding works one way only, from the target to this element.

        :param target_object: The object to bind from.
        :param target_name: The name of the property to bind from.
        :param backward: A function to apply to the value before applying it to this element.
        """
        bind_from(self, 'value', target_object, target_name, backward)
        return self

    def bind_value(self,
                   target_object: Any,
                   target_name: str = 'value', *,
                   forward: Callable[..., Any] = lambda x: x,
                   backward: Callable[..., Any] = lambda x: x,
                   ) -> Self:
        """Bind the value of this element to the target object's target_name property.

        The binding works both ways, from this element to the target and from the target to this element.

        :param target_object: The object to bind to.
        :param target_name: The name of the property to bind to.
        :param forward: A function to apply to the value before applying it to the target.
        :param backward: A function to apply to the value before applying it to this element.
        """
        bind(self, 'value', target_object, target_name, forward=forward, backward=backward)
        return self

    def set_value(self, value: Any) -> None:
        """Set the value of this element.

        :param value: The value to set.
        """
        self.value = value

    def on_value_change(self, value: Any) -> None:
        """Called when the value of this element changes.

        :param value: The new value.
        """
        self._props[self.VALUE_PROP] = self._value_to_model_value(value)
        if self._send_update_on_value_change:
            self.update()
        args = ValueChangeEventArguments(sender=self, client=self.client, value=self._value_to_event_value(value))
        handle_event(self.change_handler, args)

    def _msg_to_value(self, msg: Dict) -> Any:
        return msg['args']

    def _value_to_model_value(self, value: Any) -> Any:
        return value

    def _value_to_event_value(self, value: Any) -> Any:
        return value
