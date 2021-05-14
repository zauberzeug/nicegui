import justpy as jp
from typing import List
from .element import Element

class Label(Element):

    def __init__(self, text: str = '', typography: List[str] = []):

        if isinstance(typography, str):
            typography = [typography]
        classes = ' '.join('text-' + t for t in typography)

        view = jp.Div(text=text, classes=classes)

        super().__init__(view)

    def set_text(self, text: str):

        self.view.text = text
