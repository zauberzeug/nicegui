from __future__ import annotations

import abc
from dataclasses import dataclass
from typing import Callable, Iterator, List, Optional, Union, overload

import docutils.core

from nicegui.dataclasses import KWONLY_SLOTS
from nicegui.elements.markdown import apply_tailwind, remove_indentation

from . import registry


@dataclass(**KWONLY_SLOTS)
class DocumentationPart:
    title: Optional[str] = None
    description: Optional[str] = None
    link: Optional[str] = None
    function: Optional[Callable] = None

    @property
    def link_target(self) -> Optional[str]:
        """Return the link target for in-page navigation."""
        return self.title.lower().replace(' ', '_') if self.title else None


class Documentation(abc.ABC):

    def __init__(self,
                 route: str, *,
                 title: str,
                 subtitle: str,
                 back_link: Optional[str] = None) -> None:
        self.route = route
        self.title = title
        self.subtitle = subtitle
        self.back_link = back_link
        self._content: List[DocumentationPart] = []
        self.content()
        registry.add(self)

    def __iter__(self) -> Iterator[DocumentationPart]:
        return iter(self._content)

    def __len__(self) -> int:
        return len(self._content)

    def text(self, title: str, description: str) -> None:
        """Add a text block to the documentation."""
        self._content.append(DocumentationPart(title=title, description=description))

    @overload
    def demo(self, title: str, description: str, /) -> Callable[[Callable], Callable]: ...

    @overload
    def demo(self, element: type, /) -> Callable[[Callable], Callable]: ...

    @overload
    def demo(self, function: Callable, /) -> Callable[[Callable], Callable]: ...

    def demo(self, *args) -> Callable[[Callable], Callable]:
        """Add a demo section to the documentation."""
        if len(args) == 2:
            title, description = args
        elif isinstance(args[0], type):
            title, description = args[0].__init__.__doc__.split('\n', 1)  # type: ignore
        elif callable(args[0]):
            title, description = args[0].__doc__.split('\n', 1)
        else:
            raise ValueError('Invalid arguments')

        description = remove_indentation(description).replace('param ', '')
        html = apply_tailwind(docutils.core.publish_parts(description, writer_name='html5_polyglot')['html_body'])

        def decorator(function: Callable) -> Callable:
            self._content.append(DocumentationPart(title=title, description=html, function=function))
            return function
        return decorator

    def ui(self, function: Callable) -> Callable:
        """Add arbitrary UI to the documentation."""
        self._content.append(DocumentationPart(function=function))
        return function

    def intro(self, documentation: Documentation) -> None:
        """Add an element intro section to the documentation."""
        documentation.back_link = self.route
        part = documentation._content[0]  # pylint: disable=protected-access
        part.link = documentation.route
        self._content.append(part)

    @abc.abstractmethod
    def content(self) -> None:
        """Add documentation content here."""


class SectionDocumentation(Documentation):
    _title: str
    _route: str

    def __init_subclass__(cls, title: str, name: str) -> None:
        cls._title = title
        cls._route = f'/documentation/section_{name}'
        return super().__init_subclass__()

    def __init__(self) -> None:
        super().__init__(self._route, subtitle='Documentation', title=self._title, back_link='/documentation')


class DetailDocumentation(Documentation):
    _title: str
    _route: str

    def __init_subclass__(cls, title: str, name: str) -> None:
        cls._title = title
        cls._route = f'/documentation/{name}'
        return super().__init_subclass__()

    def __init__(self) -> None:
        super().__init__(self._route, subtitle='Documentation', title=self._title)


class UiElementDocumentation(Documentation):
    _element: Union[type, Callable]

    def __init_subclass__(cls, element: Union[type, Callable]) -> None:
        cls._element = element
        return super().__init_subclass__()

    def __init__(self) -> None:
        self.element = self._element
        name = self.element.__name__.lower()
        super().__init__(f'/documentation/{name}', subtitle='Documentation', title=f'ui.*{name}*')

    def main_demo(self) -> None:
        """Add a demo for the element here."""

    def more(self) -> None:
        """Add more demos for the element here."""

    def content(self) -> None:
        @self.demo(self.element)
        def demo():
            self.main_demo()

        self.more()
