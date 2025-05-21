from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, cast

from typing_extensions import Self

from ...binding import BindableProperty, bind, bind_from, bind_to

if TYPE_CHECKING:
    from ...element import Element


class Visibility:
    visible = BindableProperty(
        on_change=lambda sender, visible: cast(Self, sender)._handle_visibility_change(visible))  # pylint: disable=protected-access

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.visible = True
        self.ignores_events_when_hidden = True

    @property
    def is_ignoring_events(self) -> bool:
        """Return whether the element is currently ignoring events."""
        return not self.visible and self.ignores_events_when_hidden

    def bind_visibility_to(self,
                           target_object: Any,
                           target_name: str = 'visible',
                           forward: Callable[..., Any] = lambda x: x,
                           ) -> Self:
        """Bind the visibility of this element to the target object's target_name property.

        The binding works one way only, from this element to the target.
        The update happens immediately and whenever a value changes.

        :param target_object: The object to bind to.
        :param target_name: The name of the property to bind to.
        :param forward: A function to apply to the value before applying it to the target.
        """
        bind_to(self, 'visible', target_object, target_name, forward)
        return self

    def bind_visibility_from(self,
                             target_object: Any,
                             target_name: str = 'visible',
                             backward: Callable[..., Any] = lambda x: x, *,
                             value: Any = None) -> Self:
        """Bind the visibility of this element from the target object's target_name property.

        The binding works one way only, from the target to this element.
        The update happens immediately and whenever a value changes.

        :param target_object: The object to bind from.
        :param target_name: The name of the property to bind from.
        :param backward: A function to apply to the value before applying it to this element.
        :param value: If specified, the element will be visible only when the target value is equal to this value.
        """
        if value is not None:
            def backward(x):  # pylint: disable=function-redefined
                return x == value
        bind_from(self, 'visible', target_object, target_name, backward)
        return self

    def bind_visibility(self,
                        target_object: Any,
                        target_name: str = 'visible', *,
                        forward: Callable[..., Any] = lambda x: x,
                        backward: Callable[..., Any] = lambda x: x,
                        value: Any = None,
                        ) -> Self:
        """Bind the visibility of this element to the target object's target_name property.

        The binding works both ways, from this element to the target and from the target to this element.
        The update happens immediately and whenever a value changes.
        The backward binding takes precedence for the initial synchronization.

        :param target_object: The object to bind to.
        :param target_name: The name of the property to bind to.
        :param forward: A function to apply to the value before applying it to the target.
        :param backward: A function to apply to the value before applying it to this element.
        :param value: If specified, the element will be visible only when the target value is equal to this value.
        """
        if value is not None:
            def backward(x):  # pylint: disable=function-redefined
                return x == value
        bind(self, 'visible', target_object, target_name, forward=forward, backward=backward)
        return self

    def set_visibility(self, visible: bool) -> None:
        """Set the visibility of this element.

        :param visible: Whether the element should be visible.
        """
        self.visible = visible

    def _handle_visibility_change(self, visible: str) -> None:
        """Called when the visibility of this element changes.

        :param visible: Whether the element should be visible.
        """
        element: Element = cast('Element', self)
        classes = element.classes  # pylint: disable=no-member
        if visible and 'hidden' in classes:
            classes.remove('hidden')
            element.update()  # pylint: disable=no-member
        if not visible and 'hidden' not in classes:
            classes.append('hidden')
            element.update()  # pylint: disable=no-member
