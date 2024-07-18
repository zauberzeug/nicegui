from __future__ import annotations

from typing import TYPE_CHECKING, Set, TypeVar

from typing_extensions import Self

from nicegui import background_tasks, events, ui
from nicegui.element import Element

if TYPE_CHECKING:
    from .user import User

T = TypeVar('T', bound=Element)


class UserInteraction:

    def __init__(self, user: User, elements: Set[T]) -> None:
        """Iteraction object of the simulated user.

        This will be returned by the ``find`` method of the ``user`` fixture in pytests.
        It can be used to perform interaction with the found elements.
        """
        self.user = user
        for element in elements:
            assert isinstance(element, ui.element)
        self.elements = elements

    def trigger(self, event: str) -> Self:
        """Trigger the given event on the elements selected by the simulated user.

        Examples: "keydown.enter", "click", ...
        """
        assert self.user.client
        with self.user.client:
            for element in self.elements:
                for listener in element._event_listeners.values():  # pylint: disable=protected-access
                    if listener.type != event:
                        continue
                    events.handle_event(listener.handler,
                                        events.GenericEventArguments(sender=element, client=self.user.client, args={}))
        return self

    def type(self, text: str) -> Self:
        """Type the given text into the selected elements."""
        assert self.user.client
        with self.user.client:
            for element in self.elements:
                assert isinstance(element, ui.input)
                element.value = text
        return self

    def click(self) -> Self:
        """Click the selected elements."""
        assert self.user.client
        with self.user.client:
            for element in self.elements:
                assert isinstance(element, ui.element)
                href = element._props.get('href')  # pylint: disable=protected-access
                if href is not None:
                    background_tasks.create(self.user.open(href))
                    return self
                for listener in element._event_listeners.values():  # pylint: disable=protected-access
                    if listener.element_id != element.id:
                        continue
                    args = None
                    if isinstance(element, ui.checkbox):
                        args = not element.value
                    events.handle_event(listener.handler,
                                        events.GenericEventArguments(sender=element, client=self.user.client, args=args))
        return self
