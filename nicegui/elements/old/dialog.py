import asyncio
from typing import Any, Optional

import justpy as jp

from .group import Group


class Dialog(Group):

    def __init__(self, *, value: bool = False):
        """Dialog

        Creates a dialog.
        By default it is non-modal.
        To make it modal, set `.props('persistent')` on the dialog element.

        :param value: whether the dialog is already opened (default: `False`)
        """
        view = jp.QDialog(value=value, input=self._on_input, temp=False)

        self._submitted: Optional[asyncio.Event] = None
        self._result: Any = None

        super().__init__(view)

    def open(self) -> None:
        self.view.value = True
        self.update()

    def close(self) -> None:
        self.view.value = False
        self.update()

    def __await__(self):
        self._submitted = asyncio.Event()
        self._submitted.clear()
        self._result = None
        self.open()
        yield from self.view.update().__await__()
        yield from self._submitted.wait().__await__()
        self.close()
        return self._result

    def submit(self, result: Any) -> bool:
        self._result = result
        self._submitted.set()
        return False

    def _on_input(self, *_) -> bool:
        self._result = None
        if self._submitted is not None:
            self._submitted.set()
        self.update()
        return False
