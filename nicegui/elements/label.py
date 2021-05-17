import justpy as jp
from typing import Union, List
from .element import Element

class Label(Element):

    def __init__(self,
                 text: str = '',
                 typography: Union[str, List[str]] = []):

        if isinstance(typography, str):
            typography = [typography]
        classes = ' '.join('text-' + t for t in typography)

        view = jp.Div(text=text, classes=classes)

        super().__init__(view, '')

    @property
    def text(self):

        return self.view.text

    @text.setter
    def text(self, text: any):

        self.view.text = text

    def set_text(self, text: str):

        self.text = text

    def bind_text_to(self, target):

        self.text.bind_to(target, nesting=1)
        return self

    def bind_text_from(self, target):

        self.text.bind_from(target, nesting=1)
        return self

    def bind_text(self, target):

        self.text.bind(target, nesting=1)
        return self
