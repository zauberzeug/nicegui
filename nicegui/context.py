from __future__ import annotations

from typing import TYPE_CHECKING, List

from .slot import Slot

if TYPE_CHECKING:
    from .client import Client


class Context:

    @property
    def slot_stack(self) -> List[Slot]:
        """Return the slot stack of the current asyncio task."""
        return Slot.get_stack()

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
