from __future__ import annotations

from typing import TYPE_CHECKING, Generic, List, Set, Type, TypeVar, Union

from typing_extensions import Self

from nicegui import background_tasks, events, ui
from nicegui.element import Element
from nicegui.elements.mixins.disableable_element import DisableableElement
from nicegui.elements.mixins.value_element import ValueElement

if TYPE_CHECKING:
    from .user import User

T = TypeVar('T', bound=Element)


class UserInteraction(Generic[T]):

    def __init__(self, user: User, elements: Set[T], target: Union[str, Type[T], None]) -> None:
        """Interaction object of the simulated user.

        This will be returned by the ``find`` method of the ``user`` fixture in pytests.
        It can be used to perform interaction with the found elements.
        """
        self.user = user
        for element in elements:
            assert isinstance(element, ui.element)
        self.elements = elements
        self.target = target

    def trigger(self, event: str) -> Self:
        """Trigger the given event on the elements selected by the simulated user.

        Examples: "keydown.enter", "click", ...
        """
        assert self.user.client
        with self.user.client:
            for element in self.elements:
                if isinstance(element, ui.input) and event == 'keydown.tab':
                    autocomplete: List[str] = element.props['_autocomplete']
                    for option in autocomplete:
                        if option.startswith(element.value):
                            element.value = option
                            break

                for listener in element._event_listeners.values():  # pylint: disable=protected-access
                    if listener.type != event:
                        continue
                    event_arguments = events.GenericEventArguments(sender=element, client=self.user.client, args={})
                    events.handle_event(listener.handler, event_arguments)
        return self

    def type(self, text: str) -> Self:
        """Type the given text into the selected elements.

        Note: All elements must have a ``value`` attribute.
        """
        assert self.user.client
        with self.user.client:
            for element in self.elements:
                if isinstance(element, DisableableElement) and not element.enabled:
                    continue
                assert isinstance(element, (ui.input, ui.editor, ui.codemirror))
                element.value = (element.value or '') + text
        return self

    def click(self) -> Self:
        """Click the selected elements."""
        assert self.user.client
        with self.user.client:
            for element in self.elements:
                if isinstance(element, ui.link):
                    href = element.props.get('href', '#')
                    background_tasks.create(self.user.open(href))
                    return self
                if isinstance(element, ui.select):
                    if element.is_showing_popup:
                        assert isinstance(self.target, str), 'Target must be string when clicking on ui.select options'
                        element.set_value(self.target)
                    element._is_showing_popup = not element.is_showing_popup  # pylint: disable=protected-access
                    return self
                for listener in element._event_listeners.values():  # pylint: disable=protected-access
                    if listener.element_id != element.id:
                        continue
                    args = None
                    if isinstance(element, (ui.checkbox, ui.switch)):
                        args = not element.value
                    event_arguments = events.GenericEventArguments(sender=element, client=self.user.client, args=args)
                    events.handle_event(listener.handler, event_arguments)
        return self

    def clear(self) -> Self:
        """Clear the selected elements.

        Note: All elements must have a ``value`` attribute).
        """
        assert self.user.client
        with self.user.client:
            for element in self.elements:
                assert isinstance(element, ValueElement)
                element.value = None
        return self
