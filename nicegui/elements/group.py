from __future__ import annotations
from .element import Element
from ..globals import view_stack

class Group(Element):

    def __enter__(self):
        view_stack.append(self.view)
        return self

    def __exit__(self, *_):
        view_stack.pop()

    def tight(self) -> Group:
        return self.classes(replace='').style(replace='')
