from typing import Optional

from ..defaults import DEFAULT_PROP, DEFAULT_PROPS, resolve_defaults
from ..events import Handler, ValueChangeEventArguments
from .mixins.disableable_element import DisableableElement
from .mixins.icon_element import IconElement
from .mixins.text_element import TextElement
from .mixins.value_element import ValueElement


class Expansion(IconElement, TextElement, ValueElement, DisableableElement, default_classes='nicegui-expansion'):

    @resolve_defaults
    def __init__(self,
                 text: str = DEFAULT_PROPS['label'] | '', *,
                 caption: Optional[str] = DEFAULT_PROP | None,
                 icon: Optional[str] = DEFAULT_PROP | None,
                 group: Optional[str] = DEFAULT_PROP | None,
                 value: bool = DEFAULT_PROPS['model-value'] | False,
                 on_value_change: Optional[Handler[ValueChangeEventArguments]] = None
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
        super().__init__(tag='q-expansion-item', icon=icon, text=text, value=value, on_value_change=on_value_change)
        self._props.set_optional('caption', caption)
        self._props.set_optional('group', group)

    def open(self) -> None:
        """Open the expansion."""
        self.value = True

    def close(self) -> None:
        """Close the expansion."""
        self.value = False

    def _text_to_model_text(self, text: str) -> None:
        self._props['label'] = text
