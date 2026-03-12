from collections.abc import Callable
from typing import Any, cast

from typing_extensions import Self

from ...binding import BindableProperty, bind, bind_from, bind_to
from ...element import Element


class FilterElement(Element):
    FILTER_PROP = 'filter'
    filter = BindableProperty(
        on_change=lambda sender, filter: cast(Self, sender)._handle_filter_change(filter))  # pylint: disable=protected-access

    def __init__(self, *, filter: str | None = None, **kwargs: Any) -> None:  # pylint: disable=redefined-builtin
        super().__init__(**kwargs)
        self.filter = filter
        self._props[self.FILTER_PROP] = filter

    def bind_filter_to(self,
                       target_object: Any,
                       target_name: str = 'filter',
                       forward: Callable[[Any], Any] | None = None, *,
                       strict: bool | None = None,
                       ) -> Self:
        """Bind the filter of this element to the target object's target_name property.

        The binding works one way only, from this element to the target.
        The update happens immediately and whenever a value changes.

        :param target_object: The object to bind to.
        :param target_name: The name of the property to bind to.
        :param forward: A function to apply to the value before applying it to the target (default: identity).
        :param strict: Whether to check (and raise) if the target object has the specified property (default: None,
            performs a check if the object is not a dictionary, *added in version 3.0.0*).
        """
        bind_to(self, 'filter', target_object, target_name, forward, self_strict=False, other_strict=strict)
        return self

    def bind_filter_from(self,
                         target_object: Any,
                         target_name: str = 'filter',
                         backward: Callable[[Any], Any] | None = None, *,
                         strict: bool | None = None,
                         ) -> Self:
        """Bind the filter of this element from the target object's target_name property.

        The binding works one way only, from the target to this element.
        The update happens immediately and whenever a value changes.

        :param target_object: The object to bind from.
        :param target_name: The name of the property to bind from.
        :param backward: A function to apply to the value before applying it to this element (default: identity).
        :param strict: Whether to check (and raise) if the target object has the specified property (default: None,
            performs a check if the object is not a dictionary, *added in version 3.0.0*).
        """
        bind_from(self, 'filter', target_object, target_name, backward, self_strict=False, other_strict=strict)
        return self

    def bind_filter(self,
                    target_object: Any,
                    target_name: str = 'filter', *,
                    forward: Callable[[Any], Any] | None = None,
                    backward: Callable[[Any], Any] | None = None,
                    strict: bool | None = None,
                    ) -> Self:
        """Bind the filter of this element to the target object's target_name property.

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
        bind(self, 'filter', target_object, target_name,
             forward=forward, backward=backward,
             self_strict=False, other_strict=strict)
        return self

    def set_filter(self, filter_: str) -> None:
        """Set the filter of this element.

        :param filter: The new filter.
        """
        self.filter = filter_

    def _handle_filter_change(self, filter_: str) -> None:
        """Called when the filter of this element changes.

        :param filter: The new filter.
        """
        self._props[self.FILTER_PROP] = filter_
