import justpy as jp
from typing import Callable, List, Dict, Union
from .choice_element import ChoiceElement

class Select(ChoiceElement):

    def __init__(self,
                 options: Union[List, Dict],
                 value: any = None,
                 on_change: Callable = None,
                 design: str = '',
                 classes: str=''
                 ):

        view = jp.QSelect(options=options, input=self.handle_change)

        super().__init__(view, value, options, on_change, design=design, classes=classes)

    def value_to_view(self, value: any):

        matches = [o for o in self.view.options if o['value'] == value]
        if any(matches):
            return matches[0]['label']
        else:
            return value
