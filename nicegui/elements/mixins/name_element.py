from typing import Any, Callable, cast

from typing_extensions import Self

from ...binding import BindableProperty, bind, bind_from, bind_to
from ...element import Element


class NameElement(Element):
    """
    A mixin class for elements that have a name property.

    This mixin provides functionality to bind the name property of an element to another object's property,
    allowing for one-way or two-way data binding. It also provides a method to set the name directly.

    Usage:
    1. Inherit from NameElement along with other base classes for your element.
    2. Use the bind_name_to() method to bind the name property to a target object's property.
    3. Use the bind_name_from() method to bind the name property from a target object's property.
    4. Use the bind_name() method to bind the name property both ways.
    5. Use the set_name() method to set the name directly.

    Example:
    ```
    class MyElement(NameElement, OtherMixin):
        def __init__(self, name, **kwargs):
            super().__init__(**kwargs)
            self.name = name

    element = MyElement(name="My Element")
    element.bind_name_to(target_object, target_name="element_name")
    element.set_name("New Name")
    ```

    Attributes:
    - name: The name of the element.

    Methods:
    - bind_name_to(): Bind the name property to a target object's property.
    - bind_name_from(): Bind the name property from a target object's property.
    - bind_name(): Bind the name property both ways.
    - set_name(): Set the name directly.
    """

    name = BindableProperty(
        on_change=lambda sender, name: cast(Self, sender)._handle_name_change(name))  # pylint: disable=protected-access

    def __init__(self, *, name: str, **kwargs: Any) -> None:
        """
        NameElement

        Args:
        - name: The name of the element.
        - kwargs: Additional keyword arguments to pass to the base class.
        """
        super().__init__(**kwargs)
        self.name = name
        self._props['name'] = name

    def bind_name_to(self,
                     target_object: Any,
                     target_name: str = 'name',
                     forward: Callable[..., Any] = lambda x: x,
                     ) -> Self:
        """
        Bind the name of this element to the target object's target_name property.

        The binding works one way only, from this element to the target.
        The update happens immediately and whenever a value changes.

        Args:
        - target_object: The object to bind to.
        - target_name: The name of the property to bind to.
        - forward: A function to apply to the value before applying it to the target.

        Returns:
        - self: The NameElement instance.
        """
        bind_to(self, 'name', target_object, target_name, forward)
        return self

    def bind_name_from(self,
                       target_object: Any,
                       target_name: str = 'name',
                       backward: Callable[..., Any] = lambda x: x,
                       ) -> Self:
        """
        Bind the name of this element from the target object's target_name property.

        The binding works one way only, from the target to this element.
        The update happens immediately and whenever a value changes.

        Args:
        - target_object: The object to bind from.
        - target_name: The name of the property to bind from.
        - backward: A function to apply to the value before applying it to this element.

        Returns:
        - self: The NameElement instance.
        """
        bind_from(self, 'name', target_object, target_name, backward)
        return self

    def bind_name(self,
                  target_object: Any,
                  target_name: str = 'name', *,
                  forward: Callable[..., Any] = lambda x: x,
                  backward: Callable[..., Any] = lambda x: x,
                  ) -> Self:
        """
        Bind the name of this element to the target object's target_name property.

        The binding works both ways, from this element to the target and from the target to this element.
        The update happens immediately and whenever a value changes.
        The backward binding takes precedence for the initial synchronization.

        Args:
        - target_object: The object to bind to.
        - target_name: The name of the property to bind to.
        - forward: A function to apply to the value before applying it to the target.
        - backward: A function to apply to the value before applying it to this element.

        Returns:
        - self: The NameElement instance.
        """
        bind(self, 'name', target_object, target_name, forward=forward, backward=backward)
        return self

    def set_name(self, name: str) -> None:
        """
        Set the name of this element.

        This method allows you to change the name of the element to a new value.

        Args:
            name (str): The new name for the element.

        Returns:
            None

        Example:
            >>> element = NameElement()
            >>> element.set_name("New Name")
            >>> element.name
            'New Name'

        Note:
            - The name should be a string.
            - After calling this method, the `name` attribute of the element will be updated.
        """
        self.name = name

    def _handle_name_change(self, name: str) -> None:
        """
        Called when the name of this element changes.

        Args:
        - name: The new name.
        """
        self._props['name'] = name
        self.update()
