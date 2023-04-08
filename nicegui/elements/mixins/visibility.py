from typing import TYPE_CHECKING, Any, Callable

from typing_extensions import Self

from ...binding import BindableProperty, bind, bind_from, bind_to

if TYPE_CHECKING:
    from ...element import Element


class Visibility:
    visible = BindableProperty(on_change=lambda sender, visible: sender.on_visibility_change(visible))

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.visible = True

    def bind_visibility_to(self,
                           target_object: Any,
                           target_name: str = 'visible',
                           forward: Callable = lambda x: x) -> Self:
        """Bind the visibility of this element to the target object's target_name property.

        The binding works one way only, from this element to the target.

        :param target_object: The object to bind to.
        :param target_name: The name of the property to bind to.
        :param forward: A function to apply to the value before applying it to the target.
        """
        bind_to(self, 'visible', target_object, target_name, forward)
        return self

    def bind_visibility_from(self,
                             target_object: Any,
                             target_name: str = 'visible',
                             backward: Callable = lambda x: x, *,
                             value: Any = None) -> Self:
        """Bind the visibility of this element from the target object's target_name property.

        The binding works one way only, from the target to this element.

        :param target_object: The object to bind from.
        :param target_name: The name of the property to bind from.
        :param backward: A function to apply to the value before applying it to this element.
        :param value: If specified, the element will be visible only when the target value is equal to this value.
        """
        if value is not None:
            def backward(x): return x == value
        bind_from(self, 'visible', target_object, target_name, backward)
        return self

    def bind_visibility(self,
                        target_object: Any,
                        target_name: str = 'visible', *,
                        forward: Callable = lambda x: x,
                        backward: Callable = lambda x: x,
                        value: Any = None) -> Self:
        """Bind the visibility of this element to the target object's target_name property.

        The binding works both ways, from this element to the target and from the target to this element.

        :param target_object: The object to bind to.
        :param target_name: The name of the property to bind to.
        :param forward: A function to apply to the value before applying it to the target.
        :param backward: A function to apply to the value before applying it to this element.
        :param value: If specified, the element will be visible only when the target value is equal to this value.
        """
        if value is not None:
            def backward(x): return x == value
        bind(self, 'visible', target_object, target_name, forward=forward, backward=backward)
        return self

    def set_visibility(self, visible: str) -> None:
        """Set the visibility of this element.

        :param visible: Whether the element should be visible.
        """
        self.visible = visible

    def on_visibility_change(self: 'Element', visible: str) -> None:
        """Called when the visibility of this element changes.

        :param visible: Whether the element should be visible.
        """
        if visible and 'hidden' in self._classes:
            self._classes.remove('hidden')
            self.update()
        if not visible and 'hidden' not in self._classes:
            self._classes.append('hidden')
            self.update()
