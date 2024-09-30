from typing import Optional

from ..events import Handler, ValueChangeEventArguments
from .mixins.disableable_element import DisableableElement
from .mixins.text_element import TextElement
from .mixins.value_element import ValueElement


class Checkbox(TextElement, ValueElement, DisableableElement):

    def __init__(self, text: str = '', *, value: bool = False, on_change: Optional[Handler[ValueChangeEventArguments]] = None) -> None:
        """Checkbox

        This element is based on Quasar's `QCheckbox <https://quasar.dev/vue-components/checkbox>`_ component.

        :param text: the label to display next to the checkbox
        :param value: whether it should be checked initially (default: `False`)
        :param on_change: callback to execute when value changes
        """
        super().__init__(tag='q-checkbox', text=text, value=value, on_value_change=on_change)
