from __future__ import annotations

from typing import Any

from ..events import Handler, ValueChangeEventArguments
from .mixins.disableable_element import DisableableElement
from .mixins.value_element import ValueElement


class Editor(ValueElement, DisableableElement, component='editor.js', default_classes='nicegui-editor'):
    VALUE_PROP: str = 'value'
    LOOPBACK = False

    def __init__(self,
                 *,
                 placeholder: str | None = None,
                 value: str = '',
                 on_change: Handler[ValueChangeEventArguments] | None = None,
                 ) -> None:
        """Editor

        A WYSIWYG editor based on `Quasar's QEditor <https://quasar.dev/vue-components/editor>`_.
        The value is a string containing the formatted text as HTML code.

        :param value: initial value
        :param on_change: callback to be invoked when the value changes
        """
        super().__init__(value=value, on_value_change=on_change)
        if placeholder is not None:
            self._props['placeholder'] = placeholder

    def _handle_value_change(self, value: Any) -> None:
        super()._handle_value_change(value)
        if self._send_update_on_value_change:
            self.run_method('updateValue')
