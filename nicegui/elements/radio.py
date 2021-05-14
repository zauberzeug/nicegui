import justpy as jp
from typing import Callable, List, Dict, Union
from .choice_element import ChoiceElement

class Radio(ChoiceElement):

    def __init__(self, options: Union[List, Dict], value: any = None, on_change: Callable = None):

        view = jp.QOptionGroup(options=options, input=self.handle_change)

        super().__init__(view, value=value, options=options, on_change=on_change)
