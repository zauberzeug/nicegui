from typing import Any, Callable, Optional, cast

from typing_extensions import Self

from ...binding import BindableProperty, bind, bind_from, bind_to
from ...element import Element
from ...events import GenericEventArguments, ValueChangeEventArguments, handle_event


class ValueElement(Element):
    """
    Represents an element that has a value and supports binding to other objects.

    This class provides functionality for managing a value and binding it to other objects.
    It allows one-way and two-way binding, as well as customization of value transformations.

    Attributes:
        VALUE_PROP (str): The property name used to store the value in the element's properties.
        LOOPBACK (bool): A flag indicating whether to send updates back to the element when the value changes.

    Args:
        value (Any): The initial value of the element.
        on_value_change (Optional[Callable[..., Any]]): A callback function to be called when the value changes.
        throttle (float): The time interval (in seconds) to throttle value change events. Defaults to 0.
        **kwargs (Any): Additional keyword arguments to be passed to the base class constructor.

    Methods:
        bind_value_to(target_object, target_name='value', forward=lambda x: x) -> Self:
            Binds the value of this element to a property of the target object.
            The binding is one-way, from this element to the target object.

        bind_value_from(target_object, target_name='value', backward=lambda x: x) -> Self:
            Binds the value of this element from a property of the target object.
            The binding is one-way, from the target object to this element.

        bind_value(target_object, target_name='value', forward=lambda x: x, backward=lambda x: x) -> Self:
            Binds the value of this element to a property of the target object.
            The binding is two-way, allowing updates in both directions.

        set_value(value: Any) -> None:
            Sets the value of this element.

    Private Methods:
        _handle_value_change(value: Any) -> None:
            Handles the value change event and updates the element's properties and triggers the change handler.

        _event_args_to_value(e: GenericEventArguments) -> Any:
            Converts the event arguments to a value.

        _value_to_model_value(value: Any) -> Any:
            Converts the value to a model value.

        _value_to_event_value(value: Any) -> Any:
            Converts the value to an event value.
    """

    VALUE_PROP: str = 'model-value'
    LOOPBACK: bool = True
    value = BindableProperty(
        on_change=lambda sender, value: cast(Self, sender)._handle_value_change(value))  # pylint: disable=protected-access

    def __init__(self, *,
                     value: Any,
                     on_value_change: Optional[Callable[..., Any]],
                     throttle: float = 0,
                     **kwargs: Any,
                     ) -> None:
            """
            Initializes a ValueElement object.

            Args:
                value (Any): The initial value of the element.
                on_value_change (Optional[Callable[..., Any]]): A callback function that will be called when the value of the element changes.
                throttle (float, optional): The time in seconds to throttle the value change events. Defaults to 0.
                **kwargs (Any): Additional keyword arguments to be passed to the parent class.

            Returns:
                None

            Notes:
                - This method initializes a ValueElement object with the given value and callback function.
                - The `value` argument represents the initial value of the element.
                - The `on_value_change` argument is an optional callback function that will be called whenever the value of the element changes.
                - The `throttle` argument specifies the time in seconds to throttle the value change events. A value of 0 means no throttling.
                - Additional keyword arguments can be passed to the parent class using the `**kwargs` syntax.

            Example:
                # Create a ValueElement object with an initial value of 10 and a callback function
                def handle_value_change(new_value):
                    print(f"Value changed to: {new_value}")

                element = ValueElement(value=10, on_value_change=handle_value_change)

            """
            super().__init__(**kwargs)
            self._send_update_on_value_change = True
            self.set_value(value)
            self._props[self.VALUE_PROP] = self._value_to_model_value(value)
            self._props['loopback'] = self.LOOPBACK
            self._change_handler = on_value_change

            def handle_change(e: GenericEventArguments) -> None:
                self._send_update_on_value_change = self.LOOPBACK
                self.set_value(self._event_args_to_value(e))
                self._send_update_on_value_change = True
            self.on(f'update:{self.VALUE_PROP}', handle_change, [None], throttle=throttle)

    def bind_value_to(self,
                      target_object: Any,
                      target_name: str = 'value',
                      forward: Callable[..., Any] = lambda x: x,
                      ) -> Self:
        """
        Binds the value of this element to a property of the target object.
        The binding is one-way, from this element to the target object.

        Args:
            target_object (Any): The object to bind to.
            target_name (str): The name of the property to bind to. Defaults to 'value'.
            forward (Callable[..., Any]): A function to apply to the value before applying it to the target.

        Returns:
            Self: The current instance of the ValueElement.

        Example:
            >>> element = ValueElement(value=10)
            >>> target = SomeObject()
            >>> element.bind_value_to(target, 'some_property')
        """
        bind_to(self, 'value', target_object, target_name, forward)
        return self

    def bind_value_from(self,
                        target_object: Any,
                        target_name: str = 'value',
                        backward: Callable[..., Any] = lambda x: x,
                        ) -> Self:
        """
        Binds the value of this element from a property of the target object.
        The binding is one-way, from the target object to this element.

        Args:
            target_object (Any): The object to bind from.
            target_name (str): The name of the property to bind from. Defaults to 'value'.
            backward (Callable[..., Any]): A function to apply to the value before applying it to this element.

        Returns:
            Self: The current instance of the ValueElement.

        Example:
            >>> element = ValueElement(value=10)
            >>> target = SomeObject()
            >>> element.bind_value_from(target, 'some_property')
        """
        bind_from(self, 'value', target_object, target_name, backward)
        return self

    def bind_value(self,
                   target_object: Any,
                   target_name: str = 'value', *,
                   forward: Callable[..., Any] = lambda x: x,
                   backward: Callable[..., Any] = lambda x: x,
                   ) -> Self:
        """
        Binds the value of this element to a property of the target object.
        The binding is two-way, allowing updates in both directions.

        Args:
            target_object (Any): The object to bind to.
            target_name (str): The name of the property to bind to. Defaults to 'value'.
            forward (Callable[..., Any]): A function to apply to the value before applying it to the target.
            backward (Callable[..., Any]): A function to apply to the value before applying it to this element.

        Returns:
            Self: The current instance of the ValueElement.

        Example:
            >>> element = ValueElement(value=10)
            >>> target = SomeObject()
            >>> element.bind_value(target, 'some_property')
        """
        bind(self, 'value', target_object, target_name, forward=forward, backward=backward)
        return self

    def set_value(self, value: Any) -> None:
            """
            Sets the value of this element.

            This method allows you to set the value of the element to a specified value.

            Args:
                value (Any): The value to set.

            Example:
                >>> element = ValueElement(value=10)
                >>> element.set_value(20)

            Note:
                - The `value` parameter can be of any type.
                - The new value will replace the existing value of the element.
                - This method does not perform any validation on the value.

            Raises:
                None.

            Returns:
                None.
            """
            self.value = value

    def _handle_value_change(self, value: Any) -> None:
        """
        Handles the value change event and updates the element's properties and triggers the change handler.
        
        This method is called internally and should not be called directly.

        Args:
            value (Any): The new value.

        Returns:
            None

        Raises:
            None

        Notes:
            - This method is called internally and should not be called directly.
            - The `_handle_value_change` method is responsible for updating the element's properties and triggering the change handler when the value of the element changes.
            - It sets the new value in the `_props` dictionary using the `VALUE_PROP` key.
            - If `_send_update_on_value_change` is True, it calls the `update` method to update the element's appearance.
            - It creates a `ValueChangeEventArguments` object with the sender, client, and event value.
            - It calls the `handle_event` function with the change handler and the event arguments.
        """
        self._props[self.VALUE_PROP] = self._value_to_model_value(value)
        if self._send_update_on_value_change:
            self.update()
        args = ValueChangeEventArguments(sender=self, client=self.client, value=self._value_to_event_value(value))
        handle_event(self._change_handler, args)

    def _event_args_to_value(self, e: GenericEventArguments) -> Any:
            """
            Converts the event arguments to a value.

            This method is called internally and should not be called directly.

            Args:
                e (GenericEventArguments): The event arguments.

            Returns:
                Any: The converted value.

            Raises:
                None.
            """
            return e.args

    def _value_to_model_value(self, value: Any) -> Any:
        """
        Converts the value to a model value.

        Args:
            value (Any): The value to convert.

        Returns:
            Any: The converted model value.

        Example:
            This method is called internally and should not be called directly.
        """
        return value

    def _value_to_event_value(self, value: Any) -> Any:
        """
        Converts the value to an event value.

        Args:
            value (Any): The value to convert.

        Returns:
            Any: The converted event value.

        Example:
            This method is called internally and should not be called directly.
        """
        return value
