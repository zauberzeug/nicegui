from typing import TYPE_CHECKING, List

from . import globals

if TYPE_CHECKING:
    from .element import Element


class Slot:

    def __init__(self, parent: 'Element', name: str) -> None:
        self.name = name
        self.parent = parent
        self.children: List['Element'] = []

        self._child_count_before_enter = 0

    def __enter__(self):
        self._child_count_before_enter = len(self.children)
        globals.client_stack[-1].slot_stack.append(self)
        return self

    def __exit__(self, *_):
        globals.client_stack[-1].slot_stack.pop()
        if len(self.children) != self._child_count_before_enter:
            self.parent.update()
