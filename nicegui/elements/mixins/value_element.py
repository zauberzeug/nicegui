from typing import Any, Callable, List, Optional, cast

from typing_extensions import Self

from ...binding import BindableProperty, bind, bind_from, bind_to
from ...element import Element
from ...events import GenericEventArguments, Handler, ValueChangeEventArguments, handle_event


class ValueElement(Element):
    VALUE_PROP: str = 'model-value'
    """Name of the prop that holds the value of the element"""

    LOOPBACK: Optional[bool] = True
    """Whether to set the new value directly on the client or after getting an update from the server.

    - ``True``: The value is updated by sending a change event to the server which responds with an update.
    - ``False``: The value is updated by setting the VALUE_PROP directly on the client.
    - ``None``: The value is updated automatically by the Vue element.
    """

    value = BindableProperty(
        on_change=lambda sender, value: cast(Self, sender)._handle_value_change(value))  # pylint: disable=protected-access

    def __init__(self, *,
                 value: Any,
                 on_value_change: Optional[Handler[ValueChangeEventArguments]] = None,
                 throttle: float = 0,
                 **kwargs: Any,
                 ) -> None:
        super().__init__(**kwargs)
        self._send_update_on_value_change = True
        self.set_value(value)
        self._props[self.VALUE_PROP] = self._value_to_model_value(value)
        self._props['loopback'] = self.LOOPBACK
        self._change_handlers: List[Handler[ValueChangeEventArguments]] = [on_value_change] if on_value_change else []

        def handle_change(e: GenericEventArguments) -> None:
            self._send_update_on_value_change = self.LOOPBACK is True
            self.set_value(self._event_args_to_value(e))
            self._send_update_on_value_change = True
        self.on(f'update:{self.VALUE_PROP}', handle_change, [None], throttle=throttle)

    def on_value_change(self, callback: Handler[ValueChangeEventArguments]) -> Self:
        """Add a callback to be invoked when the value changes."""
        self._change_handlers.append(callback)
        return self

    def bind_value_to(self,
                      target_object: Any,
                      target_name: str = 'value',
                      forward: Callable[..., Any] = lambda x: x,
                      ) -> Self:
        """Bind the value of this element to the target object's target_name property.

        The binding works one way only, from this element to the target.
        The update happens immediately and whenever a value changes.

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
        The update happens immediately and whenever a value changes.

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
        The update happens immediately and whenever a value changes.
        The backward binding takes precedence for the initial synchronization.

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

    def _handle_value_change(self, value: Any) -> None:
        self._props[self.VALUE_PROP] = self._value_to_model_value(value)
        if self._send_update_on_value_change:
            self.update()
        args = ValueChangeEventArguments(sender=self, client=self.client, value=self._value_to_event_value(value))
        for handler in self._change_handlers:
            handle_event(handler, args)

    def _event_args_to_value(self, e: GenericEventArguments) -> Any:
        return e.args

    def _value_to_model_value(self, value: Any) -> Any:
        return value

    def _value_to_event_value(self, value: Any) -> Any:
        return value
