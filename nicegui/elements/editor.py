from typing import Any, Callable, Optional

from .mixins.disableable_element import DisableableElement
from .mixins.value_element import ValueElement


class Editor(ValueElement, DisableableElement):
    LOOPBACK = None

    def __init__(self,
                 *,
                 placeholder: Optional[str] = None,
                 value: str = '',
                 on_change: Optional[Callable[..., Any]] = None,
                 ) -> None:
        """Editor

        A WYSIWYG editor based on `Quasar's QEditor <https://quasar.dev/vue-components/editor>`_.
        The value is a string containing the formatted text as HTML code.

        :param value: initial value
        :param on_change: callback to be invoked when the value changes
        """
        super().__init__(tag='q-editor', value=value, on_value_change=on_change)
        self._classes.append('nicegui-editor')
        if placeholder is not None:
            self._props['placeholder'] = placeholder
