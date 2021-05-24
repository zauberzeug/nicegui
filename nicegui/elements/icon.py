import justpy as jp
from .element import Element

class Icon(Element):

    def __init__(self,
                 name: str,
                 ):

        view = jp.QIcon(name=name, classes=f'q-pt-xs', size='20px')

        super().__init__(view)
