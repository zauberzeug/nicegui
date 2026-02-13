from typing import Optional

from ..elements.mixins.disableable_element import DisableableElement
from ..events import Handler, UiEventArguments, handle_event


class PopupEdit(DisableableElement):
    def __init__(self, *,
                 on_show: Optional[Handler[UiEventArguments]] = None,
                 on_hide: Optional[Handler[UiEventArguments]] = None,) -> None:
        """Popup Edit

        This element is based on Quasar's `QPopupEdit <https://quasar.dev/vue-components/popup-edit>`_ component.
        It provides a popup editor that can be used to edit text or other content in a popup dialog.

        NOTE: We only use the popup edit as a container for other elements.

        - The JavaScript value of the popup edit will not be used.
        - Rather, value handling is done by the child elements using `NiceGUI's data binding <https://nicegui.io/documentation/section_binding_properties>`_.

        :param on_show: callback to execute when the popup editor is shown
        :param on_hide: callback to execute when the popup editor is hidden
        """
        super().__init__(tag='q-popup-edit')
        if on_show:
            self.on_show(on_show)
        if on_hide:
            self.on_hide(on_hide)

    def show(self) -> None:
        """Open the popup editor."""
        self.run_method('show')

    def hide(self) -> None:
        """Close the popup editor."""
        self.run_method('hide')

    def on_show(self, callback: Handler[UiEventArguments]) -> None:
        """Register a handler to be called when the popup editor is shown.

        :param handler: callback to execute when the popup editor is shown
        """
        self.on('show', lambda: handle_event(callback, UiEventArguments(sender=self, client=self.client)), args=[])

    def on_hide(self, callback: Handler[UiEventArguments]) -> None:
        """Register a handler to be called when the popup editor is hidden.

        :param handler: callback to execute when the popup editor is hidden
        """
        self.on('hide', lambda: handle_event(callback, UiEventArguments(sender=self, client=self.client)), args=[])
