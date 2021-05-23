import justpy as jp
from typing import Callable, List, Dict, Union
from .choice_element import ChoiceElement

class Select(ChoiceElement):

    def __init__(self,
                 options: Union[List, Dict],
                 *,
                 value: any = None,
                 on_change: Callable = None,
                 ):
        """Dropdown Selection Element

        :param options: a list ['value1', ...] or dictionary `{'value1':'label1', ...}` specifying the options
        :param value: the inital value
        :param on_change: callback to execute when selection changes
        """

        view = jp.QSelect(options=options, input=self.handle_change)

        super().__init__(view, options, value=value, on_change=on_change)

    def value_to_view(self, value: any):

        matches = [o for o in self.view.options if o['value'] == value]
        if any(matches):
            return matches[0]['label']
        else:
            return value

    def handle_change(self, msg):

        msg['label'] = msg['value']['label']
        msg['value'] = msg['value']['value']
        return super().handle_change(msg)
