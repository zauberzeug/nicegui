import justpy as jp
from .element import Element

class Icon(Element):

    def __init__(self, name: str, size: str = '20px', color: str = 'dark'):

        view = jp.QIcon(name=name, classes=f'q-pt-xs text-{color}', size=size)

        super().__init__(view)
