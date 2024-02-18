from typing import Any, Callable, Optional

from .mixins.disableable_element import DisableableElement
from .mixins.text_element import TextElement
from .mixins.value_element import ValueElement


class Expansion(TextElement, ValueElement, DisableableElement):

    def __init__(self,
                 text: str = '', *,
                 caption: Optional[str] = None,
                 icon: Optional[str] = None,
                 group: Optional[str] = None,
                 value: bool = False,
                 on_value_change: Optional[Callable[..., Any]] = None
                 ) -> None:
        """Expansion Element

        Provides an expandable container based on Quasar's `QExpansionItem <https://quasar.dev/vue-components/expansion-item>`_ component.

        :param text: title text
        :param caption: optional caption (or sub-label) text
        :param icon: optional icon (default: None)
        :param group: optional group name for coordinated open/close state within the group a.k.a. "accordion mode"
        :param value: whether the expansion should be opened on creation (default: `False`)
        :param on_value_change: callback to execute when value changes
        """
        super().__init__(tag='q-expansion-item', text=text, value=value, on_value_change=on_value_change)
        if caption is not None:
            self._props['caption'] = caption
        if group is not None:
            self._props['group'] = group
        self._props['icon'] = icon
        self._classes.append('nicegui-expansion')

    def open(self) -> None:
        """Open the expansion."""
        self.value = True

    def close(self) -> None:
        """Close the expansion."""
        self.value = False

    def _text_to_model_text(self, text: str) -> None:
        self._props['label'] = text
