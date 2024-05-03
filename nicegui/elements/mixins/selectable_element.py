from typing import Any, Callable, List, Optional, cast

from typing_extensions import Self

from ...binding import BindableProperty, bind, bind_from, bind_to
from ...element import Element
from ...events import ValueChangeEventArguments, handle_event


class SelectableElement(Element):
    selected = BindableProperty(
        on_change=lambda sender, selected: cast(Self, sender)._handle_selection_change(selected))  # pylint: disable=protected-access

    def __init__(self, *,
                 selectable: bool,
                 selected: bool,
                 on_selection_change: Optional[Callable[..., Any]],
                 **kwargs: Any) -> None:
        super().__init__(**kwargs)
        if not selectable:
            return

        self._props['selectable'] = selectable

        self.selected = selected
        self._props['selected'] = selected
        self.set_selected(selected)
        self.on('update:selected', lambda e: self.set_selected(e.args))

        self._selection_change_handlers: List[Callable[..., Any]] = []
        if on_selection_change:
            self.on_selection_change(on_selection_change)

    def on_selection_change(self, callback: Callable[..., Any]) -> Self:
        """Add a callback to be invoked when the selection state changes."""
        self._selection_change_handlers.append(callback)
        return self

    def bind_selected_to(self,
                         target_object: Any,
                         target_name: str = 'selected',
                         forward: Callable[..., Any] = lambda x: x,
                         ) -> Self:
        """Bind the selection state of this element to the target object's target_name property.

        The binding works one way only, from this element to the target.
        The update happens immediately and whenever a value changes.

        :param target_object: The object to bind to.
        :param target_name: The name of the property to bind to.
        :param forward: A function to apply to the value before applying it to the target.
        """
        bind_to(self, 'selected', target_object, target_name, forward)
        return self

    def bind_selected_from(self,
                           target_object: Any,
                           target_name: str = 'selected',
                           backward: Callable[..., Any] = lambda x: x,
                           ) -> Self:
        """Bind the selection state of this element from the target object's target_name property.

        The binding works one way only, from the target to this element.
        The update happens immediately and whenever a value changes.

        :param target_object: The object to bind from.
        :param target_name: The name of the property to bind from.
        :param backward: A function to apply to the value before applying it to this element.
        """
        bind_from(self, 'selected', target_object, target_name, backward)
        return self

    def bind_selected(self,
                      target_object: Any,
                      target_name: str = 'selected', *,
                      forward: Callable[..., Any] = lambda x: x,
                      backward: Callable[..., Any] = lambda x: x,
                      ) -> Self:
        """Bind the selection state of this element to the target object's target_name property.

        The binding works both ways, from this element to the target and from the target to this element.
        The update happens immediately and whenever a value changes.
        The backward binding takes precedence for the initial synchronization.

        :param target_object: The object to bind to.
        :param target_name: The name of the property to bind to.
        :param forward: A function to apply to the value before applying it to the target.
        :param backward: A function to apply to the value before applying it to this element.
        """
        bind(self, 'selected', target_object, target_name, forward=forward, backward=backward)
        return self

    def set_selected(self, selected: bool) -> None:
        """Set the selection state of this element.

        :param selected: The new selection state.
        """
        self.selected = selected

    def _handle_selection_change(self, selected: bool) -> None:
        """Called when the selection state of this element changes.

        :param selected: The new selection state.
        """
        self._props['selected'] = selected
        self.update()
        args = ValueChangeEventArguments(sender=self, client=self.client, value=self._props['selected'])
        for handler in self._selection_change_handlers:
            handle_event(handler, args)
