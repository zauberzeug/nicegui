from __future__ import annotations

from typing import TYPE_CHECKING

from . import core
from .slot import Slot

if TYPE_CHECKING:
    from .client import Client


class Context:

    @property
    def slot_stack(self) -> list[Slot]:
        """Return the slot stack of the current asyncio task."""
        stack = Slot.get_stack()
        if not stack and not core.script_mode and not core.app.is_started:
            # create a pseudo client to "survive" until reaching `ui.run()`
            from .client import Client  # pylint: disable=import-outside-toplevel,cyclic-import
            from .page import page  # pylint: disable=import-outside-toplevel,cyclic-import
            if not Client.instances:  # in case some kind of dummy client is already created
                core.script_mode = True
                core.script_client = Client(page('/')).__enter__()  # pylint: disable=unnecessary-dunder-call
                stack = Slot.get_stack()
        return stack

    @property
    def slot(self) -> Slot:
        """Return the current slot."""
        slot_stack = self.slot_stack
        if not slot_stack:
            raise RuntimeError('The current slot cannot be determined because the slot stack for this task is empty.\n'
                               'This may happen if you try to create UI from a background task.\n'
                               'To fix this, enter the target slot explicitly using `with container_element:`.')
        return slot_stack[-1]

    @property
    def client(self) -> Client:
        """Return the current client."""
        return self.slot.parent.client


context = Context()
