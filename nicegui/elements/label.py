import justpy as jp
from .element import Element

class Label(Element):

    def __init__(self,
                 text: str = '',
                 ):
        """Label Element

        Displays some text.

        :param text: the content of the label
        """

        view = jp.Div(text=text)

        super().__init__(view)

    @property
    def text(self):

        return self.view.text

    @text.setter
    def text(self, text: any):

        self.view.text = text

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
