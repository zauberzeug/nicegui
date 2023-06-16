from typing import Any, Callable, Optional

from .mixins.disableable_element import DisableableElement
from .mixins.text_element import TextElement
from .mixins.value_element import ValueElement


class Checkbox(TextElement, ValueElement, DisableableElement):

    def __init__(self, text: str = '', *, value: bool = False, on_change: Optional[Callable[..., Any]] = None) -> None:
        """Checkbox

        :param text: the label to display next to the checkbox
        :param value: whether it should be checked initially (default: `False`)
        :param on_change: callback to execute when value changes
        """
        super().__init__(tag='q-checkbox', text=text, value=value, on_value_change=on_change)
