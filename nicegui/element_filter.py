from __future__ import annotations

from typing import Generic, Iterator, List, Optional, Type, TypeVar, Union

from typing_extensions import Self

from nicegui import context
from nicegui.element import Element
from nicegui.elements.mixins.content_element import ContentElement
from nicegui.elements.mixins.source_element import SourceElement

T = TypeVar('T', bound=Element)


class ElementFilter(Generic[T], Iterator[T]):
    DEFAULT_LOCAL_SCOPE = False

    def __init__(self, *,
                 kind: Type[T] = Element,
                 marker: Union[str, list[str], None] = None,
                 content: Union[str, list[str], None] = None,
                 local_scope: bool = DEFAULT_LOCAL_SCOPE,
                 ) -> None:
        """ElementFilter

        Sometimes it's handy to search the Python element tree of the current page. 
        `ElementFilter()` allows powerful filtering by kind of elements, markers and content.
        It also provides a fluent interface to apply more filters like excluding elements or filtering for elements within a specific parent.
        The filter can be used as an iterator to iterate over the found elements and is always applied while iterating and not when being instantiated.

        :param kind: filter by element type; the iterator will be of type `type`
        :param marker: filter by element markers; can be a list of strings or a single string where markers are separated by whitespace
        :param content: filter for elements which contain sub-string in one of their content attributes like .text, .value, .source,...; can be a singe string or list of strings which all must match
        :param local_scope: if `True`, only elements within the current scope are returned; by default the whole page is searched (this default behavior can be changed with `ui.get.DEFAULT_LOCAL_SCOPE = True`)
        """
        self._kinds = kind
        self._markers = marker.split() if isinstance(marker, str) else marker
        self._contents = [content] if isinstance(content, str) else content
        self._within_types: list[Element] = []
        self._within_markers: list[str] = []
        self._within_kinds: list[Element] = []
        self._not_within_types: list[Element] = []
        self._not_within_markers: list[str] = []
        self._not_within_kinds: list[Element] = []
        self._exclude_kinds: list[Element] = []
        self._exclude_markers: list[str] = []
        self._exclude_content: list[str] = []
        self._scope = context.slot.parent if local_scope else context.client.layout

    def __iter__(self) -> Iterator[T]:
        return self.iterate(self._scope)

    def iterate(self, parent: Element, *, visited: List[Element] = []) -> Iterator[T]:
        for element in parent:
            element_contents = [
                element._props.get('text', ''),
                (element.text if hasattr(element, 'text') else ''),
                element._props.get('label', ''),
                element._props.get('icon', ''),
                (element.content if isinstance(element, ContentElement) else ''),
                (element.source if isinstance(element, SourceElement) else ''),
                element._props.get('placeholder', ''),
                (element._props.get('value', '') or ''),  # NOTE the value could be None
            ]
            content = ' '.join(str(c) for c in element_contents)

            if (self._kinds is None or isinstance(element, self._kinds)) and \
                (not self._markers or all(m in element._markers for m in self._markers)) and \
                (not self._contents or all(c in content for c in self._contents)) and \
                (not self._exclude_kinds or not any(isinstance(element, type) for type in self._exclude_kinds)) and \
                (not self._exclude_markers or not any(m in element._markers for m in self._exclude_markers)) and \
                (not self._exclude_content or (hasattr(element, 'text') and not any(text in element.text for text in self._exclude_content))) and \
                    (not self._within_kinds or any(element in within_element for within_element in self._within_kinds)):
                if (not self._within_types or any(isinstance(element, type) for type in self._within_types for element in visited)) and \
                    (not self._within_markers or any(m in element._markers for m in self._within_markers for element in visited)) and \
                    (not self._not_within_types or not any(isinstance(element, type) for type in self._not_within_types for element in visited)) and \
                        (not self._not_within_markers or not any(m in element._markers for m in self._not_within_markers for element in visited)):
                    yield element
            if element not in self._not_within_kinds:
                yield from self.iterate(element, visited=visited + [element])

    def __next__(self) -> T:
        if self._iterator is None:
            raise StopIteration
        return next(self._iterator)

    def __len__(self) -> int:
        return len(list(iter(self)))

    def __getitem__(self, index) -> T:
        return list(iter(self))[index]

    def within(self, *, kind: Optional[Type] = None, marker: Optional[str] = None, instance: Union[Element, list[Element], None] = None) -> Self:
        if kind is not None:
            assert issubclass(kind, Element)
            self._within_types.append(kind)
        if marker is not None:
            self._within_markers.append(marker)
        if instance is not None:
            self._within_kinds.extend(instance if isinstance(instance, list) else [instance])
        return self

    def exclude(self, *, kind: Optional[Element] = None, marker: Optional[str] = None, content: Optional[str] = None) -> Self:
        """Exclude elements with specific element type, marker or content."""

        if kind is not None:
            assert issubclass(kind, Element)
            self._exclude_kinds.append(kind)
        if marker is not None:
            self._exclude_markers.append(marker)
        if content is not None:
            self._exclude_content.append(content)
        return self

    def not_within(self, *, kind: Optional[Type] = None, marker: Optional[str] = None, instance: Union[Element, list[Element], None] = None) -> Self:
        """Exclude elements which have a parent of a specific type or marker."""

        if kind is not None:
            assert issubclass(kind, Element)
            self._not_within_types.append(kind)
        if marker is not None:
            self._not_within_markers.append(marker)
        if instance is not None:
            self._not_within_kinds.extend(instance if isinstance(instance, list) else [instance])
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
