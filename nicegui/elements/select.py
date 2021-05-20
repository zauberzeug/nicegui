import justpy as jp
from typing import Callable, List, Dict, Union
from .choice_element import ChoiceElement

class Select(ChoiceElement):

    def __init__(self,
                 options: Union[List, Dict],
                 value: any = None,
                 on_change: Callable = None,
                 design: str = '',
                 classes: str = ''
                 ):
        """Dropdown Selection Element

        :param options: a list or dict specifying the options
        :param value: the inital value
        :param on_change: callback when selection changes
        :param design: Quasar props to alter the appearance (see `their reference <https://quasar.dev/vue-components/select>`_)
        """

        view = jp.QSelect(options=options, input=self.handle_change)

        super().__init__(view, value, options, on_change, design=design, classes=classes)

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
