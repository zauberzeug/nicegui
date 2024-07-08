from typing import List

from nicegui import Client, ElementFilter, background_tasks, context, events, ui


class UserFocus:

    def __init__(self, client: Client, elements: List[ui.element]):
        self.client = client
        for element in elements:
            assert isinstance(element, ui.element)
        self.elements = elements

    def trigger(self, event: str) -> None:
        """Trigger the given event on the elements focused by the simulated user."""
        with self.client:
            for element in self.elements:
                for listener in element._event_listeners.values():  # pylint: disable=protected-access
                    if listener.type != event:
                        continue
                    events.handle_event(listener.handler,
                                        events.GenericEventArguments(sender=element, client=self.client, args={}))
