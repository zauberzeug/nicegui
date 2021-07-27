from typing import Callable
import justpy as jp
from .element import Element
from ..utils import handle_exceptions, provide_arguments

class Button(Element):

    def __init__(self,
                 text: str = '',
                 *,
                 on_click: Callable = None,
                 ):
        """Button Element

        :param text: the label of the button
        :param on_click: callback which is invoked when button is pressed
        """

        view = jp.QButton(label=text, color='primary')

        if on_click is not None:
            view.on('click', handle_exceptions(provide_arguments(on_click)))

        super().__init__(view)

    @property
    def text(self):

        return self.view.label

    @text.setter
    def text(self, text: any):

        self.view.label = text

    def set_text(self, text: str):

        self.text = text

    def bind_text_to(self, target, forward=lambda x: x):

        self.text.bind_to(target, forward=forward, nesting=1)
        return self

    def bind_text_from(self, target, backward=lambda x: x):

        self.text.bind_from(target, backward=backward, nesting=1)
        return self

    def bind_text(self, target, forward=lambda x: x, backward=lambda x: x):

        self.text.bind(target, forward=forward, backward=backward, nesting=1)
        return self
