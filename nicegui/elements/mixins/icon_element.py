from collections.abc import Callable
from typing import Any, cast

from typing_extensions import Self

from ...binding import BindableProperty, bind, bind_from, bind_to
from ...element import Element


class IconElement(Element):
    icon = BindableProperty(
        on_change=lambda sender, icon: cast(Self, sender)._handle_icon_change(icon))  # pylint: disable=protected-access

    def __init__(self, *, icon: str | None = None, **kwargs: Any) -> None:  # pylint: disable=redefined-builtin
        super().__init__(**kwargs)
        self.icon = icon
        self._props.set_optional('icon', icon)

    def bind_icon_to(self,
                     target_object: Any,
                     target_name: str = 'icon',
                     forward: Callable[[Any], Any] | None = None, *,
                     strict: bool | None = None,
                     ) -> Self:
        """Bind the icon of this element to the target object's target_name property.

        The binding works one way only, from this element to the target.
        The update happens immediately and whenever a value changes.

        :param target_object: The object to bind to.
        :param target_name: The name of the property to bind to.
        :param forward: A function to apply to the value before applying it to the target (default: identity).
        :param strict: Whether to check (and raise) if the target object has the specified property (default: None,
            performs a check if the object is not a dictionary, *added in version 3.0.0*).
        """
        bind_to(self, 'icon', target_object, target_name, forward, self_strict=False, other_strict=strict)
        return self

    def bind_icon_from(self,
                       target_object: Any,
                       target_name: str = 'icon',
                       backward: Callable[[Any], Any] | None = None, *,
                       strict: bool | None = None,
                       ) -> Self:
        """Bind the icon of this element from the target object's target_name property.

        The binding works one way only, from the target to this element.
        The update happens immediately and whenever a value changes.

        :param target_object: The object to bind from.
        :param target_name: The name of the property to bind from.
        :param backward: A function to apply to the value before applying it to this element (default: identity).
        :param strict: Whether to check (and raise) if the target object has the specified property (default: None,
            performs a check if the object is not a dictionary, *added in version 3.0.0*).
        """
        bind_from(self, 'icon', target_object, target_name, backward, self_strict=False, other_strict=strict)
        return self

    def bind_icon(self,
                  target_object: Any,
                  target_name: str = 'icon', *,
                  forward: Callable[[Any], Any] | None = None,
                  backward: Callable[[Any], Any] | None = None,
                  strict: bool | None = None,
                  ) -> Self:
        """Bind the icon of this element to the target object's target_name property.

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
        bind(self, 'icon', target_object, target_name,
             forward=forward, backward=backward,
             self_strict=False, other_strict=strict)
        return self

    def set_icon(self, icon: str | None) -> None:
        """Set the icon of this element.

        :param icon: The new icon.
        """
        self.icon = icon

    def _handle_icon_change(self, icon: str | None) -> None:
        """Called when the icon of this element changes.

        :param icon: The new icon.
        """
        self._props.set_optional('icon', icon)
