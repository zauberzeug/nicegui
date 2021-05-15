import justpy as jp
from typing import List
from .element import Element

class Link(Element):

    def __init__(self, text: str = '', href: str = '#', typography: List[str] = []):

        if isinstance(typography, str):
            typography = [typography]

        classes = ' '.join('text-' + t for t in typography)
        view = jp.A(text=text, href=href, classes=classes)

        super().__init__(view, '')
