from typing import Any, Callable, Dict, List, Optional, Union

import justpy as jp

from .choice_element import ChoiceElement


class Toggle(ChoiceElement):

    def __init__(self, options: Union[List, Dict], *, value: Any = None, on_change: Optional[Callable] = None):
        """Toggle

        :param options: a list ['value1', ...] or dictionary `{'value1':'label1', ...}` specifying the options
        :param value: the initial value
        :param on_change: callback to execute when selection changes
        """
        view = jp.QBtnToggle(input=self.handle_change, temp=False)

        super().__init__(view, options, value=value, on_change=on_change)
