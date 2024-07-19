from __future__ import annotations

from typing import Generic, Iterator, List, Optional, Type, TypeVar, Union

from typing_extensions import Self

from .context import context
from .element import Element
from .elements.mixins.content_element import ContentElement
from .elements.mixins.source_element import SourceElement

T = TypeVar('T', bound=Element)


class ElementFilter(Generic[T], Iterator[T]):
    DEFAULT_LOCAL_SCOPE = False

    def __init__(self, *,
                 kind: Optional[Type[T]] = None,
                 marker: Union[str, List[str], None] = None,
                 content: Union[str, List[str], None] = None,
                 local_scope: bool = DEFAULT_LOCAL_SCOPE,
                 ) -> None:
        """ElementFilter

        Sometimes it is handy to search the Python element tree of the current page.
        ``ElementFilter()`` allows powerful filtering by kind of elements, markers and content.
        It also provides a fluent interface to apply more filters like excluding elements or filtering for elements within a specific parent.
        The filter can be used as an iterator to iterate over the found elements and is always applied while iterating and not when being instantiated.

        :param kind: filter by element type; the iterator will be of type ``kind``
        :param marker: filter by element markers; can be a list of strings or a single string where markers are separated by whitespace
        :param content: filter for elements which contain ``content`` in one of their content attributes like ``.text``, ``.value``, ``.source``, ...; can be a singe string or a list of strings which all must match
        :param local_scope: if `True`, only elements within the current scope are returned; by default the whole page is searched (this default behavior can be changed with ``ElementFilter.DEFAULT_LOCAL_SCOPE = True``)
        """
        self._kind = kind or Element
        self._markers = marker.split() if isinstance(marker, str) else marker
        self._contents = [content] if isinstance(content, str) else content
        self._within_kinds: List[Type[Element]] = []
        self._within_markers: List[str] = []
        self._within_instances: List[Element] = []
        self._not_within_kinds: List[Type[Element]] = []
        self._not_within_markers: List[str] = []
        self._not_within_instances: List[Element] = []
        self._exclude_kinds: List[Type[Element]] = []
        self._exclude_markers: List[str] = []
        self._exclude_content: List[str] = []
        self._scope = context.slot.parent if local_scope else context.client.layout

    def __iter__(self) -> Iterator[T]:
        return self._iterate(self._scope)

    def _iterate(self, parent: Element, *, visited: Optional[List[Element]] = None) -> Iterator[T]:
        # pylint: disable=protected-access
        visited = visited or []
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
                element._props.get('options', {}).get('message', ''),
            ]
            content = ' '.join(str(c) for c in element_contents)

            # pylint: disable=too-many-boolean-expressions
            if (
                (self._kind is None or isinstance(element, self._kind)) and
                (not self._markers or all(m in element._markers for m in self._markers)) and
                (not self._contents or all(c in content for c in self._contents)) and
                (not self._exclude_kinds or not any(isinstance(element, kinds) for kinds in self._exclude_kinds)) and
                (not self._exclude_markers or not any(m in element._markers for m in self._exclude_markers)) and
                (not self._exclude_content or (hasattr(element, 'text') and not any(text in element.text for text in self._exclude_content))) and
                (not self._within_instances or any(element in instance for instance in self._within_instances))
            ):
                if (
                    (not self._within_kinds or any(isinstance(element, kind) for kind in self._within_kinds for element in visited)) and
                    (not self._within_markers or any(m in element._markers for m in self._within_markers for element in visited)) and
                    (not self._not_within_kinds or not any(isinstance(element, kinds) for kinds in self._not_within_kinds for element in visited)) and
                    (not self._not_within_markers or not any(m in element._markers
                                                             for m in self._not_within_markers
                                                             for element in visited))
                ):
                    yield element
            if element not in self._not_within_instances:
                yield from self._iterate(element, visited=[*visited, element])

    def __next__(self) -> T:
        if self._iterator is None:
            raise StopIteration
        return next(self._iterator)

    def __len__(self) -> int:
        return len(list(iter(self)))

    def __getitem__(self, index) -> T:
        return list(iter(self))[index]

    def within(self, *, kind: Optional[Type] = None, marker: Optional[str] = None, instance: Union[Element, List[Element], None] = None) -> Self:
        """Filter elements which have a specific match in the parent hierarchy."""
        if kind is not None:
            assert issubclass(kind, Element)
            self._within_kinds.append(kind)
        if marker is not None:
            self._within_markers.append(marker)
        if instance is not None:
            self._within_instances.extend(instance if isinstance(instance, list) else [instance])
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

    def not_within(self, *, kind: Optional[Type] = None, marker: Optional[str] = None, instance: Union[Element, List[Element], None] = None) -> Self:
        """Exclude elements which have a parent of a specific type or marker."""
        if kind is not None:
            assert issubclass(kind, Element)
            self._not_within_kinds.append(kind)
        if marker is not None:
            self._not_within_markers.append(marker)
        if instance is not None:
            self._not_within_instances.extend(instance if isinstance(instance, list) else [instance])
        return self

    def classes(self, add: Optional[str] = None, *, remove: Optional[str] = None, replace: Optional[str] = None) -> Self:
        """Apply, remove, or replace HTML classes.

        This allows modifying the look of the element or its layout using `Tailwind <https://tailwindcss.com/>`_ or `Quasar <https://quasar.dev/>`_ classes.

        Removing or replacing classes can be helpful if predefined classes are not desired.

        :param add: whitespace-delimited string of classes
        :param remove: whitespace-delimited string of classes to remove from the element
        :param replace: whitespace-delimited string of classes to use instead of existing ones
        """
        for element in self:
            element.classes(add, remove=remove, replace=replace)
        return self

    def style(self, add: Optional[str] = None, *, remove: Optional[str] = None, replace: Optional[str] = None) -> Self:
        """Apply, remove, or replace CSS definitions.

        Removing or replacing styles can be helpful if the predefined style is not desired.

        :param add: semicolon-separated list of styles to add to the element
        :param remove: semicolon-separated list of styles to remove from the element
        :param replace: semicolon-separated list of styles to use instead of existing ones
        """
        for element in self:
            element.style(add, remove=remove, replace=replace)
        return self

    def props(self, add: Optional[str] = None, *, remove: Optional[str] = None) -> Self:
        """Add or remove props.

        This allows modifying the look of the element or its layout using `Quasar <https://quasar.dev/>`_ props.
        Since props are simply applied as HTML attributes, they can be used with any HTML element.

        Boolean properties are assumed ``True`` if no value is specified.

        :param add: whitespace-delimited list of either boolean values or key=value pair to add
        :param remove: whitespace-delimited list of property keys to remove
        """
        for element in self:
            element.props(add, remove=remove)
        return self
