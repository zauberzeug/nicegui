from typing import Callable, Optional

from .mixins.text_element import TextElement
from .mixins.value_element import ValueElement


class Checkbox(TextElement, ValueElement):

    def __init__(self, text: str = '', *, value: bool = False, on_change: Optional[Callable] = None) -> None:
        """Checkbox

        :param text: the label to display next to the checkbox
        :param value: whether it should be checked initially (default: `False`)
        :param on_change: callback to execute when value changes
        """
        super().__init__('q-checkbox')
        self.init_text(text)
        self.init_value(value, on_change)
