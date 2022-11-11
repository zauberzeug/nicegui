from typing import TYPE_CHECKING, List

from . import globals

if TYPE_CHECKING:
    from .element import Element


class Slot:

    def __init__(self, parent: 'Element', name: str) -> None:
        self.name = name
        self.parent = parent
        self.children: List['Element'] = []

    def __enter__(self):
        globals.client_stack[-1].slot_stack.append(self)
        return self

    def __exit__(self, *_):
        globals.client_stack[-1].slot_stack.pop()
