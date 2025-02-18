from typing import Any, Callable, Optional, cast

from typing_extensions import Self

from ...binding import BindableProperty, bind, bind_from, bind_to
from ...element import Element


class IconElement(Element):
    icon = BindableProperty(
        on_change=lambda sender, icon: cast(Self, sender)._handle_icon_change(icon))  # pylint: disable=protected-access

    def __init__(self, *, icon: Optional[str] = None, **kwargs: Any) -> None:  # pylint: disable=redefined-builtin
        super().__init__(**kwargs)
        self.icon = icon
        if icon is not None:
            self._props['icon'] = icon

    def bind_icon_to(self,
                     target_object: Any,
                     target_name: str = 'icon',
                     forward: Callable[..., Any] = lambda x: x,
                     ) -> Self:
        """Bind the icon of this element to the target object's target_name property.

        The binding works one way only, from this element to the target.
        The update happens immediately and whenever a value changes.

        :param target_object: The object to bind to.
        :param target_name: The name of the property to bind to.
        :param forward: A function to apply to the value before applying it to the target.
        """
        bind_to(self, 'icon', target_object, target_name, forward)
        return self

    def bind_icon_from(self,
                       target_object: Any,
                       target_name: str = 'icon',
                       backward: Callable[..., Any] = lambda x: x,
                       ) -> Self:
        """Bind the icon of this element from the target object's target_name property.

        The binding works one way only, from the target to this element.
        The update happens immediately and whenever a value changes.

        :param target_object: The object to bind from.
        :param target_name: The name of the property to bind from.
        :param backward: A function to apply to the value before applying it to this element.
        """
        bind_from(self, 'icon', target_object, target_name, backward)
        return self

    def bind_icon(self,
                  target_object: Any,
                  target_name: str = 'icon', *,
                  forward: Callable[..., Any] = lambda x: x,
                  backward: Callable[..., Any] = lambda x: x,
                  ) -> Self:
        """Bind the icon of this element to the target object's target_name property.

        The binding works both ways, from this element to the target and from the target to this element.
        The update happens immediately and whenever a value changes.
        The backward binding takes precedence for the initial synchronization.

        :param target_object: The object to bind to.
        :param target_name: The name of the property to bind to.
        :param forward: A function to apply to the value before applying it to the target.
        :param backward: A function to apply to the value before applying it to this element.
        """
        bind(self, 'icon', target_object, target_name, forward=forward, backward=backward)
        return self

    def set_icon(self, icon: Optional[str]) -> None:
        """Set the icon of this element.

        :param icon: The new icon.
        """
        self.icon = icon

    def _handle_icon_change(self, icon: Optional[str]) -> None:
        """Called when the icon of this element changes.

        :param icon: The new icon.
        """
        if icon is not None:
            self._props['icon'] = icon
        else:
            self._props.pop('icon', None)
        self.update()
