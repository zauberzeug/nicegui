from typing import Any

from ..defaults import DEFAULT_PROP, resolve_defaults
from ..events import Handler, ValueChangeEventArguments
from .mixins.disableable_element import DisableableElement
from .mixins.value_element import ValueElement


class Editor(ValueElement[str], DisableableElement, component='editor.js', default_classes='nicegui-editor'):
    VALUE_PROP: str = 'value'
    LOOPBACK = False

    @resolve_defaults
    def __init__(self,
                 *,
                 placeholder: str | None = DEFAULT_PROP | None,
                 value: str = DEFAULT_PROP | '',
                 on_change: Handler[ValueChangeEventArguments[str]] | None = None,
                 sanitize: bool = True,
                 ) -> None:
        """Editor

        A WYSIWYG editor based on `Quasar's QEditor <https://quasar.dev/vue-components/editor>`_.
        The value is a string containing the formatted text as HTML code.

        :param placeholder: text to show if no value is entered
        :param value: initial value
        :param on_change: callback to be invoked when the value changes
        :param sanitize: whether to sanitize the HTML code via DOMPurify before displaying it in the browser;
            markup which DOMPurify removes, like an ``<iframe>``, also disappears from the value once the user edits the content
            (default: ``True``, use ``False`` only with trusted content, *added in version 3.19.0*)
        """
        super().__init__(value=value, on_value_change=on_change)
        self._props.set_optional('placeholder', placeholder)
        self._props['sanitize'] = sanitize

    def _handle_value_change(self, value: Any) -> None:
        super()._handle_value_change(value)
        if self._send_update_on_value_change:
            self.run_method('updateValue')

    def _displayed_contents(self, *, only_visible: bool) -> list:
        return [*super()._displayed_contents(only_visible=only_visible), self._props.get(self.VALUE_PROP)]
