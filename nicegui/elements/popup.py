from ..defaults import DEFAULT_PROPS, resolve_defaults
from .mixins.openable_element import OpenableElement


class Popup(OpenableElement):

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
