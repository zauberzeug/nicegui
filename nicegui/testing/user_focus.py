from typing import TYPE_CHECKING, List, Self

from nicegui import Client, ElementFilter, background_tasks, context, events, ui

if TYPE_CHECKING:
    from .user import User


class UserFocus:

    def __init__(self, user: 'User', elements: List[ui.element]):
        self.user = user
        for element in elements:
            assert isinstance(element, ui.element)
        self.elements = elements

    def trigger(self, event: str) -> Self:
        """Trigger the given event on the elements focused by the simulated user."""
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
        """Type the given text into the focused elements."""
        assert self.user.client
        with self.user.client:
            for element in self.elements:
                assert isinstance(element, ui.input)
                element.value = text
        return self

    def click(self) -> Self:
        """Click the focused elements."""
        assert self.user.client
        with self.user.client:
            for element in self.elements:
                assert isinstance(element, ui.element)
                href = element._props.get('href')  # pylint: disable=protected-access
                if href is not None:
                    background_tasks.create(self.user.open(href))
                    return
                for listener in element._event_listeners.values():  # pylint: disable=protected-access
                    if listener.element_id != element.id:
                        continue
                    args = None
                    if isinstance(element, ui.checkbox):
                        args = not element.value
                    events.handle_event(listener.handler,
                                        events.GenericEventArguments(sender=element, client=self.user.client, args=args))
