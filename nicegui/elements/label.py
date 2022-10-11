import justpy as jp

from ..binding import BindableProperty, BindTextMixin
from .element import Element


class Label(Element, BindTextMixin):
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
