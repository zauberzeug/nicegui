from typing import Any, Callable, cast

from typing_extensions import Self

from ...binding import BindableProperty, bind, bind_from, bind_to
from ...element import Element


class DisableableElement(Element):
    """
    A mixin class for creating disableable elements in NiceGUI.

    This class provides functionality for enabling and disabling an element,
    as well as binding the enabled state to another object's property.

    Attributes:
        enabled (BindableProperty): A bindable property representing the enabled state of the element.
        ignores_events_when_disabled (bool): A flag indicating whether the element should ignore events when disabled.

    Methods:
        __init__(self, **kwargs: Any): Initializes the DisableableElement instance.
        is_ignoring_events(self) -> bool: Returns whether the element is currently ignoring events.
        enable(self) -> None: Enables the element.
        disable(self) -> None: Disables the element.
        bind_enabled_to(self, target_object: Any, target_name: str = 'enabled', forward: Callable[..., Any] = lambda x: x) -> Self:
            Binds the enabled state of this element to the target object's target_name property.
        bind_enabled_from(self, target_object: Any, target_name: str = 'enabled', backward: Callable[..., Any] = lambda x: x) -> Self:
            Binds the enabled state of this element from the target object's target_name property.
        bind_enabled(self, target_object: Any, target_name: str = 'enabled', forward: Callable[..., Any] = lambda x: x,
                      backward: Callable[..., Any] = lambda x: x) -> Self:
            Binds the enabled state of this element to the target object's target_name property in both directions.
        set_enabled(self, value: bool) -> None: Sets the enabled state of the element.
        _handle_enabled_change(self, enabled: bool) -> None: Called when the element is enabled or disabled.
    """

    enabled = BindableProperty(
        on_change=lambda sender, value: cast(Self, sender)._handle_enabled_change(value))  # pylint: disable=protected-access

    def __init__(self, **kwargs: Any) -> None:
        """
        Initializes the DisableableElement instance.

        Args:
            **kwargs: Additional keyword arguments to be passed to the parent class constructor.
        """
        super().__init__(**kwargs)
        self.enabled = True
        self.ignores_events_when_disabled = True
    @property
    def is_ignoring_events(self) -> bool:
        """
        Returns whether the element is currently ignoring events.

        Returns:
            bool: True if the element is ignoring events, False otherwise.
        """
        if super().is_ignoring_events:
            return True
        return not self.enabled and self.ignores_events_when_disabled

    def enable(self) -> None:
        """
        Enables the element.
        """
        self.enabled = True

    def disable(self) -> None:
        """
        Disables the element.
        """
        self.enabled = False

    def bind_enabled_to(self,
                        target_object: Any,
                        target_name: str = 'enabled',
                        forward: Callable[..., Any] = lambda x: x,
                        ) -> Self:
        """
        Binds the enabled state of this element to the target object's target_name property.

        The binding works one way only, from this element to the target.
        The update happens immediately and whenever a value changes.

        Args:
            target_object (Any): The object to bind to.
            target_name (str): The name of the property to bind to.
            forward (Callable[..., Any]): A function to apply to the value before applying it to the target.

        Returns:
            Self: The DisableableElement instance.
        """
        bind_to(self, 'enabled', target_object, target_name, forward)
        return self

    def bind_enabled_from(self,
                          target_object: Any,
                          target_name: str = 'enabled',
                          backward: Callable[..., Any] = lambda x: x,
                          ) -> Self:
        """
        Binds the enabled state of this element from the target object's target_name property.

        The binding works one way only, from the target to this element.
        The update happens immediately and whenever a value changes.

        Args:
            target_object (Any): The object to bind from.
            target_name (str): The name of the property to bind from.
            backward (Callable[..., Any]): A function to apply to the value before applying it to this element.

        Returns:
            Self: The DisableableElement instance.
        """
        bind_from(self, 'enabled', target_object, target_name, backward)
        return self

    def bind_enabled(self,
                     target_object: Any,
                     target_name: str = 'enabled', *,
                     forward: Callable[..., Any] = lambda x: x,
                     backward: Callable[..., Any] = lambda x: x,
                     ) -> Self:
        """
        Binds the enabled state of this element to the target object's target_name property.

        The binding works both ways, from this element to the target and from the target to this element.
        The update happens immediately and whenever a value changes.
        The backward binding takes precedence for the initial synchronization.

        Args:
            target_object (Any): The object to bind to.
            target_name (str): The name of the property to bind to.
            forward (Callable[..., Any]): A function to apply to the value before applying it to the target.
            backward (Callable[..., Any]): A function to apply to the value before applying it to this element.

        Returns:
            Self: The DisableableElement instance.
        """
        bind(self, 'enabled', target_object, target_name, forward=forward, backward=backward)
        return self

    def set_enabled(self, value: bool) -> None:
        """
        Sets the enabled state of the element.

        Args:
            value (bool): The new enabled state.
        """
        self.enabled = value

    def _handle_enabled_change(self, enabled: bool) -> None:
        """
        Called when the element is enabled or disabled.

        Args:
            enabled (bool): The new state.
        """
        self._props['disable'] = not enabled
        self.update()
