from __future__ import annotations

import inspect

from typing_extensions import ParamSpec

from .event import Event, _invoke_and_forget

P = ParamSpec('P')


class DistributedEvent(Event[P]):
    """Distributed Event

    A subclass of Event that automatically shares events across all NiceGUI instances
    in the same network when distributed mode is enabled via `ui.run(distributed=True)`.

    All instances of the same DistributedEvent (determined by creation location)
    across different processes will receive emitted events.

    *Added in version 3.x.x*
    """

    def __init__(self) -> None:
        """Create a distributed event that will be shared across instances."""
        super().__init__()
        # NOTE: Use creation location for topic to ensure same DistributedEvent in different processes shares the same topic
        frame = inspect.currentframe()
        assert frame is not None
        frame = frame.f_back
        assert frame is not None
        # NOTE: Skip frames from typing module (when using DistributedEvent[T]() syntax)
        while frame and 'typing.py' in frame.f_code.co_filename:
            frame = frame.f_back
        assert frame is not None
        module = inspect.getmodule(frame)
        module_name = module.__name__ if module else 'unknown'
        self.topic = f'event_{module_name}:{frame.f_code.co_filename}:{frame.f_lineno}'
        self._zenoh_setup_done = False
        self._setup_distributed()

    def _setup_distributed(self) -> None:
        """Set up distributed event handling if enabled.

        This method is safe to call multiple times due to the _zenoh_setup_done guard.
        It's called during DistributedEvent initialization and retroactively when DistributedSession.initialize() is called.
        Events emitted before distributed mode is initialized will only be local.
        """
        if self._zenoh_setup_done:
            return
        from .distributed import DistributedSession
        session = DistributedSession.get()
        if session is None:
            return

        def remote_handler(data: dict) -> None:
            """Handle events received from remote instances."""
            for callback in self.callbacks:
                _invoke_and_forget(callback, *data.get('args', ()), **data.get('kwargs', {}))

        session.subscribe(self.topic, remote_handler)
        self._zenoh_setup_done = True

    def emit(self, *args: P.args, **kwargs: P.kwargs) -> None:
        """Fire the event without waiting for the subscribed callbacks to complete."""
        if not self._zenoh_setup_done:
            self._setup_distributed()

        super().emit(*args, **kwargs)

        from .distributed import DistributedSession
        session = DistributedSession.get()
        if session is not None:
            session.publish(self.topic, {'args': args, 'kwargs': kwargs})

    async def call(self, *args: P.args, **kwargs: P.kwargs) -> None:
        """Fire the event and wait asynchronously until all subscribed callbacks are completed."""
        if not self._zenoh_setup_done:
            self._setup_distributed()

        await super().call(*args, **kwargs)

        from .distributed import DistributedSession
        session = DistributedSession.get()
        if session is not None:
            session.publish(self.topic, {'args': args, 'kwargs': kwargs})
