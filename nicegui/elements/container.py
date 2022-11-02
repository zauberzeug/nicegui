import justpy as jp

from .element import Element
from ..auto_context import ContextMixin


class Container(Element, ContextMixin):

    def __init__(self, **kwargs):
        """QDiv Container"""
        view = jp.QDiv(temp=True, **kwargs)
        super().__init__(view)
