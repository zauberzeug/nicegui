from typing import Generic, Iterator, Optional, Type, TypeVar

from typing_extensions import Self

from nicegui import context
from nicegui.element import Element

T = TypeVar('T', bound=Element)


class elements(Generic[T], Iterator[T]):

    def __init__(self, *, type: Optional[Type[T]] = Element):
        self.type = type

    def __iter__(self) -> Iterator[T]:
        client = context.get_client()
        return self.iterate(client.layout)

    def __next__(self) -> T:  # Define __next__ to return the next item from _iterator
        if self._iterator is None:
            raise StopIteration
        return next(self._iterator)

    def iterate(self, parent: Element) -> Iterator[T]:
        for element in parent:
            if self.type is None or isinstance(element, self.type):
                yield element
            yield from self.iterate(element)

    def __len__(self) -> int:
        return len(list(iter(self)))

    def __getitem__(self, index) -> T:
        return list(iter(self))[index]

    def classes(self, add: Optional[str] = None, *, remove: Optional[str] = None, replace: Optional[str] = None) -> Self:
        for element in self:
            element.classes(add, remove=remove, replace=replace)

    def style(self, add: Optional[str] = None, *, remove: Optional[str] = None, replace: Optional[str] = None) -> Self:
        for element in self:
            element.style(add, remove=remove, replace=replace)

    def props(self, add: Optional[str] = None, *, remove: Optional[str] = None) -> Self:
        for element in self:
            element.props(add, remove=remove)


get = elements
