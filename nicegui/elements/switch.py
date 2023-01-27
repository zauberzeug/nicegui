from typing import Callable, Optional

from .mixins.text_element import TextElement
from .mixins.value_element import ValueElement


class Switch(TextElement, ValueElement):

    def __init__(self,
                 text: str = '', *,
                 value: bool = False,
                 on_change: Optional[Callable] = None,
                 throttle: float = 0,
                 only_serverside_react: bool = False,
                 server_side_loopback: bool = False,
                 **kwargs) -> None:
        """Switch

        :param text: the label to display next to the switch
        :param value: whether it should be active initially (default: `False`)
        :param on_change: callback which is invoked when state is changed by the user
        """
        super().__init__(
            tag='q-toggle',
            text=text,
            value=value,
            on_value_change=on_change,
            throttle=throttle,
            only_serverside_react=only_serverside_react,
            server_side_loopback=server_side_loopback,
            **kwargs)
