import justpy as jp
from .element import Element

class Link(Element):

    def __init__(self,
                 text: str = '',
                 href: str = '#',
                 ):

        view = jp.A(text=text, href=href)

        super().__init__(view)
