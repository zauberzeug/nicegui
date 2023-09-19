from typing import Any, Callable, Optional

from .mixins.disableable_element import DisableableElement
from .mixins.value_element import ValueElement


class Editor(ValueElement, DisableableElement):

    def __init__(self,
                 *,
                 placeholder: Optional[str] = None,
                 value: str = '',
                 on_change: Optional[Callable[..., Any]] = None,
                 ) -> None:
        """Editor

        A code editor with syntax highlighting, based on `Quasar's QEditor <https://quasar.dev/vue-components/editor>`_.

        :param value: initial value
        :param on_change: callback to be invoked when the value changes
        """
        super().__init__(tag='q-editor', value=value, on_value_change=on_change)
        if placeholder is not None:
            self._props['placeholder'] = placeholder
