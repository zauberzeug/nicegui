from typing import TYPE_CHECKING, Iterator, List, Optional

from typing_extensions import Self

from . import globals

if TYPE_CHECKING:
    from .element import Element


class Slot:

    def __init__(self, parent: 'Element', name: str, template: Optional[str] = None) -> None:
        self.name = name
        self.parent = parent
        self.template = template
        self.children: List['Element'] = []

    def __enter__(self) -> Self:
        globals.get_slot_stack().append(self)
        return self

    def __exit__(self, *_) -> None:
        globals.get_slot_stack().pop()
        globals.prune_slot_stack()

    def __iter__(self) -> Iterator['Element']:
        return iter(self.children)
