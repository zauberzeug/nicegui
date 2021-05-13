import justpy as jp
from .element import Element

class Button(Element):

    def __init__(self, text: str):

        view = jp.QButton(text=text)
        super().__init__(view)
