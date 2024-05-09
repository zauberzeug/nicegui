from __future__ import annotations

from typing import TYPE_CHECKING, List

from .logging import log
from .slot import Slot

if TYPE_CHECKING:
    from .client import Client


class Context:

    def get_slot_stack(self) -> List[Slot]:
        """Return the slot stack of the current asyncio task. (DEPRECATED, use context.slot_stack instead)"""
        log.warning('context.get_slot_stack() is deprecated, use context.slot_stack instead')
        return self.slot_stack

    def get_slot(self) -> Slot:
        """Return the current slot. (DEPRECATED, use context.slot instead)"""
        log.warning('context.get_slot() is deprecated, use context.slot instead')
        return self.slot

    def get_client(self) -> Client:
        """Return the current client. (DEPRECATED, use context.client instead)"""
        log.warning('context.get_client() is deprecated, use context.client instead')
        return self.client

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
