from typing import Generic, Iterator, List, Optional, Type, TypeVar, Union

from typing_extensions import Self

from nicegui import context
from nicegui.element import Element

T = TypeVar('T', bound=Element)


class elements(Generic[T], Iterator[T]):

    def __init__(self, *, type: Type[T] = Element, key: Union[str, list[str], None] = None) -> None:
        """Get elements by type and/or key.

        :param type: type of the elements to get (iterator will then be of type `type`)
        :param key: key of the elements to get, can be a list of strings or a single string where keys are separated by whitespace
        """
        self._types = type
        self._keys = key.split() if isinstance(key, str) else key
        assert self._keys is None or isinstance(self._keys, list)
        self._within_types: list[Element] = []
        self._within_keys: list[str] = []

    def __iter__(self) -> Iterator[T]:
        client = context.get_client()
        return self.iterate(client.layout)

    def iterate(self, parent: Element, *, visited: List[Element] = []) -> Iterator[T]:
        for element in parent:
            if (self._types is None or isinstance(element, self._types)) and \
                    (not self._keys or all(key in element._keys for key in self._keys)):
                if (not self._within_types or any(isinstance(element, type) for type in self._within_types for element in visited)) and \
                        (not self._within_keys or any(key in element._keys for key in self._within_keys for element in visited)):
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

    def within(self, *, type: Optional[Type[T]] = None, key: str = None) -> Self:
        if type is not None:
            assert issubclass(type, Element)
            self._within_types.append(type)
        if key is not None:
            self._within_keys.append(key)
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
