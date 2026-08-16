from typing import Any

from typing_extensions import Self

from ...events import GenericEventArguments, Handler, ValueChangeEventArguments, ValueT, handle_event
from .value_element import ValueElement


class ReleasableElement(ValueElement[ValueT]):

    def __init__(self, *,
                 on_release: Handler[ValueChangeEventArguments[ValueT]] | None = None,
                 **kwargs: Any,
                 ) -> None:
        super().__init__(**kwargs)
        self._release_handlers: list[Handler[ValueChangeEventArguments[ValueT]]] = []
        self._released_value = self.value
        if on_release:
            self.on_release(on_release)

    def on_release(self, callback: Handler[ValueChangeEventArguments[ValueT]]) -> Self:
        """Add a callback to be invoked when the user finishes an interaction.

        In contrast to ``on_value_change``, this is not called while dragging, but once the element is released.
        Clicking the track and pressing an arrow key also finish an interaction and invoke the callback.
        The event's ``previous_value`` is the value at the previous release, ignoring programmatic changes.
        """
        if not self._release_handlers:
            self.on('change', self._handle_release, [None])
        self._release_handlers.append(callback)
        return self

    def _handle_release(self, e: GenericEventArguments) -> None:
        previous_value = self._released_value
        self._released_value = self._event_args_to_value(e)
        args = ValueChangeEventArguments(sender=self, client=self.client,
                                         value=self._released_value, previous_value=previous_value)
        for handler in self._release_handlers:
            handle_event(handler, args)
