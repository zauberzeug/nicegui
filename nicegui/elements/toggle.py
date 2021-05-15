import justpy as jp
from typing import Callable, List, Dict, Union
from .choice_element import ChoiceElement

class Toggle(ChoiceElement):

    def __init__(self,
                 options: Union[List, Dict],
                 value: any = None,
                 design: str = '',
                 on_change: Callable = None):

        view = jp.QBtnToggle(input=self.handle_change)

        super().__init__(view, design, value, options, on_change)
