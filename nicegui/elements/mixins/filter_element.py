from typing import Any, Callable, Optional, cast

from typing_extensions import Self

from ...binding import BindableProperty, bind, bind_from, bind_to
from ...element import Element


class FilterElement(Element):
    """
    Represents a filter element that can be bound to another object's property.

    This element allows you to bind its `filter` property to a target object's property,
    enabling two-way synchronization of the filter value.

    Usage:
    1. Create an instance of `FilterElement`.
    2. Optionally, set the initial filter value using the `filter` parameter in the constructor.
    3. Bind the filter to a target object's property using the `bind_filter_to` or `bind_filter_from` methods.
    4. Optionally, use the `bind_filter` method to establish a two-way binding.
    5. Update the filter value using the `set_filter` method.
    6. Implement the `_handle_filter_change` method to handle filter changes.

    Example:
    ```
    filter_element = FilterElement(filter='example')
    filter_element.bind_filter_to(target_object, target_name='filter')
    filter_element.set_filter('new_filter')
    ```

    Args:
        filter (str, optional): The initial filter value. Defaults to None.
        **kwargs: Additional keyword arguments to be passed to the base class constructor.
    """

    FILTER_PROP = 'filter'
    filter = BindableProperty(
        on_change=lambda sender, filter: cast(Self, sender)._handle_filter_change(filter))  # pylint: disable=protected-access

    def __init__(self, *, filter: Optional[str] = None, **kwargs: Any) -> None:  # pylint: disable=redefined-builtin
        """
        Initializes a new instance of the FilterElement class.

        Args:
            filter (str, optional): The initial filter value. Defaults to None.
            **kwargs: Additional keyword arguments to be passed to the base class constructor.
        """
        super().__init__(**kwargs)
        self.filter = filter
        self._props[self.FILTER_PROP] = filter

    def bind_filter_to(self,
                       target_object: Any,
                       target_name: str = 'filter',
                       forward: Callable[..., Any] = lambda x: x,
                       ) -> Self:
        """
        Binds the filter of this element to the target object's property.

        The binding works one way only, from this element to the target.
        The update happens immediately and whenever a value changes.

        Args:
            target_object (Any): The object to bind to.
            target_name (str, optional): The name of the property to bind to. Defaults to 'filter'.
            forward (Callable[..., Any], optional): A function to apply to the value before applying it to the target. Defaults to lambda x: x.

        Returns:
            Self: The current instance of the FilterElement.
        """
        bind_to(self, 'filter', target_object, target_name, forward)
        return self

    def bind_filter_from(self,
                         target_object: Any,
                         target_name: str = 'filter',
                         backward: Callable[..., Any] = lambda x: x,
                         ) -> Self:
        """
        Binds the filter of this element from the target object's property.

        The binding works one way only, from the target to this element.
        The update happens immediately and whenever a value changes.

        Args:
            target_object (Any): The object to bind from.
            target_name (str, optional): The name of the property to bind from. Defaults to 'filter'.
            backward (Callable[..., Any], optional): A function to apply to the value before applying it to this element. Defaults to lambda x: x.

        Returns:
            Self: The current instance of the FilterElement.
        """
        bind_from(self, 'filter', target_object, target_name, backward)
        return self

    def bind_filter(self,
                    target_object: Any,
                    target_name: str = 'filter', *,
                    forward: Callable[..., Any] = lambda x: x,
                    backward: Callable[..., Any] = lambda x: x,
                    ) -> Self:
        """
        Binds the filter of this element to the target object's property.

        The binding works both ways, from this element to the target and from the target to this element.
        The update happens immediately and whenever a value changes.
        The backward binding takes precedence for the initial synchronization.

        Args:
            target_object (Any): The object to bind to.
            target_name (str, optional): The name of the property to bind to. Defaults to 'filter'.
            forward (Callable[..., Any], optional): A function to apply to the value before applying it to the target. Defaults to lambda x: x.
            backward (Callable[..., Any], optional): A function to apply to the value before applying it to this element. Defaults to lambda x: x.

        Returns:
            Self: The current instance of the FilterElement.
        """
        bind(self, 'filter', target_object, target_name, forward=forward, backward=backward)
        return self

    def set_filter(self, filter_: str) -> None:
        """
        Sets the filter of this element.

        Args:
            filter_ (str): The new filter value.
        """
        self.filter = filter_

    def _handle_filter_change(self, filter_: str) -> None:
        """
        Called when the filter of this element changes.

        Args:
            filter_ (str): The new filter value.
        """
        self._props[self.FILTER_PROP] = filter_
        self.update()
