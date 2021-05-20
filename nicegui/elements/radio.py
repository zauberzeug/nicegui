import justpy as jp
from typing import Callable, List, Dict, Union
from .choice_element import ChoiceElement

class Radio(ChoiceElement):

    def __init__(self,
                 options: Union[List, Dict],
                 value: any = None,
                 on_change: Callable = None,
                 design: str = '',
                 classes: str = ''
                 ):
        """Radio Selection Element

        :param options: a list or dict specifying the options
        :param value: the inital value
        :param on_change: callback when selection changes
        :param design: Quasar props to alter the appearance (see `their reference <https://quasar.dev/vue-components/radio>`_)
        """

        view = jp.QOptionGroup(options=options, input=self.handle_change)

        super().__init__(view, value, options, on_change, design=design, classes=classes)
