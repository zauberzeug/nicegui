
import queue
import threading
from typing import Any, Dict, Optional, Sequence, Tuple, Union

from typing_extensions import Self

from .. import events, helpers, storage
from ..event_listener import EventListener


class EventManager:
    def __init__(self) -> None:
        self._event_listeners: Dict[str, list[EventListener]] = {}
        self._running = True
        self._window_monitor: Optional[threading.Thread] = None

    def start(self):
        self._window_monitor = threading.Thread(
            target=self._event_loop,
            name='pywebview_event_monitor',
            daemon=True
        )
        self._window_monitor.start()

    def _event_loop(self):
        from .native import event_queue

        while self._running:
            try:
                if event_queue is not None and not event_queue.empty():
                    data = event_queue.get_nowait()
                    self._handle_event(**data)
            except queue.Empty:
                continue

    def on(self,
            type: str,  # pylint: disable=redefined-builtin
            handler: Optional[events.Handler[events.PywebviewEventArguments]] = None,
            args: Union[None, Sequence[str], Sequence[Optional[Sequence[str]]]] = None,
            *,
            throttle: float = 0.0,
            leading_events: bool = True,
            trailing_events: bool = True,
            # DEPRECATED: None will be removed in version 3.0
            js_handler: Optional[str] = '(...args) => emit(...args)',
           ) -> Self:
        """Subscribe to an event.

        The event handler can be a Python function, a JavaScript function or a combination of both:

        - If you want to handle the event on the server with all (serializable) event arguments,
            use a Python ``handler``.
        - If you want to handle the event on the client side without emitting anything to the server,
            use ``js_handler`` with a JavaScript function handling the event.
        - If you want to handle the event on the server with a subset or transformed version of the event arguments,
            use ``js_handler`` with a JavaScript function emitting the transformed arguments using ``emit()``, and
            use a Python ``handler`` to handle these arguments on the server side.
            The ``js_handler`` can also decide to selectively emit arguments to the server,
            in which case the Python ``handler`` will not always be called.

        Note that the arguments ``throttle``, ``leading_events``, and ``trailing_events`` are only relevant
        when emitting events to the server.

        *Updated in version 2.18.0: Both handlers can be specified at the same time.*

        :param type: name of the event (e.g. "click", "mousedown", or "update:model-value")
        :param handler: callback that is called upon occurrence of the event
        :param args: arguments included in the event message sent to the event handler (default: ``None`` meaning all)
        :param throttle: minimum time (in seconds) between event occurrences (default: 0.0)
        :param leading_events: whether to trigger the event handler immediately upon the first event occurrence (default: ``True``)
        :param trailing_events: whether to trigger the event handler after the last event occurrence (default: ``True``)
        :param js_handler: JavaScript function that is handling the event on the client (default: "(...args) => emit(...args)")
        """
        if js_handler is None:
            helpers.warn_once('Passing `js_handler=None` to `on()` is deprecated. '
                              'Use the default "(...args) => emit(...args)" instead or remove the parameter.')
        if js_handler == '(...args) => emit(...args)':
            js_handler = None

        if handler or js_handler:
            listener = EventListener(
                element_id=0,
                type=helpers.event_type_to_camel_case(type),
                args=[args] if args and isinstance(args[0], str) else args,  # type: ignore
                handler=handler,
                js_handler=js_handler,
                throttle=throttle,
                leading_events=leading_events,
                trailing_events=trailing_events,
                request=storage.request_contextvar.get(),
            )
            if self._event_listeners.get(listener.type):
                self._event_listeners[listener.type].append(listener)
            else:
                self._event_listeners[listener.type] = [listener]
        return self

    def _handle_event(self, id: str, args: Tuple[Any, ...]) -> None:
        listeners = self._event_listeners.get(id)
        if listeners is None:
            return

        for listener in listeners:
            storage.request_contextvar.set(listener.request)
            event_args = events.PywebviewEventArguments(id=id, args=args)
            events.handle_event(listener.handler, event_args)


event_manager = EventManager()
