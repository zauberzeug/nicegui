from typing_extensions import Self

from ..defaults import DEFAULT_PROPS, resolve_defaults
from .mixins.value_element import ValueElement


class Popup(ValueElement[bool]):

    @resolve_defaults
    def __init__(self, *, value: bool = DEFAULT_PROPS['model-value'] | False) -> None:
        """Popup

        Creates a popup based on Quasar's `QPopupProxy <https://quasar.dev/vue-components/popup-proxy>`_ component.
        The popup should be placed inside the element where it should be shown
        and opens when the user clicks on that element.
        Depending on the screen width, it is displayed as a menu or,
        below the "breakpoint" prop (default: 450px), as a dialog.

        *Added in version 3.15.0*

        :param value: whether the popup is already opened (default: ``False``)
        """
        super().__init__(tag='q-popup-proxy', value=value)

    def _render_markdown(self) -> str:
        return self._children_to_markdown() if self.value else ''

    def open(self) -> Self:
        """Open the popup."""
        self.value = True
        return self

    def close(self) -> Self:
        """Close the popup."""
        self.value = False
        return self

    def toggle(self) -> Self:
        """Toggle the popup."""
        self.value = not self.value
        return self
