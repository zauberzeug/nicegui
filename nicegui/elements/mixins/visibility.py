from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, cast

from typing_extensions import Self

from ...binding import BindableProperty, bind, bind_from, bind_to

if TYPE_CHECKING:
    from ...element import Element


class Visibility:
    """
    Mixin class for managing the visibility of an element.

    This class provides methods and properties for controlling the visibility of an element.
    It allows binding the visibility to another object's property, both one-way and two-way.
    The visibility can also be set directly using the `set_visibility` method.

    Usage:
    1. Creating an element with visibility mixin:
        ```
        class MyElement(Visibility, ...):
            ...
        ```

    2. Setting the initial visibility:
        ```
        element = MyElement()
        element.set_visibility(True)
        ```

    3. Binding the visibility to another object's property:
        ```
        element.bind_visibility_to(target_object, target_name)
        ```

    4. Binding the visibility from another object's property:
        ```
        element.bind_visibility_from(target_object, target_name)
        ```

    5. Binding the visibility both ways:
        ```
        element.bind_visibility(target_object, target_name)
        ```

    Attributes:
    - visible: A boolean property representing the visibility of the element.
    - ignores_events_when_hidden: A boolean property indicating whether the element should ignore events when hidden.

    Methods:
    - bind_visibility_to: Bind the visibility of this element to the target object's property.
    - bind_visibility_from: Bind the visibility of this element from the target object's property.
    - bind_visibility: Bind the visibility of this element both ways with the target object's property.
    - set_visibility: Set the visibility of this element directly.
    """

    visible = BindableProperty(
        on_change=lambda sender, visible: cast(Self, sender)._handle_visibility_change(visible))  # pylint: disable=protected-access

    def __init__(self, **kwargs: Any) -> None:
        """
        Initialize the visibility mixin.

        This mixin provides functionality for managing the visibility of an element.

        Args:
            **kwargs: Additional keyword arguments to be passed to the parent class.

        Attributes:
            visible (bool): Indicates whether the element is visible or not. By default, it is set to True.
            ignores_events_when_hidden (bool): Indicates whether the element should ignore events when it is hidden. By default, it is set to True.

        Example:
            >>> element = VisibilityMixin()
            >>> element.visible
            True
            >>> element.ignores_events_when_hidden
            True
        """
        super().__init__(**kwargs)
        self.visible = True
        self.ignores_events_when_hidden = True

    @property
    def is_ignoring_events(self) -> bool:
        """
        Return whether the element is currently ignoring events.

        This method checks if the element is currently ignoring events based on its visibility and
        the value of the `ignores_events_when_hidden` attribute.

        Returns:
            bool: True if the element is ignoring events, False otherwise.

        Example:
            >>> element = MyElement()
            >>> element.visible = False
            >>> element.ignores_events_when_hidden = True
            >>> element.is_ignoring_events()
            True

        Note:
            The `visible` attribute determines whether the element is visible or hidden.
            The `ignores_events_when_hidden` attribute determines whether the element should ignore events when hidden.
        """
        return not self.visible and self.ignores_events_when_hidden

    def bind_visibility_to(self,
                               target_object: Any,
                               target_name: str = 'visible',
                               forward: Callable[..., Any] = lambda x: x,
                               ) -> Self:
            """
            Bind the visibility of this element to the target object's property.

            The binding works one way only, from this element to the target.
            The update happens immediately and whenever a value changes.

            Args:
            - target_object (Any): The object to bind to.
            - target_name (str): The name of the property to bind to.
            - forward (Callable[..., Any]): A function to apply to the value before applying it to the target.

            Returns:
            - Self: The instance of the element.

            Example:
            ```python
            element.bind_visibility_to(target_object, target_name)
            ```

            Note:
            - The `target_object` must have a property with the name specified in `target_name`.
            - The `forward` function can be used to transform the value before applying it to the target property.

            Raises:
            - TypeError: If `target_object` is not of type `Any`.
            - ValueError: If `target_name` is not a string.
            """
            bind_to(self, 'visible', target_object, target_name, forward)
            return self

    def bind_visibility_from(self,
                                                     target_object: Any,
                                                     target_name: str = 'visible',
                                                     backward: Callable[..., Any] = lambda x: x, *,
                                                     value: Any = None) -> Self:
            """
            Bind the visibility of this element from the target object's property.

            The binding works one way only, from the target to this element.
            The update happens immediately and whenever a value changes.

            Args:
            - target_object (Any): The object to bind from.
            - target_name (str, optional): The name of the property to bind from. Defaults to 'visible'.
            - backward (Callable[..., Any], optional): A function to apply to the value before applying it to this element.
                Defaults to lambda x: x.
            - value (Any, optional): If specified, the element will be visible only when the target value is equal to this value.
                Defaults to None.

            Returns:
            - Self: The instance of the element.

            Example:
            ```python
            element.bind_visibility_from(target_object, target_name)
            ```

            Notes:
            - The binding is one-way, meaning changes in the target object's property will update the visibility of this element,
                but changes in the visibility of this element will not affect the target object's property.
            - The `backward` function is applied to the value before it is applied to this element. It can be used to transform
                the value to a different format if needed.
            - If the `value` parameter is specified, the element will only be visible when the target value is equal to the specified value.
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
        """
        Bind the visibility of this element to the target object's property.

        The binding works both ways, from this element to the target and from the target to this element.
        The update happens immediately and whenever a value changes.
        The backward binding takes precedence for the initial synchronization.

        Args:
        - target_object (Any): The object to bind to.
        - target_name (str): The name of the property to bind to.
        - forward (Callable[..., Any]): A function to apply to the value before applying it to the target.
        - backward (Callable[..., Any]): A function to apply to the value before applying it to this element.
        - value (Any): If specified, the element will be visible only when the target value is equal to this value.

        Returns:
        - Self: The instance of the element.

        Example:
        ```python
        element.bind_visibility(target_object, target_name)
        ```

        **Notes**:
        - The `bind_visibility` method allows you to bind the visibility of an element to a property of another object.
        - The binding works both ways, meaning that changes in the element's visibility will update the target property, and changes in the target property will update the element's visibility.
        - The `forward` and `backward` functions can be used to transform the values before applying them to the target or the element, respectively.
        - If the `value` parameter is specified, the element will only be visible when the target property's value is equal to the specified value.
        - The initial synchronization between the element and the target property is performed using the `backward` function.
        """
        if value is not None:
            def backward(x):  # pylint: disable=function-redefined
                return x == value
        bind(self, 'visible', target_object, target_name, forward=forward, backward=backward)
        return self

    def set_visibility(self, visible: bool) -> None:
        """
        Set the visibility of this element.

        This method allows you to control the visibility of the element. When an element is
        visible, it will be rendered and displayed on the user interface. When it is not
        visible, it will be hidden from view.

        Args:
            visible (bool): Whether the element should be visible. Set it to True to make
                the element visible, and False to hide it.

        Example:
            To make an element visible, use the following code:

            ```python
            element.set_visibility(True)
            ```

            To hide an element, use the following code:

            ```python
            element.set_visibility(False)
            ```

        Note:
            - By default, elements are visible when they are created.
            - Changing the visibility of an element will trigger a re-rendering of the user
              interface to reflect the new visibility state.
        """
        self.visible = visible

    def _handle_visibility_change(self, visible: str) -> None:
        """
        Called when the visibility of this element changes.

        Args:
            visible (str): A string indicating whether the element should be visible or hidden. 
                Valid values are 'visible' and 'hidden'.

        Returns:
            None

        Raises:
            None

        Notes:
            This method is responsible for handling the visibility change of an element. 
            It updates the element's classes based on the visibility value and triggers an update.

            If the element is set to be visible and the 'hidden' class is present in its classes, 
            the 'hidden' class will be removed and the element will be updated.

            If the element is set to be hidden and the 'hidden' class is not present in its classes, 
            the 'hidden' class will be added and the element will be updated.

        Example:
            # Create an element
            element = Element()

            # Set the visibility to 'visible'
            element._handle_visibility_change('visible')

            # Set the visibility to 'hidden'
            element._handle_visibility_change('hidden')
        """
        element: Element = cast('Element', self)
        classes = element._classes  # pylint: disable=protected-access, no-member
        if visible and 'hidden' in classes:
            classes.remove('hidden')
            element.update()  # pylint: disable=no-member
        if not visible and 'hidden' not in classes:
            classes.append('hidden')
            element.update()  # pylint: disable=no-member
