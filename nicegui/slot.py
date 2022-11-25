from typing import TYPE_CHECKING, List

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
        self.parent.client.slot_stack.append(self)
        return self

    def __exit__(self, *_):
        self.parent.client.slot_stack.pop()
        self.lazy_update()

    def lazy_update(self) -> None:
        if self.child_count != len(self.children):
            self.child_count = len(self.children)
            self.parent.update()
