import abc
from dataclasses import dataclass
from typing import Callable, Iterator, List, Optional

from nicegui.dataclasses import KWONLY_SLOTS


@dataclass(**KWONLY_SLOTS)
class DocumentationPart:
    title: Optional[str] = None
    description: Optional[str] = None
    function: Optional[Callable] = None


class Documentation(abc.ABC):

    def __init__(self) -> None:
        self._content: List[DocumentationPart] = []
        self.content()

    def __iter__(self) -> Iterator[DocumentationPart]:
        return iter(self._content)

    def add_markdown(self, title: str, description: str) -> None:
        """Add a markdown section to the documentation."""
        self._content.append(DocumentationPart(title=title, description=description))

    def add_element_demo(self, element: type) -> Callable[[Callable], Callable]:
        """Add a demo section for an element to the documentation."""
        def decorator(function: Callable) -> Callable:
            part = DocumentationPart(title=element.__name__, description=element.__doc__ or '', function=function)
            self._content.append(part)
            return function
        return decorator

    def add_raw_nicegui(self, function: Callable) -> Callable:
        """Add a raw NiceGUI section to the documentation."""
        self._content.append(DocumentationPart(function=function))
        return function

    @abc.abstractmethod
    def content(self) -> None:
        """Add documentation content here."""
