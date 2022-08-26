import justpy as jp

from ..binding import BindableProperty, bind_from, bind_to
from .element import Element


class Label(Element):
    text = BindableProperty()

    def __init__(self, text: str = ''):
        """Label

        Displays some text.

        :param text: the content of the label
        """
        view = jp.Div(text=text, temp=False)
        super().__init__(view)

        self.text = text
        self.bind_text_to(self.view, 'text')

    def set_text(self, text: str):
        self.text = text

    def bind_text_to(self, target_object, target_name, forward=lambda x: x):
        bind_to(self, 'text', target_object, target_name, forward=forward)
        return self

    def bind_text_from(self, target_object, target_name, backward=lambda x: x):
        bind_from(self, 'text', target_object, target_name, backward=backward)
        return self

    def bind_text(self, target_object, target_name, forward=lambda x: x, backward=lambda x: x):
        bind_from(self, 'text', target_object, target_name, backward=backward)
        bind_to(self, 'text', target_object, target_name, forward=forward)
        return self
