from typing import Any, Callable, Optional

from .mixins.disableable_element import DisableableElement
from .mixins.value_element import ValueElement


class Expansion(ValueElement, DisableableElement):

    def __init__(self,
                 text: Optional[str] = None, *,
                 icon: Optional[str] = None,
                 value: bool = False,
                 on_value_change: Optional[Callable[..., Any]] = None
                 ) -> None:
        """Expansion Element

        Provides an expandable container based on Quasar's `QExpansionItem <https://quasar.dev/vue-components/expansion-item>`_ component.

        :param text: title text
        :param icon: optional icon (default: None)
        :param value: whether the expansion should be opened on creation (default: `False`)
        :param on_value_change: callback to execute when value changes
        """
        super().__init__(tag='q-expansion-item', value=value, on_value_change=on_value_change)
        if text is not None:
            self._props['label'] = text
        self._props['icon'] = icon
        self._classes = ['nicegui-expansion']

    def open(self) -> None:
        """Open the expansion."""
        self.value = True

    def close(self) -> None:
        """Close the expansion."""
        self.value = False
