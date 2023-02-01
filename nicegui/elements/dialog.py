import asyncio
from typing import Any, Optional

from .mixins.value_element import ValueElement


class Dialog(ValueElement):

    def __init__(self, *, value: bool = False) -> None:
        """Dialog

        Creates a dialog.
        By default it is dismissible by clicking or pressing ESC.
        To make it persistent, set `.props('persistent')` on the dialog element.

        :param value: whether the dialog should be opened on creation (default: `False`)
        """
        super().__init__(tag='q-dialog', value=value, on_value_change=None)
        self._result: Any = None
        self._submitted: Optional[asyncio.Event] = None

    @property
    def submitted(self) -> asyncio.Event:
        if self._submitted is None:
            self._submitted = asyncio.Event()
        return self._submitted

    def open(self) -> None:
        self.value = True

    def close(self) -> None:
        self.value = False

    def __await__(self):
        self._result = None
        self.submitted.clear()
        self.open()
        yield from self.submitted.wait().__await__()
        result = self._result
        self.close()
        return result

    def submit(self, result: Any) -> None:
        self._result = result
        self.submitted.set()

    def on_value_change(self, value: Any) -> None:
        super().on_value_change(value)
        if not self.value:
            self._result = None
            self.submitted.set()
