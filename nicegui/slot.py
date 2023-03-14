from typing import Optional, TYPE_CHECKING, List

from . import globals

if TYPE_CHECKING:
    from .element import Element


class Slot:

    def __init__(self, parent: 'Element', name: str, template: Optional[str] = None) -> None:
        self.name = name
        self.parent = parent
        self.children: List['Element'] = []
        self.template: str = template

    def __enter__(self):
        globals.get_slot_stack().append(self)
        return self

    def __exit__(self, *_):
        globals.get_slot_stack().pop()
        globals.prune_slot_stack()
