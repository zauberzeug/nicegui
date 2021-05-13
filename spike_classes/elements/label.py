import justpy as jp
from .element import Element

class Label(Element):

    def __init__(self, text: str):

        view = jp.Div(text=text)
        super().__init__(view)
