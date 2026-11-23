import asyncio
import weakref
from typing import Any, Self

from ..context import context
from ..defaults import DEFAULT_PROPS, resolve_defaults
from ..element import Element
from ..helpers import NoImplicitAwait
from .mixins.openable_element import OpenableElement


class Dialog(OpenableElement, NoImplicitAwait, component='dialog.js'):

    @resolve_defaults
    def __init__(self, *, value: bool = DEFAULT_PROPS['model-value'] | False) -> None:
        """Dialog

        Creates a dialog based on Quasar's `QDialog <https://quasar.dev/vue-components/dialog>`_ component.
        By default it is dismissible by clicking or pressing ESC.
        To make it persistent, set ``.props('persistent')`` on the dialog element.

        Note: The dialog is an element.
        That means it is not removed when closed, but only hidden.
        You should either create it only once and then reuse it, or remove it with ``.clear()`` after dismissal.

        *Updated in version 3.16.0: Awaiting a dialog resolves with ``None`` when the dialog is deleted,
        e.g. because the client disconnected.*

        :param value: whether the dialog should be opened on creation (default: ``False``)
        """
        with context.client.layout:
            super().__init__(value=value, on_value_change=None)

        # create a canary element in the current context to trigger the deletion of the dialog when its parent is deleted
        canary = Element()
        canary.visible = False
        weakref.finalize(
            canary, lambda: self.delete() if not self.is_deleted and self._parent_slot and self._parent_slot() else None
        )

        self._pending_result: asyncio.Future | None = None
        self._submitted: asyncio.Event | None = None

    @property
    def submitted(self) -> asyncio.Event:
        """An event that is set when the dialog is submitted.

        *Updated in version 3.16.0: The event is also set when the dialog is deleted.*
        """
        if self._submitted is None:
            self._submitted = asyncio.Event()
        return self._submitted

    def toggle(self) -> Self:  # pylint: disable=useless-parent-delegation
        """Toggle the dialog.

        *Added in version 3.15.0*
        """
        return super().toggle()

    def __await__(self):
        if not self._is_safe_to_interact():
            return None  # the dialog cannot be submitted anymore, so we resolve immediately instead of waiting forever
        if self._pending_result is None:  # otherwise join the awaits that are already waiting, e.g. after a double-click
            self._pending_result = asyncio.get_running_loop().create_future()
            self.submitted.clear()
            self.open()
        result = yield from asyncio.shield(self._pending_result).__await__()
        if not self.is_deleted and self._pending_result is None:
            # closing a deleted dialog would warn about using a deleted element,
            # and closing while a new round is already awaited would resolve that round with None
            self.close()
        return result

    def submit(self, result: Any) -> None:
        """Submit the dialog with the given result."""
        self._resolve(result)

    def _resolve(self, result: Any) -> None:
        # the awaiting tasks hold the future, so the dialog does not keep the result alive
        future, self._pending_result = self._pending_result, None
        if future is not None and not future.get_loop().is_closed():  # at interpreter exit nobody can be woken up anymore
            future.set_result(result)
        self.submitted.set()

    def _handle_value_change(self, value: Any) -> None:
        super()._handle_value_change(value)
        if not self.value:
            self._resolve(None)

    def _handle_delete(self) -> None:
        # resolve pending awaits so their tasks don't wait forever, e.g. when the client is deleted after a disconnect
        # (a result submitted just before deletion has already resolved them, so it still reaches the awaiting tasks)
        self._resolve(None)
        super()._handle_delete()
