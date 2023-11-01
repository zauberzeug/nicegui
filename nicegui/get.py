from typing import Generic, Iterator, List, Optional, Type, TypeVar

from typing_extensions import Self

from nicegui import context
from nicegui.element import Element

T = TypeVar('T', bound=Element)


class elements(Generic[T], Iterator[T]):

    def __init__(self, *, type: Optional[Type[T]] = Element, key: str = '') -> None:
        self.type = type
        self.key = key
        self._within_types = []

    def __iter__(self) -> Iterator[T]:
        client = context.get_client()
        return self.iterate(client.layout)

    def iterate(self, parent: Element, *, visited: List[Element] = []) -> Iterator[T]:
        for element in parent:
            if (self.type is None or isinstance(element, self.type)) and \
                    (not self.key or self.key in element._keys):
                if not self._within_types or any(isinstance(element, type) for type in self._within_types for element in visited):
                    yield element
            yield from self.iterate(element, visited=visited + [element])

    def __next__(self) -> T:
        if self._iterator is None:
            raise StopIteration
        return next(self._iterator)

    def __len__(self) -> int:
        return len(list(iter(self)))

    def __getitem__(self, index) -> T:
        return list(iter(self))[index]

    def within(self, *, type: Optional[Type[T]] = Element) -> Self:
        self._within_types.append(type)
        return self

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
