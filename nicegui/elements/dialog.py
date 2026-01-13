import asyncio
from typing import Any, Optional

from ..defaults import DEFAULT_PROPS, resolve_defaults
from ..element import Element
from .mixins.value_element import ValueElement


class Dialog(ValueElement, component='dialog.js'):

    @resolve_defaults
    def __init__(self, *,
                 value: bool = DEFAULT_PROPS['model-value'] | False,
                 top_level: bool = False,  # DEPRECATED: top_level will default to True in NiceGUI 4.0
                 ) -> None:
        """Dialog

        Creates a dialog based on Quasar's `QDialog <https://quasar.dev/vue-components/dialog>`_ component.
        By default it is dismissible by clicking or pressing ESC.
        To make it persistent, set `.props('persistent')` on the dialog element.

        NOTE: The dialog is an element.
        That means it is not removed when closed, but only hidden.
        You should either create it only once and then reuse it, or remove it with `.clear()` after dismissal.

        *Since version 3.6.0*:
        You can now create a dialog as a top level element by setting ``top_level=True``.
        This will ensure that the dialog is always visible and not hidden when nested inside a hidden container.
        The dialog will still be automatically deleted when the original context is deleted.
        This behavior will be the default in NiceGUI 4.0.

        :param value: whether the dialog should be opened on creation (default: `False`)
        :param top_level: whether the dialog is created as a top level element (default: `False`, *added in version 3.6.0*, will default to `True` in NiceGUI 4.0)
        """
        super().__init__(value=value, on_value_change=None)
        self._result: Any = None
        self._submitted: Optional[asyncio.Event] = None

        if top_level is True:
            self.move(self.client.content)
            _DeletePropagationElement(self)

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


class _DeletePropagationElement(Element):

    def __init__(self, element_to_delete: Element) -> None:
        super().__init__()
        self.visible = False
        self._element_to_delete = element_to_delete

    def _handle_delete(self) -> None:
        self._element_to_delete.delete()
        return super()._handle_delete()
