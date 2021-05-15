import justpy as jp
from .element import Element

class Icon(Element):

    def __init__(self, name: str, size: str = '20px'):

        view = jp.QIcon(name=name, classes=f'q-pt-xs', size=size)

        super().__init__(view, '')
