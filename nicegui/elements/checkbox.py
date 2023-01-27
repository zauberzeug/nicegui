from typing import Callable, Optional

from .mixins.text_element import TextElement
from .mixins.value_element import ValueElement


class Checkbox(TextElement, ValueElement):

    def __init__(self,
                 text: str = '', *,
                 value: bool = False,
                 on_change: Optional[Callable] = None,
                 throttle: float = 0,
                 only_serverside_react: bool = False,
                 server_side_loopback: bool = False,
                 **kwargs) -> None:
        """Checkbox

        :param text: the label to display next to the checkbox
        :param value: whether it should be checked initially (default: `False`)
        :param on_change: callback to execute when value changes
        """
        super().__init__(
            tag='q-checkbox',
            text=text,
            value=value,
            on_value_change=on_change,
            throttle=throttle,
            only_serverside_react=only_serverside_react,
            server_side_loopback=server_side_loopback,
            **kwargs)
