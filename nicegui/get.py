from __future__ import annotations

from typing import Generic, Iterator, List, Optional, Type, TypeVar, Union

from typing_extensions import Self

from nicegui import context
from nicegui.element import Element

T = TypeVar('T', bound=Element)


class elements(Generic[T], Iterator[T]):

    def __init__(self, *,
                 type: Type[T] = Element,
                 key: Union[str, list[str], None] = None,
                 text: Union[str, list[str], None] = None,
                 ) -> None:
        """Get elements by type and/or key.

        :param type: filter by type of the elements; the iterator will be of type `type`
        :param key: filter by element keys; can be a list of strings or a single string where keys are separated by whitespace
        :param text: filter for elements which contain sub-text in their `.text` attribute; can be a singe string or list of strings which all must match
        """
        self._types = type
        self._keys = key.split() if isinstance(key, str) else key
        self._texts = [text] if isinstance(text, str) else text
        self._within_types: list[Element] = []
        self._within_keys: list[str] = []
        self._exclude_types: list[Element] = []
        self._exclude_keys: list[str] = []
        self.exclude_texts: list[str] = []

    def __iter__(self) -> Iterator[T]:
        client = context.get_client()
        return self.iterate(client.layout)

    def iterate(self, parent: Element, *, visited: List[Element] = []) -> Iterator[T]:
        for element in parent:
            if (self._types is None or isinstance(element, self._types)) and \
                (not self._keys or all(key in element._keys for key in self._keys)) and \
                (not self._texts or hasattr(element, 'text') and all(text in element.text for text in self._texts)) and \
                (not self._exclude_types or not any(isinstance(element, type) for type in self._exclude_types)) and \
                (not self._exclude_keys or not any(key in element._keys for key in self._exclude_keys)) and \
                    (not self.exclude_texts or ((hasattr(element, 'text') and not any(text in element.text for text in self.exclude_texts)))):
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

    def within(self, *, type: Optional[Element] = None, key: str = None) -> Self:
        if type is not None:
            assert issubclass(type, Element)
            self._within_types.append(type)
        if key is not None:
            self._within_keys.append(key)
        return self

    def exclude(self, *, type: Optional[Element] = None, key: Optional[str] = None, text: Optional[str] = None) -> Self:
        if type is not None:
            assert issubclass(type, Element)
            self._exclude_types.append(type)
        if key is not None:
            self._exclude_keys.append(key)
        if text is not None:
            self.exclude_texts.append(text)
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
