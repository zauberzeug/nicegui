import justpy as jp
from typing import Callable, List, Dict, Union
from .choice_element import ChoiceElement

class Toggle(ChoiceElement):

    def __init__(self,
                 options: Union[List, Dict],
                 value: any = None,
                 on_change: Callable = None,
                 design: str = '',
                 classes: str = '',
                 ):
        """Toggle Element

        :param options: a list ['value1', ...] or dictionary `{'value1':'label1', ...}` specifying the options
        :param value: the inital value
        :param on_change: callback to execute when selection changes
        :param design: Quasar props to alter the appearance (see `their reference <https://quasar.dev/vue-components/toggle>`_)
        """

        view = jp.QBtnToggle(input=self.handle_change)

        super().__init__(view, value, options, on_change, design=design, classes=classes)
