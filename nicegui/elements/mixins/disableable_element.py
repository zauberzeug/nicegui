from collections.abc import Callable
from typing import Any, cast

from typing_extensions import Self

from ...binding import BindableProperty, bind, bind_from, bind_to
from ...element import Element


class DisableableElement(Element):
    enabled = BindableProperty(
        on_change=lambda sender, value: cast(Self, sender)._handle_enabled_change(value))  # pylint: disable=protected-access

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.enabled = True
        self.ignores_events_when_disabled = True

    @property
    def is_ignoring_events(self) -> bool:
        """Return whether the element is currently ignoring events."""
        if super().is_ignoring_events:
            return True
        return not self.enabled and self.ignores_events_when_disabled

    def enable(self) -> None:
        """Enable the element."""
        self.enabled = True

    def disable(self) -> None:
        """Disable the element."""
        self.enabled = False

    def bind_enabled_to(self,
                        target_object: Any,
                        target_name: str = 'enabled',
                        forward: Callable[[Any], Any] | None = None, *,
                        strict: bool | None = None,
                        ) -> Self:
        """Bind the enabled state of this element to the target object's target_name property.

        The binding works one way only, from this element to the target.
        The update happens immediately and whenever a value changes.

        :param target_object: The object to bind to.
        :param target_name: The name of the property to bind to.
        :param forward: A function to apply to the value before applying it to the target (default: identity).
        :param strict: Whether to check (and raise) if the target object has the specified property (default: None,
            performs a check if the object is not a dictionary, *added in version 3.0.0*).
        """
        bind_to(self, 'enabled', target_object, target_name, forward, self_strict=False, other_strict=strict)
        return self

    def bind_enabled_from(self,
                          target_object: Any,
                          target_name: str = 'enabled',
                          backward: Callable[[Any], Any] | None = None, *,
                          strict: bool | None = None,
                          ) -> Self:
        """Bind the enabled state of this element from the target object's target_name property.

        The binding works one way only, from the target to this element.
        The update happens immediately and whenever a value changes.

        :param target_object: The object to bind from.
        :param target_name: The name of the property to bind from.
        :param backward: A function to apply to the value before applying it to this element (default: identity).
        :param strict: Whether to check (and raise) if the target object has the specified property (default: None,
            performs a check if the object is not a dictionary, *added in version 3.0.0*).
        """
        bind_from(self, 'enabled', target_object, target_name, backward, self_strict=False, other_strict=strict)
        return self

    def bind_enabled(self,
                     target_object: Any,
                     target_name: str = 'enabled', *,
                     forward: Callable[[Any], Any] | None = None,
                     backward: Callable[[Any], Any] | None = None,
                     strict: bool | None = None,
                     ) -> Self:
        """Bind the enabled state of this element to the target object's target_name property.

        The binding works both ways, from this element to the target and from the target to this element.
        The update happens immediately and whenever a value changes.
        The backward binding takes precedence for the initial synchronization.

        :param target_object: The object to bind to.
        :param target_name: The name of the property to bind to.
        :param forward: A function to apply to the value before applying it to the target (default: identity).
        :param backward: A function to apply to the value before applying it to this element (default: identity).
        :param strict: Whether to check (and raise) if the target object has the specified property (default: None,
            performs a check if the object is not a dictionary, *added in version 3.0.0*).
        """
        bind(self, 'enabled', target_object, target_name,
             forward=forward, backward=backward,
             self_strict=False, other_strict=strict)
        return self

    def set_enabled(self, value: bool) -> None:
        """Set the enabled state of the element."""
        self.enabled = value

    def _handle_enabled_change(self, enabled: bool) -> None:
        """Called when the element is enabled or disabled.

        :param enabled: The new state.
        """
        self._props['disable'] = not enabled
