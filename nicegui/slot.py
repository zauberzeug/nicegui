from typing import TYPE_CHECKING, List

from . import globals

if TYPE_CHECKING:
    from .element import Element


class Slot:

    def __init__(self, parent: 'Element', name: str) -> None:
        self.name = name
        self.parent = parent
        self.children: List['Element'] = []
        self.child_count = 0

    def __enter__(self):
        self.child_count = len(self.children)
        globals.get_slot_stack().append(self)
        return self

    def __exit__(self, *_):
        globals.get_slot_stack().pop()
        globals.prune_slot_stack()
        self.lazy_update()

    def lazy_update(self) -> None:
        if self.child_count != len(self.children):
            self.child_count = len(self.children)
            self.parent.update()
