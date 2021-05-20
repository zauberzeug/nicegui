import justpy as jp
from typing import Callable, List, Dict, Union
from .choice_element import ChoiceElement

class Toggle(ChoiceElement):

    def __init__(self,
                 options: Union[List, Dict],
                 value: any = None,
                 on_change: Callable = None,
                 design: str = '',
                 classes:str='',
                 ):

        view = jp.QBtnToggle(input=self.handle_change)

        super().__init__(view, value, options, on_change, design=design, classes=classes)
