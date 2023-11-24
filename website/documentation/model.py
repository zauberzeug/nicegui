from __future__ import annotations

import abc
import re
from dataclasses import dataclass
from typing import Callable, Iterator, List, Optional

import docutils.core

from nicegui.dataclasses import KWONLY_SLOTS
from nicegui.elements.markdown import apply_tailwind, remove_indentation


@dataclass(**KWONLY_SLOTS)
class DocumentationPart:
    title: Optional[str] = None
    description: Optional[str] = None
    link: Optional[str] = None
    function: Optional[Callable] = None


class Documentation(abc.ABC):
    TITLE: Optional[str] = None

    def __init__(self, route: str, back_link: Optional[str] = None) -> None:
        self.route = route
        self.back_link = back_link
        self._content: List[DocumentationPart] = []
        self.content()

    def __iter__(self) -> Iterator[DocumentationPart]:
        return iter(self._content)

    def add_markdown(self, title: str, description: str) -> None:
        """Add a markdown section to the documentation."""
        self._content.append(DocumentationPart(title=title, description=description))

    def add_markdown_demo(self, title: str, description: str) -> Callable[[Callable], Callable]:
        """Add a markdown section to the documentation."""
        def decorator(function: Callable) -> Callable:
            self._content.append(DocumentationPart(title=title, description=description, function=function))
            return function
        return decorator

    def add_element_intro(self, documentation: ElementDocumentation) -> None:
        """Add an element intro section to the documentation."""
        self.add_main_element_demo(documentation, intro_only=True)

    def add_main_element_demo(self, documentation: ElementDocumentation, *, intro_only: bool = False) -> None:
        """Add a demo section for an element to the documentation."""
        title, doc = documentation.element.__init__.__doc__.split('\n', 1)  # type: ignore
        doc = remove_indentation(doc).replace('param ', '')
        html = apply_tailwind(docutils.core.publish_parts(doc, writer_name='html5_polyglot')['html_body'])
        if intro_only:
            html = re.sub(r'<dl class=".* simple">.*?</dl>', '', html, flags=re.DOTALL)
        self._content.append(DocumentationPart(
            title=title,
            description=html,
            link=documentation.route if intro_only else None,
            function=documentation.main_demo,
        ))

    def add_raw_nicegui(self, function: Callable) -> Callable:
        """Add a raw NiceGUI section to the documentation."""
        self._content.append(DocumentationPart(function=function))
        return function

    @abc.abstractmethod
    def content(self) -> None:
        """Add documentation content here."""


class SectionDocumentation(Documentation):
    element_documentations: List[ElementDocumentation]

    def __init_subclass__(cls, title: str) -> None:
        cls.TITLE = title
        cls.element_documentations = []
        return super().__init_subclass__()

    def add_element_intro(self, documentation: ElementDocumentation) -> None:
        self.element_documentations.append(documentation)
        super().add_element_intro(documentation)


class ElementDocumentation(Documentation):
    element: type

    def __init_subclass__(cls, element: type) -> None:
        cls.element = element
        return super().__init_subclass__()

    def __init__(self) -> None:
        super().__init__(self.element.__name__.lower())

    @abc.abstractmethod
    def main_demo(self) -> None:
        """Add a demo for the element here."""

    def more_demos(self) -> None:
        """Add more demos for the element here."""

    def content(self) -> None:
        self.add_main_element_demo(self)
        self.more_demos()
