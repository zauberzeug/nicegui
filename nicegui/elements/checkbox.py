from typing import Callable, Optional

from .binding_mixins import BindTextMixin
from .bool_element import BoolElement


class Checkbox(BoolElement, BindTextMixin):

    def __init__(self, text: str = '', *, value: bool = False, on_change: Optional[Callable] = None) -> None:
        """Checkbox

        :param text: the label to display next to the checkbox
        :param value: whether it should be checked initially (default: `False`)
        :param on_change: callback to execute when value changes
        """
        super().__init__('q-checkbox', value=value, on_change=on_change)
        self.text = text
        self._text = text

    def on_text_change(self, text: str) -> None:
        self._text = text
        self.update()
