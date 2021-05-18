import justpy as jp
from typing import Callable, List, Dict, Union
from .choice_element import ChoiceElement

class Select(ChoiceElement):

    def __init__(self,
                 options: Union[List, Dict],
                 value: any = None,
                 design: str = '',
                 on_change: Callable = None):

        view = jp.QSelect(options=options, input=self.handle_change)

        super().__init__(view, design, value, options, on_change)

    def value_to_view(self, value: any):

        matches = [o for o in self.view.options if o['value'] == value]
        if any(matches):
            return matches[0]['label']
        else:
            return value
