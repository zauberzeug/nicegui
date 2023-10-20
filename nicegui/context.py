from __future__ import annotations

from typing import TYPE_CHECKING, List

from .slot import Slot

if TYPE_CHECKING:
    from .client import Client


def get_slot_stack() -> List[Slot]:
    """Return the slot stack of the current asyncio task."""
    return Slot.get_stack()


def get_slot() -> Slot:
    """Return the current slot."""
    return Slot.get_stack()[-1]


def get_client() -> Client:
    """Return the current client."""
    return get_slot().parent.client
