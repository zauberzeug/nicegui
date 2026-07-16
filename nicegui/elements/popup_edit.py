from typing_extensions import Self

from ..events import Handler, UiEventArguments, handle_event
from .mixins.disableable_element import DisableableElement


class PopupEdit(DisableableElement):

    def __init__(self, *,
                 on_show: Handler[UiEventArguments] | None = None,
                 on_hide: Handler[UiEventArguments] | None = None,
                 ) -> None:
        """Popup Edit

        This element is based on Quasar's `QPopupEdit <https://quasar.dev/vue-components/popup-edit>`_ component.
        It provides a popup editor that can be used to edit text or other content in a popup dialog.

        This element only serves as a container for other elements; its own JavaScript value is not used.
        Value handling is done by the child elements using `NiceGUI's data binding <https://nicegui.io/documentation/section_binding_properties>`_.

        *Added in version 3.15.0*

        :param on_show: callback to execute when the popup editor is shown
        :param on_hide: callback to execute when the popup editor is hidden
        """
        super().__init__(tag='q-popup-edit')
        for prop in ('buttons', 'auto-save', 'validate', 'label-set', 'label-cancel'):
            self._props.add_warning(prop,
                                    f'The prop "{prop}" operates on QPopupEdit\'s own model value, which `ui.popup_edit` does not use. '
                                    'Use data binding on the child elements instead.')
        if on_show:
            self.on_show(on_show)
        if on_hide:
            self.on_hide(on_hide)

    def open(self) -> Self:
        """Open the popup editor."""
        self.run_method('show')
        return self

    def close(self) -> Self:
        """Close the popup editor."""
        self.run_method('hide')
        return self

    def on_show(self, callback: Handler[UiEventArguments]) -> Self:
        """Register a handler to be called when the popup editor is shown.

        :param callback: callback to execute when the popup editor is shown
        """
        self.on('show', lambda: handle_event(callback, UiEventArguments(sender=self, client=self.client)), args=[])
        return self

    def on_hide(self, callback: Handler[UiEventArguments]) -> Self:
        """Register a handler to be called when the popup editor is hidden.

        :param callback: callback to execute when the popup editor is hidden
        """
        self.on('hide', lambda: handle_event(callback, UiEventArguments(sender=self, client=self.client)), args=[])
        return self
