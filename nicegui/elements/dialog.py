import asyncio
from typing import Any, Optional

from .mixins.value_element import ValueElement


class Dialog(ValueElement):

    def __init__(self, *, value: bool = False) -> None:
        """Dialog

        Creates a dialog based on Quasar's `QDialog <https://quasar.dev/vue-components/dialog>`_ component.
        By default it is dismissible by clicking or pressing ESC.
        To make it persistent, set `.props('persistent')` on the dialog element.

        NOTE: The dialog is an element.
        That means it is not removed when closed, but only hidden.
        You should either create it only once and then reuse it, or remove it with `.clear()` after dismissal.

        :param value: whether the dialog should be opened on creation (default: `False`)
        """
        super().__init__(tag='q-dialog', value=value, on_value_change=None)
        self._result: Any = None
        self._submitted: Optional[asyncio.Event] = None

    @property
    def submitted(self) -> asyncio.Event:
        """An event that is set when the dialog is submitted."""
        if self._submitted is None:
            self._submitted = asyncio.Event()
        return self._submitted

    def open(self) -> None:
        """Open the dialog."""
        self.value = True

    def close(self) -> None:
        """Close the dialog."""
        self.value = False

    def __await__(self):
        self._result = None
        self.submitted.clear()
        self.open()
        yield from self.submitted.wait().__await__()  # pylint: disable=no-member
        result = self._result
        self.close()
        return result

    def submit(self, result: Any) -> None:
        """Submit the dialog with the given result."""
        self._result = result
        self.submitted.set()

    def _handle_value_change(self, value: Any) -> None:
        super()._handle_value_change(value)
        if not self.value:
            self._result = None
            self.submitted.set()
